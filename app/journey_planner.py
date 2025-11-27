"""Journey planner for creating content viewing itineraries."""
from typing import List, Optional
from app.models import Content, Journey
from app.scrapers.wikipedia_scraper import WikipediaScraper
from app.scrapers.rotten_tomatoes_scraper import RottenTomatoesScraper
from app.utils.vector_store import VectorStore


class JourneyPlanner:
    """Plans content viewing journeys based on duration and preferences."""
    
    def __init__(self):
        """Initialize the journey planner."""
        self.wiki_scraper = WikipediaScraper()
        self.rt_scraper = RottenTomatoesScraper()
        self._vector_store = None
    
    @property
    def vector_store(self):
        """Lazy initialization of vector store."""
        if self._vector_store is None:
            self._vector_store = VectorStore()
        return self._vector_store
    
    def search_content(self, query: str, limit: int = 10) -> List[Content]:
        """Search for content matching the query."""
        contents = []
        
        # Search Wikipedia
        wiki_results = self.wiki_scraper.search_content(query, limit=limit)
        
        for title in wiki_results:
            content = self.wiki_scraper.get_content_info(title)
            if content:
                # Add rating from Rotten Tomatoes
                rating = self.rt_scraper.get_rating(content.title)
                if rating:
                    content.rating = rating
                
                contents.append(content)
                
                # Add to vector store for semantic search
                self.vector_store.add_content(
                    content_id=content.title,
                    title=content.title,
                    description=content.description or "",
                    metadata={
                        'content_type': content.content_type,
                        'duration_minutes': content.duration_minutes,
                        'genres': content.genres,
                        'rating': content.rating
                    }
                )
        
        return contents
    
    def semantic_search(self, query: str, limit: int = 10) -> List[Content]:
        """Perform semantic search for similar content."""
        results = self.vector_store.search(query, limit=limit)
        
        contents = []
        for result in results:
            payload = result['content']
            content = Content(
                title=payload['title'],
                content_type=payload.get('content_type', 'movie'),
                duration_minutes=payload.get('duration_minutes', 120),
                rating=payload.get('rating'),
                genres=payload.get('genres', []),
                description=payload.get('description', '')
            )
            contents.append(content)
        
        return contents
    
    def create_journey(self, target_duration: int, preferences: Optional[str] = None,
                      content_type: Optional[str] = None) -> Journey:
        """
        Create a viewing journey to fill the target duration.
        
        Args:
            target_duration: Target duration in minutes
            preferences: Optional search query for content preferences
            content_type: Filter by 'movie' or 'show'
        
        Returns:
            Journey object with selected content
        """
        # Search for content based on preferences
        if preferences:
            available_content = self.search_content(preferences, limit=20)
        else:
            # Default search
            available_content = self.search_content("popular movies", limit=20)
        
        # Filter by content type if specified
        if content_type:
            available_content = [c for c in available_content 
                               if c.content_type == content_type]
        
        # Sort by rating (if available)
        available_content.sort(key=lambda x: x.rating or 0, reverse=True)
        
        # Select content to fill the journey
        selected_content = []
        total_duration = 0
        
        for content in available_content:
            if total_duration + content.duration_minutes <= target_duration + 30:  # 30 min tolerance
                selected_content.append(content)
                total_duration += content.duration_minutes
                
                if abs(total_duration - target_duration) < 15:  # Within 15 minutes
                    break
        
        return Journey(
            total_duration=total_duration,
            contents=selected_content
        )
