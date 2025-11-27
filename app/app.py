"""Flask application for Content Journey Finder."""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from app.journey_planner import JourneyPlanner

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__, 
           template_folder='templates',
           static_folder='static')
CORS(app)

# Configure app
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Initialize journey planner
planner = JourneyPlanner()


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/api/search', methods=['POST'])
def search():
    """Search for content."""
    data = request.get_json()
    query = data.get('query', '')
    limit = data.get('limit', 10)
    
    try:
        contents = planner.search_content(query, limit=limit)
        return jsonify({
            'success': True,
            'contents': [c.to_dict() for c in contents]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/semantic-search', methods=['POST'])
def semantic_search():
    """Perform semantic search."""
    data = request.get_json()
    query = data.get('query', '')
    limit = data.get('limit', 10)
    
    try:
        contents = planner.semantic_search(query, limit=limit)
        return jsonify({
            'success': True,
            'contents': [c.to_dict() for c in contents]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/plan-journey', methods=['POST'])
def plan_journey():
    """Plan a content viewing journey."""
    data = request.get_json()
    duration = data.get('duration', 180)  # Default 3 hours
    preferences = data.get('preferences', '')
    content_type = data.get('content_type', None)
    
    try:
        journey = planner.create_journey(
            target_duration=duration,
            preferences=preferences if preferences else None,
            content_type=content_type
        )
        return jsonify({
            'success': True,
            'journey': journey.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(host='0.0.0.0', port=port, debug=debug)
