from flask import jsonify, request
from flask_jwt_extended import jwt_required
from .. import explore_bp
import os
import requests

@explore_bp.route('/places', methods=['GET'])
@jwt_required()
def get_places():
    try:
        # Get parameters from request
        lat = request.args.get('lat')
        lng = request.args.get('lng')
        radius = request.args.get('radius', '1500')  # Default 1.5km radius
        type = request.args.get('type', 'tourist_attraction')  # Default type
        
        if not lat or not lng:
            return jsonify({
                'error': 'Latitude and longitude are required'
            }), 400

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
            'location': f"{lat},{lng}",
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
            
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug print
        return jsonify({
            'error': 'An error occurred while fetching places',
            'details': str(e)
        }), 500