from flask import jsonify, request
from flask_jwt_extended import jwt_required
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from .. import explore_bp
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@explore_bp.route('/geocode', methods=['GET'])
@jwt_required()
def get_coordinates():
    address = request.args.get('address')
    
    if not address:
        return jsonify({
            'error': 'Address parameter is required'
        }), 400
    
    try:
        # Current implementation using Nominatim
        geolocator = Nominatim(user_agent="go_tripping")
        location = geolocator.geocode(address)
        
        if location:
            return jsonify({
                'address': address,
                'latitude': location.latitude,
                'longitude': location.longitude
            }), 200
        else:
            return jsonify({
                'error': 'Could not find coordinates for the given address'
            }), 404

        # Google Places API implementation (commented out for now)
        """
        # Get API key from environment variables
        api_key = os.getenv('GOOGLE_PLACES_API_KEY')
        if not api_key:
            return jsonify({
                'error': 'Google Places API key not configured'
            }), 500

        # Construct the Google Places API URL
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            'address': address,
            'key': api_key
        }

        # Make request to Google Places API
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200 and data.get('status') == 'OK':
            result = data['results'][0]
            return jsonify({
                'address': result['formatted_address'],
                'latitude': result['geometry']['location']['lat'],
                'longitude': result['geometry']['location']['lng']
            }), 200
        else:
            return jsonify({
                'error': 'Could not find coordinates for the given address',
                'details': data.get('error_message', 'Unknown error')
            }), 404
        """
            
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        return jsonify({
            'error': 'Geocoding service is currently unavailable'
        }), 503
    except Exception as e:
        return jsonify({
            'error': 'An error occurred while geocoding the address'
        }), 500 