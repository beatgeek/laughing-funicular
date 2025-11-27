"""Data models for movies and shows."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Content:
    """Represents a movie or TV show."""
    title: str
    content_type: str  # 'movie' or 'show'
    duration_minutes: int
    rating: Optional[float] = None
    genres: Optional[list] = None
    description: Optional[str] = None
    year: Optional[int] = None
    wikipedia_url: Optional[str] = None
    
    def __post_init__(self):
        if self.genres is None:
            self.genres = []
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'title': self.title,
            'content_type': self.content_type,
            'duration_minutes': self.duration_minutes,
            'rating': self.rating,
            'genres': self.genres,
            'description': self.description,
            'year': self.year,
            'wikipedia_url': self.wikipedia_url
        }


@dataclass
class Journey:
    """Represents a content journey (like a flight itinerary)."""
    total_duration: int
    contents: list
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'total_duration': self.total_duration,
            'contents': [c.to_dict() for c in self.contents]
        }
