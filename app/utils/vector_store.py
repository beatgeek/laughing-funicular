"""Vector store for semantic search using Qdrant."""
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import os
from typing import List, Dict, Optional
import uuid


class VectorStore:
    """Manages semantic search using Qdrant vector database."""
    
    def __init__(self, collection_name: str = "content_collection"):
        """Initialize vector store with Qdrant client."""
        self.collection_name = collection_name
        
        # Use in-memory Qdrant for simplicity
        # In production, connect to a Qdrant server
        self.client = QdrantClient(":memory:")
        
        # Initialize sentence transformer model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.vector_size = 384  # Dimension of all-MiniLM-L6-v2
        
        # Create collection if it doesn't exist
        self._init_collection()
    
    def _init_collection(self):
        """Initialize the Qdrant collection."""
        try:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE),
            )
        except Exception as e:
            print(f"Collection already exists or error: {e}")
    
    def add_content(self, content_id: str, title: str, description: str, 
                   metadata: Optional[Dict] = None):
        """Add content to the vector store."""
        # Create embedding from title and description
        text = f"{title}. {description}"
        vector = self.model.encode(text).tolist()
        
        # Prepare payload
        payload = {
            "content_id": content_id,
            "title": title,
            "description": description
        }
        if metadata:
            payload.update(metadata)
        
        # Add to Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload=payload
                )
            ]
        )
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for similar content using semantic search."""
        # Create query embedding
        query_vector = self.model.encode(query).tolist()
        
        # Search in Qdrant
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit
        )
        
        # Format results
        results = []
        for hit in search_result:
            results.append({
                "score": hit.score,
                "content": hit.payload
            })
        
        return results
    
    def clear_collection(self):
        """Clear all data from the collection."""
        self._init_collection()
