"""Qdrant Vector DB connection and search service."""
from typing import List, Dict, Any, Optional, Union
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from app.core.config import settings
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)


class QdrantService:
    """Service for interacting with Qdrant vector database."""
    
    def __init__(self):
        """Initialize Qdrant client with lazy connection."""
        self.client = None
        self.collection_name = "netherlands_pilot"
        self.openai_client = OpenAI(api_key=settings.openai_api_key)
        
        # Store connection parameters for lazy initialization
        self.qdrant_url = settings.qdrant_url
        self.qdrant_api_key = settings.qdrant_api_key
        
        # Log configuration (mask sensitive data)
        logger.info(f"Qdrant configured - URL: {self.qdrant_url[:50]}..." if len(self.qdrant_url) > 50 else f"Qdrant configured - URL: {self.qdrant_url}")
        logger.info(f"Qdrant API Key: {'Set' if self.qdrant_api_key else 'Not set'}")
    
    def _ensure_client(self):
        """Lazy initialization of Qdrant client with better error handling."""
        if self.client is not None:
            return True
        
        try:
            logger.info(f"Initializing Qdrant client to: {self.qdrant_url}")
            
            # Create client with timeout settings for cloud environments
            if self.qdrant_api_key:
                self.client = QdrantClient(
                    url=self.qdrant_url,
                    api_key=self.qdrant_api_key,
                    timeout=30.0  # 30 second timeout for cloud
                )
            else:
                self.client = QdrantClient(
                    url=self.qdrant_url,
                    timeout=30.0  # 30 second timeout for cloud
                )
            
            # Test connection with a lightweight operation
            try:
                collections = self.client.get_collections()
                logger.info(f"✅ Qdrant connection successful. Collections: {[c.name for c in collections.collections]}")
                return True
            except Exception as e:
                logger.error(f"❌ Qdrant connection test failed: {str(e)}")
                logger.error(f"   URL: {self.qdrant_url}")
                logger.error(f"   Error type: {type(e).__name__}")
                self.client = None
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to create Qdrant client: {str(e)}")
            logger.error(f"   URL: {self.qdrant_url}")
            logger.error(f"   Error type: {type(e).__name__}")
            self.client = None
            return False
    
    def search(
        self,
        query: str,
        limit: int = 5,
        country: str = "netherlands",
        year: str = "2025"
    ) -> List[Dict[str, Any]]:
        """
        Search the vector database with mandatory metadata filters.
        
        CRITICAL: Must always filter by country="netherlands" and year="2025" for V1.
        
        Args:
            query: Search query text
            limit: Number of results to return (default: 5)
            country: Country filter (default: "netherlands")
            year: Year filter (default: "2025")
        
        Returns:
            List of search results with metadata
        """
        try:
            # Lazy initialization - connect on first use
            if not self._ensure_client():
                logger.warning("Qdrant client not available. Returning empty results.")
                return []
            
            # Convert query text to embedding vector
            # Qdrant search requires a query vector, not text
            query_vector = self._text_to_embedding(query)
            
            # Perform vector search using search method (standard API for qdrant-client 1.10+)
            # No metadata filters for V1 - search all documents
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit
            )
            
            # Format results
            # search_points returns list of ScoredPoint objects
            results = []
            for result in search_results:
                results.append({
                    "score": result.score,
                    "payload": result.payload,
                    "id": result.id
                })
            
            logger.info(f"Qdrant search successful: {len(results)} results for query: {query[:50]}...")
            return results
        
        except Exception as e:
            # Log detailed error information
            logger.error(f"Qdrant search error: {str(e)}")
            logger.error(f"   Error type: {type(e).__name__}")
            logger.error(f"   QDRANT_URL: {self.qdrant_url}")
            logger.warning("System will continue without Qdrant context (using LLM knowledge only)")
            
            # Reset client to force reconnection on next attempt
            self.client = None
            return []
    
    def format_context(self, search_results: List[Dict[str, Any]]) -> str:
        """
        Format search results into a context string for LLM.
        
        Args:
            search_results: List of search result dictionaries
        
        Returns:
            Formatted context string
        """
        if not search_results:
            return "No relevant context found in knowledge base."
        
        context_parts = []
        for i, result in enumerate(search_results, 1):
            payload = result.get("payload", {})
            # LangChain QdrantVectorStore stores: page_content and metadata
            content = payload.get("page_content", "")
            metadata = payload.get("metadata", {})
            source_filename = metadata.get("source_filename") or metadata.get("source", "Unknown")
            
            context_parts.append(f"Context {i} (Source: {source_filename}):\n{content}")
        
        return "\n---\n".join(context_parts)
    
    def _text_to_embedding(self, text: str) -> List[float]:
        """
        Convert text to embedding vector using OpenAI.
        
        Args:
            text: Text to convert to embedding
        
        Returns:
            List of floats representing the embedding vector
        """
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {str(e)}")
            # Return empty vector as fallback (will result in no matches)
            return [0.0] * 1536  # text-embedding-3-small dimension

