"""
Tools for the multi-agent tourism system.
Contains Weather Agent and Places Agent tools.
"""
import requests
from typing import Optional, Dict, List
import json


def get_coordinates(place_name: str) -> Optional[Dict[str, float]]:
    """
    Get coordinates (latitude, longitude) for a place using Nominatim API.
    
    Args:
        place_name: Name of the place
        
    Returns:
        Dictionary with 'lat' and 'lon' keys, or None if place not found
    """
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": place_name,
            "format": "json",
            "limit": 1
        }
        headers = {
            "User-Agent": "Tourism-Agent/1.0"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data and len(data) > 0:
            location = data[0]
            return {
                "lat": float(location["lat"]),
                "lon": float(location["lon"]),
                "display_name": location.get("display_name", place_name)
            }
        return None
    except Exception as e:
        print(f"Error getting coordinates: {e}")
        return None


def weather_agent(place_name: str) -> str:
    """
    Weather Agent: Gets current weather and forecast for a place.
    Uses Open-Meteo API.
    
    Args:
        place_name: Name of the place
        
    Returns:
        Formatted weather information string
    """
    try:
        # First, get coordinates
        coords = get_coordinates(place_name)
        if not coords:
            return f"I don't know if this place exists: {place_name}"
        
        lat = coords["lat"]
        lon = coords["lon"]
        
        # Get weather data from Open-Meteo
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,precipitation_probability",
            "timezone": "auto"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if "current" in data:
            current = data["current"]
            temp = current.get("temperature_2m", "N/A")
            precip_prob = current.get("precipitation_probability", 0)
            
            return f"In {place_name} it's currently {int(temp)}°C with a chance of {int(precip_prob)}% to rain."
        else:
            return f"Could not fetch weather data for {place_name}"
            
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {str(e)}"
    except Exception as e:
        return f"Error in weather agent: {str(e)}"


def search_famous_places_by_name(city_name: str) -> List[str]:
    """
    Search for famous tourist places by name using Nominatim API.
    This helps find well-known places that might not be in the radius search.
    
    Args:
        city_name: Name of the city
        
    Returns:
        List of famous place names found
    """
    famous_places = []
    
    # Map of cities to their famous places
    city_famous_places = {
        'bangalore': [
            'Bannerghatta National Park',
            'Vidhana Soudha',
            'Tipu Sultan Palace',
            'ISKCON Temple Bangalore',
            'Nandi Hills',
            'Lalbagh Botanical Garden',
            'Cubbon Park',
            'Bangalore Palace',
            'Ulsoor Lake',
            'Wonderla Bangalore',
            'Innovative Film City',
            'Bannerghatta Biological Park'
        ],
        'bengaluru': [
            'Bannerghatta National Park',
            'Vidhana Soudha',
            'Tipu Sultan Palace',
            'ISKCON Temple Bangalore',
            'Nandi Hills',
            'Lalbagh Botanical Garden',
            'Cubbon Park',
            'Bangalore Palace'
        ],
        'mysore': [
            'Mysore Palace',
            'Chamundi Hills',
            'Brindavan Gardens',
            'St. Philomena\'s Church',
            'Jaganmohan Palace',
            'Somnathpur Temple'
        ],
        'udupi': [
            'Udupi Sri Krishna Temple',
            'Malpe Beach',
            'St. Mary\'s Island',
            'Kaup Beach'
        ]
    }
    
    city_lower = city_name.lower()
    
    # Get famous places for this city
    places_to_search = []
    for key, places in city_famous_places.items():
        if key in city_lower:
            places_to_search = places
            break
    
    # Search for each famous place
    for place in places_to_search:
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                "q": f"{place}, {city_name}",
                "format": "json",
                "limit": 1
            }
            headers = {"User-Agent": "Tourism-Agent/1.0"}
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    result = data[0]
                    # Check if it's a tourist attraction
                    place_type = result.get('type', '')
                    class_type = result.get('class', '')
                    if any(tag in class_type for tag in ['tourism', 'historic', 'leisure', 'amenity']) or \
                       any(tag in place_type for tag in ['tourism', 'historic', 'leisure', 'amenity']):
                        display_name = result.get('display_name', '')
                        # Extract just the place name
                        name = display_name.split(',')[0].strip()
                        if name:
                            famous_places.append(name)
        except Exception as e:
            continue
    
    return famous_places


def places_agent(place_name: str) -> str:
    """
    Places Agent: Gets tourist attractions for a place.
    Uses Nominatim for geocoding and Overpass API for places.
    Enhanced to find famous places by name and increase search radius.
    
    Args:
        place_name: Name of the place
        
    Returns:
        Formatted list of tourist attractions (up to 20)
    """
    try:
        # First, get coordinates
        coords = get_coordinates(place_name)
        if not coords:
            return f"I don't know if this place exists: {place_name}"
        
        lat = coords["lat"]
        lon = coords["lon"]
        
        # Search for famous places by name first
        famous_places = search_famous_places_by_name(place_name)
        
        # Comprehensive Overpass API query for all tourist attraction types
        # Increased radius to 100km for major cities to catch places like Nandi Hills
        # Categories: National parks, Zoos, Art galleries, Beaches, Hiking, Famous streets, 
        #            Adventure spots, Temples/Churches/Mosques, Viewpoints
        search_radius = 100000  # 100km for comprehensive search
        
        overpass_query = f"""
        [out:json][timeout:60];
        (
          // 1. ZOOS & BIOLOGICAL PARKS
          node["tourism"="zoo"](around:{search_radius},{lat},{lon});
          way["tourism"="zoo"](around:{search_radius},{lat},{lon});
          relation["tourism"="zoo"](around:{search_radius},{lat},{lon});
          
          // 2. ART GALLERIES
          node["tourism"="gallery"](around:{search_radius},{lat},{lon});
          node["amenity"="arts_centre"](around:{search_radius},{lat},{lon});
          way["tourism"="gallery"](around:{search_radius},{lat},{lon});
          way["amenity"="arts_centre"](around:{search_radius},{lat},{lon});
          
          // 3. NATIONAL PARKS & NATURE RESERVES (including Bannerghatta)
          node["leisure"="nature_reserve"](around:{search_radius},{lat},{lon});
          node["boundary"="national_park"](around:{search_radius},{lat},{lon});
          way["leisure"="nature_reserve"](around:{search_radius},{lat},{lon});
          way["boundary"="national_park"](around:{search_radius},{lat},{lon});
          relation["boundary"="national_park"](around:{search_radius},{lat},{lon});
          relation["leisure"="nature_reserve"](around:{search_radius},{lat},{lon});
          
          // 4. BEACHES
          node["natural"="beach"](around:{search_radius},{lat},{lon});
          node["leisure"="beach_resort"](around:{search_radius},{lat},{lon});
          way["natural"="beach"](around:{search_radius},{lat},{lon});
          way["leisure"="beach_resort"](around:{search_radius},{lat},{lon});
          
          // 5. HIKING TRAILS & PEAKS (including Nandi Hills)
          node["natural"="peak"](around:{search_radius},{lat},{lon});
          node["natural"="volcano"](around:{search_radius},{lat},{lon});
          node["natural"="hill"](around:{search_radius},{lat},{lon});
          way["route"="hiking"](around:{search_radius},{lat},{lon});
          way["leisure"="track"]["sport"="hiking"](around:{search_radius},{lat},{lon});
          
          // 6. VIEWPOINTS (scenic spots)
          node["tourism"="viewpoint"](around:{search_radius},{lat},{lon});
          way["tourism"="viewpoint"](around:{search_radius},{lat},{lon});
          
          // 7. ADVENTURE SPOTS
          node["tourism"="theme_park"](around:{search_radius},{lat},{lon});
          node["leisure"="adult_gaming_centre"](around:{search_radius},{lat},{lon});
          node["leisure"="water_park"](around:{search_radius},{lat},{lon});
          node["sport"~"^(climbing|paragliding|rafting|canoeing|kayaking|surfing|diving|skydiving)$"](around:{search_radius},{lat},{lon});
          way["tourism"="theme_park"](around:{search_radius},{lat},{lon});
          way["leisure"="water_park"](around:{search_radius},{lat},{lon});
          way["sport"~"^(climbing|paragliding|rafting|canoeing|kayaking|surfing|diving|skydiving)$"](around:{search_radius},{lat},{lon});
          
          // 8. FAMOUS TEMPLES, CHURCHES, MOSQUES, SHRINES (including ISKCON)
          node["amenity"="place_of_worship"](around:{search_radius},{lat},{lon});
          node["historic"~"^(temple|church|mosque|shrine|monastery|abbey|cathedral|basilica)$"](around:{search_radius},{lat},{lon});
          way["amenity"="place_of_worship"](around:{search_radius},{lat},{lon});
          way["historic"~"^(temple|church|mosque|shrine|monastery|abbey|cathedral|basilica)$"](around:{search_radius},{lat},{lon});
          relation["amenity"="place_of_worship"](around:{search_radius},{lat},{lon});
          
          // 9. GOVERNMENT BUILDINGS & PALACES (including Vidhana Soudha, Tipu Sultan Palace)
          node["building"="government"](around:{search_radius},{lat},{lon});
          node["historic"="palace"](around:{search_radius},{lat},{lon});
          way["building"="government"](around:{search_radius},{lat},{lon});
          way["historic"="palace"](around:{search_radius},{lat},{lon});
          relation["historic"="palace"](around:{search_radius},{lat},{lon});
          
          // 10. FAMOUS STREETS (historic/notable streets with names)
          way["highway"~"^(primary|secondary|tertiary|residential|pedestrian|living_street)$"]["name"~"."](around:{search_radius},{lat},{lon});
          
          // 11. OTHER TOURIST ATTRACTIONS
          node["tourism"~"^(attraction|museum|artwork)$"](around:{search_radius},{lat},{lon});
          node["historic"~"^(monument|castle|tower|ruins|tomb|fort|memorial|archaeological_site)$"](around:{search_radius},{lat},{lon});
          node["leisure"~"^(park|stadium|golf_course|marina)$"](around:{search_radius},{lat},{lon});
          node["amenity"~"^(theatre|cinema|library|planetarium)$"](around:{search_radius},{lat},{lon});
          way["tourism"~"^(attraction|museum|artwork)$"](around:{search_radius},{lat},{lon});
          way["historic"~"^(monument|castle|tower|ruins|tomb|fort|memorial|archaeological_site)$"](around:{search_radius},{lat},{lon});
          way["leisure"~"^(park|stadium|golf_course|marina)$"](around:{search_radius},{lat},{lon});
          way["amenity"~"^(theatre|cinema|library|planetarium)$"](around:{search_radius},{lat},{lon});
        );
        out center;
        """
        
        url = "https://overpass-api.de/api/interpreter"
        response = requests.post(url, data={"data": overpass_query}, timeout=60)
        response.raise_for_status()
        
        data = response.json()
        
        places = []
        seen_names = set()
        
        # Add famous places found by name search first (prioritize them)
        for place in famous_places:
            if place and place not in seen_names:
                places.append(place)
                seen_names.add(place.lower())
        
        # Keywords to exclude (companies, stores, non-tourist entities)
        exclude_keywords = [
            'store', 'shop', 'mall', 'market', 'company', 'corp', 'ltd', 'inc', 
            'dna', 'lab', 'laboratory', 'office', 'building', 'commercial',
            'warehouse', 'factory', 'industrial', 'business', 'enterprise'
        ]
        
        if "elements" in data:
            for element in data["elements"]:
                # Process nodes, ways, and relations with tags
                if element.get("type") in ["node", "way", "relation"]:
                    tags = element.get("tags", {})
                    name = tags.get("name", "").strip()
                    
                    if not name or name in seen_names:
                        continue
                    
                    # Skip if name contains exclude keywords
                    name_lower = name.lower()
                    if any(keyword in name_lower for keyword in exclude_keywords):
                        continue
                    
                    # Check if it's actually a tourist attraction
                    tourism_type = tags.get("tourism", "")
                    historic_type = tags.get("historic", "")
                    leisure_type = tags.get("leisure", "")
                    amenity_type = tags.get("amenity", "")
                    natural_type = tags.get("natural", "")
                    sport_type = tags.get("sport", "")
                    boundary_type = tags.get("boundary", "")
                    highway_type = tags.get("highway", "")
                    
                    # Validate it's a tourist attraction
                    is_tourist_attraction = False
                    
                    # 1. ZOOS
                    if tourism_type == "zoo":
                        is_tourist_attraction = True
                    
                    # 2. ART GALLERIES
                    elif tourism_type == "gallery" or amenity_type == "arts_centre":
                        is_tourist_attraction = True
                    
                    # 3. NATIONAL PARKS & NATURE RESERVES
                    elif leisure_type == "nature_reserve" or boundary_type == "national_park":
                        is_tourist_attraction = True
                    
                    # 4. BEACHES
                    elif natural_type == "beach" or leisure_type == "beach_resort":
                        is_tourist_attraction = True
                    
                    # 5. HIKING TRAILS & PEAKS
                    elif natural_type in ["peak", "volcano"] or sport_type == "hiking" or leisure_type == "track":
                        is_tourist_attraction = True
                    
                    # 6. VIEWPOINTS
                    elif tourism_type == "viewpoint":
                        is_tourist_attraction = True
                    
                    # 7. ADVENTURE SPOTS
                    elif tourism_type == "theme_park" or leisure_type in ["adult_gaming_centre", "water_park"]:
                        is_tourist_attraction = True
                    elif sport_type in ["climbing", "paragliding", "rafting", "canoeing", "kayaking", "surfing", "diving", "skydiving"]:
                        is_tourist_attraction = True
                    
                    # 8. TEMPLES, CHURCHES, MOSQUES, SHRINES
                    elif amenity_type == "place_of_worship":
                        is_tourist_attraction = True
                    elif historic_type in ["temple", "church", "mosque", "shrine", "monastery", "abbey", "cathedral", "basilica"]:
                        is_tourist_attraction = True
                    
                    # 9. FAMOUS STREETS (notable streets with names - filter by length and significance)
                    elif highway_type and name and len(name) > 5:
                        # Only include if it's a significant street (not just any residential street)
                        # Check if it has historic/tourism tag OR is a major road type
                        if historic_type or tourism_type or highway_type in ["primary", "secondary", "tertiary", "pedestrian"]:
                            is_tourist_attraction = True
                    
                    # 10. OTHER TOURIST ATTRACTIONS
                    elif tourism_type in ["attraction", "museum", "artwork"]:
                        is_tourist_attraction = True
                    elif historic_type in ["monument", "castle", "palace", "tower", "ruins", "tomb", "fort", "memorial", "archaeological_site"]:
                        is_tourist_attraction = True
                    elif leisure_type in ["park", "stadium", "golf_course", "marina"]:
                        is_tourist_attraction = True
                    elif amenity_type in ["theatre", "cinema", "library", "planetarium"]:
                        is_tourist_attraction = True
                    
                    # Exclude certain types that aren't real attractions
                    excluded_tourism_types = ['information', 'hotel', 'hostel', 'apartment', 'guest_house']
                    if tourism_type in excluded_tourism_types:
                        continue
                    
                    excluded_amenities = ['restaurant', 'cafe', 'fast_food', 'pharmacy', 'bank', 'atm', 'hospital', 'clinic', 'school', 'university']
                    if amenity_type in excluded_amenities and not is_tourist_attraction:
                        continue
                    
                    if is_tourist_attraction:
                        # Normalize name for comparison
                        name_lower = name.lower()
                        if name_lower not in seen_names:
                            places.append(name)
                            seen_names.add(name_lower)
                            
                            if len(places) >= 20:  # Increased to 20
                                break
        
        # If we have places, return them (up to 20)
        if places:
            places_list = "\n".join(places[:20])  # Limit to 20 places
            return f"In {place_name} these are the places you can go,\n\n{places_list}"
        else:
            # If no places found, try a broader search
            return f"Could not find specific tourist attractions for {place_name}. The place might exist, but no tourist attractions were found in the area."
        
    except requests.exceptions.RequestException as e:
        return f"Error fetching places data: {str(e)}"
    except Exception as e:
        return f"Error in places agent: {str(e)}"

