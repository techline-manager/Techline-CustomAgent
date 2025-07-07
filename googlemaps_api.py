import os
import requests
from typing import Dict, Tuple, Optional
from dotenv import load_dotenv

load_dotenv()

class GoogleMapsAPI:
    """Google Maps API integration for address validation and geocoding."""
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_MAPS_API_KEY environment variable is required")
        
        self.geocoding_url = "https://maps.googleapis.com/maps/api/geocode/json"
        self.places_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    
    def validate_address(self, address: str) -> Tuple[bool, Optional[Dict]]:
        """
        Validate an address using Google Maps Geocoding API.
        
        Args:
            address (str): The address to validate
            
        Returns:
            Tuple[bool, Optional[Dict]]: (is_valid, address_data)
        """
        try:
            params = {
                'address': address,
                'key': self.api_key
            }
            
            response = requests.get(self.geocoding_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'OK' and data['results']:
                # Address is valid
                result = data['results'][0]
                address_data = {
                    'formatted_address': result['formatted_address'],
                    'location': result['geometry']['location'],
                    'place_id': result['place_id'],
                    'address_components': result['address_components']
                }
                return True, address_data
            else:
                return False, None
                
        except requests.RequestException as e:
            print(f"Error validating address: {e}")
            return False, None
    
    def validate_zip_code(self, zip_code: str, country_code: str = "US") -> Tuple[bool, Optional[Dict]]:
        """
        Validate a zip code using Google Maps Geocoding API.
        
        Args:
            zip_code (str): The zip code to validate
            country_code (str): Country code (default: "US")
            
        Returns:
            Tuple[bool, Optional[Dict]]: (is_valid, location_data)
        """
        try:
            # Format the query to be more specific
            query = f"{zip_code}, {country_code}"
            
            params = {
                'address': query,
                'key': self.api_key,
                'components': f'country:{country_code}'
            }
            
            response = requests.get(self.geocoding_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'OK' and data['results']:
                result = data['results'][0]
                
                # Check if the result actually contains the zip code
                postal_code_found = False
                for component in result['address_components']:
                    if 'postal_code' in component['types']:
                        if component['long_name'] == zip_code or component['short_name'] == zip_code:
                            postal_code_found = True
                            break
                
                if postal_code_found:
                    location_data = {
                        'formatted_address': result['formatted_address'],
                        'location': result['geometry']['location'],
                        'place_id': result['place_id'],
                        'zip_code': zip_code,
                        'city': self._extract_city(result['address_components']),
                        'state': self._extract_state(result['address_components'])
                    }
                    return True, location_data
                else:
                    return False, None
            else:
                return False, None
                
        except requests.RequestException as e:
            print(f"Error validating zip code: {e}")
            return False, None
    
    def _extract_city(self, address_components) -> Optional[str]:
        """Extract city from address components."""
        for component in address_components:
            if 'locality' in component['types']:
                return component['long_name']
            elif 'administrative_area_level_2' in component['types']:
                return component['long_name']
        return None
    
    def _extract_state(self, address_components) -> Optional[str]:
        """Extract state from address components."""
        for component in address_components:
            if 'administrative_area_level_1' in component['types']:
                return component['short_name']
        return None