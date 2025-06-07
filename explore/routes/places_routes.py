from flask import jsonify, request
from flask_jwt_extended import jwt_required
from .. import explore_bp
import os
import json
from pathlib import Path

@explore_bp.route('/places', methods=['GET'])
@jwt_required()
def get_places():
    try:
        # Get the path to places_data.json
        data_file = Path(__file__).parent.parent / 'data' / 'places_data.json'
        
        # Read the JSON data
        with open(data_file, 'r') as f:
            data = json.load(f)
            
        return jsonify(data), 200

        # Google Places API implementation (commented out)
        """
        # Get parameters from request
        location = request.args.get('location', 'Toronto')
        radius = request.args.get('radius', '5000')  # Default 5km radius
        type = request.args.get('type', 'tourist_attraction')  # Default type
        
        # Get API key from environment variables
        api_key = os.getenv('GOOGLE_PLACES_API_KEY')
        print(f"API Key loaded: {'Yes' if api_key else 'No'}")  # Debug print
        
        if not api_key:
            return jsonify({
                'error': 'Google Places API key not configured'
            }), 500

        # Construct the Google Places API URL
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            'location': location,
            'radius': radius,
            'type': type,
            'key': api_key
        }

        # Make request to Google Places API
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200 and data.get('status') == 'OK':
            return jsonify(data), 200
        else:
            return jsonify({
                'error': 'Could not fetch places',
                'details': data.get('error_message', 'Unknown error')
            }), 404
        """
            
    except FileNotFoundError:
        return jsonify({
            'error': 'Places data file not found'
        }), 404
    except json.JSONDecodeError:
        return jsonify({
            'error': 'Invalid JSON data in places file'
        }), 500
    except Exception as e:
        return jsonify({
            'error': 'An error occurred while fetching places'
        }), 500