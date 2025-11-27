# Content Journey Finder 🎬✈️

A Python web application that helps you plan your perfect viewing journey, just like booking a flight! Find movies and TV shows to watch during your travels, organized as "journey legs" to perfectly fill your available time.

## Features

- **Travel Finder Style Interface**: Plan your content viewing journey with an intuitive, flight-booking-inspired UI
- **Smart Duration Matching**: Enter your available time (e.g., flight duration) and get a perfectly matched content itinerary
- **Wikipedia Integration**: Fetches rich movie and TV show data from Wikipedia
- **Rotten Tomatoes Ratings**: Includes rating data (demonstration with simulated ratings)
- **Semantic Search**: Uses Qdrant vector database with sentence transformers for intelligent content recommendations
- **Flexible Filtering**: Filter by content type (movies vs. TV shows) and genre preferences
- **Beautiful UI**: Modern, responsive design with gradient backgrounds and smooth animations

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Data Sources**: Wikipedia API, web scraping (Rotten Tomatoes concept)
- **Semantic Search**: Qdrant vector database with sentence-transformers
- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **ML Models**: all-MiniLM-L6-v2 for text embeddings

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/beatgeek/laughing-funicular.git
cd laughing-funicular
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (optional):
```bash
cp .env.example .env
# Edit .env if needed
```

## Usage

### Running Locally

Start the application:
```bash
python run.py
```

The application will be available at `http://localhost:5000`

### Using the Application

1. **Enter Journey Duration**: Specify how long your journey is (e.g., flight duration in minutes)
2. **Add Preferences**: Enter genres, themes, or specific titles you're interested in
3. **Select Content Type**: Choose movies, TV shows, or both
4. **Plan Journey**: Click "Plan My Journey" to get your personalized content itinerary
5. **View Results**: See your journey broken down into "legs" with details about each movie/show

### API Endpoints

The application provides RESTful API endpoints:

- `POST /api/plan-journey`: Create a viewing journey
  ```json
  {
    "duration": 180,
    "preferences": "action movies",
    "content_type": "movie"
  }
  ```

- `POST /api/search`: Search for content
  ```json
  {
    "query": "science fiction",
    "limit": 10
  }
  ```

- `POST /api/semantic-search`: Semantic search for similar content
  ```json
  {
    "query": "time travel adventure",
    "limit": 10
  }
  ```

## Architecture

The application follows a modular architecture:

```
app/
├── app.py                  # Flask application and routes
├── models.py               # Data models (Content, Journey)
├── journey_planner.py      # Journey planning logic
├── scrapers/
│   ├── wikipedia_scraper.py      # Wikipedia data fetching
│   └── rotten_tomatoes_scraper.py # Rating data (demo)
├── utils/
│   └── vector_store.py     # Qdrant vector database integration
├── templates/
│   └── index.html          # Main UI template
└── static/
    ├── css/styles.css      # Styling
    └── js/app.js           # Frontend logic
```

## How It Works

1. **Content Discovery**: The application searches Wikipedia for movies and TV shows based on user preferences
2. **Data Enrichment**: Each piece of content is enriched with metadata (duration, genre, description, year)
3. **Vector Embedding**: Content descriptions are converted to vector embeddings using sentence transformers
4. **Semantic Search**: Qdrant vector database enables intelligent similarity-based recommendations
5. **Journey Planning**: An algorithm selects content to fill the target duration while maximizing ratings
6. **Journey Presentation**: Results are displayed in a travel-itinerary format with "journey legs"

## Limitations & Future Enhancements

### Current Limitations
- Rotten Tomatoes integration uses simulated ratings (demo purposes)
- Duration extraction from Wikipedia is heuristic-based
- In-memory Qdrant instance (data not persisted between restarts)

### Potential Enhancements
- Official Rotten Tomatoes API integration
- User accounts and saved journeys
- More sophisticated duration matching algorithms
- Additional data sources (IMDb, TMDB)
- Persistent vector database
- Content streaming platform integration
- Multi-language support

## Development

### Running Tests

(Tests to be implemented)

```bash
python -m pytest
```

### Code Structure

The codebase follows Python best practices:
- Type hints for better code clarity
- Dataclasses for clean data models
- Modular design with separation of concerns
- RESTful API design

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Mozilla Public License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Wikipedia for providing rich content data
- Qdrant for vector database technology
- Sentence Transformers for text embeddings
- The open-source community

## Disclaimer

This is a demonstration application. Rotten Tomatoes ratings are simulated for demonstration purposes. In a production environment, proper API integrations and rate limiting should be implemented.
