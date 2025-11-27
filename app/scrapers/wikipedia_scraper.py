"""Wikipedia scraper for movie and show information."""
import wikipedia
import re
from typing import Optional, Dict, List
from app.models import Content


class WikipediaScraper:
    """Scrapes movie and show data from Wikipedia."""
    
    @staticmethod
    def search_content(query: str, limit: int = 5) -> List[str]:
        """Search for content titles on Wikipedia."""
        try:
            results = wikipedia.search(query, results=limit)
            return results
        except Exception as e:
            print(f"Error searching Wikipedia: {e}")
            return []
    
    @staticmethod
    def get_content_info(title: str) -> Optional[Content]:
        """Get detailed information about a movie or show from Wikipedia."""
        try:
            page = wikipedia.page(title, auto_suggest=False)
            summary = page.summary
            
            # Try to extract duration and type from the summary
            content_type = 'movie'
            duration = 120  # Default duration
            
            # Look for runtime information
            runtime_match = re.search(r'(\d+)\s*(?:minutes?|mins?)', summary, re.IGNORECASE)
            if runtime_match:
                duration = int(runtime_match.group(1))
            else:
                # Default durations based on keywords
                if any(keyword in summary.lower() for keyword in ['television', 'tv series', 'series']):
                    content_type = 'show'
                    duration = 45  # Average episode length
            
            # Try to extract year
            year_match = re.search(r'\b(19\d{2}|20\d{2})\b', summary)
            year = int(year_match.group(1)) if year_match else None
            
            # Extract genres (simple heuristic)
            genres = []
            genre_keywords = ['action', 'comedy', 'drama', 'thriller', 'horror', 
                            'science fiction', 'romance', 'documentary', 'animation']
            for genre in genre_keywords:
                if genre in summary.lower():
                    genres.append(genre.title())
            
            return Content(
                title=page.title,
                content_type=content_type,
                duration_minutes=duration,
                description=summary[:300] + '...' if len(summary) > 300 else summary,
                year=year,
                genres=genres[:3],  # Limit to 3 genres
                wikipedia_url=page.url
            )
        except wikipedia.exceptions.DisambiguationError as e:
            # Try the first option
            if e.options:
                try:
                    return WikipediaScraper.get_content_info(e.options[0])
                except:
                    pass
        except Exception as e:
            print(f"Error fetching Wikipedia page for '{title}': {e}")
        
        return None
