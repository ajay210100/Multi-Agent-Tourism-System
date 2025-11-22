"""
Parent Tourism AI Agent that orchestrates the multi-agent system.
Coordinates Weather Agent and Places Agent based on user queries.
Uses rule-based logic (no paid AI services).
"""
import re
from tools import weather_agent, places_agent


class TourismAgent:
    """
    Parent agent that orchestrates weather and places agents.
    Uses rule-based logic to determine which agents to call.
    """
    
    def __init__(self):
        """Initialize the Tourism Agent."""
        pass
    
    def extract_place_name(self, user_input: str) -> str:
        """
        Extract place name from user input.
        Looks for patterns like "going to [place]", "visit [place]", etc.
        Improved to handle lowercase place names like "mysore", "udupi".
        
        Args:
            user_input: User's query
            
        Returns:
            Extracted place name or empty string
        """
        # Common patterns for place names - case insensitive, more flexible
        patterns = [
            r"going to go to ([A-Za-z][A-Za-z\s]+?)(?:,|\.|$|\?|what|where|let|plan|trip)",  # "going to go to Mysore"
            r"going to ([A-Za-z][A-Za-z\s]+?)(?:,|\.|$|\?|what|where|let|plan|trip)",         # "going to mysore"
            r"visit ([A-Za-z][A-Za-z\s]+?)(?:,|\.|$|\?|what|where|let|plan|trip)",            # "visit Paris"
            r"in ([A-Za-z][A-Za-z\s]+?)(?:,|\.|$|\?|what|where|let|plan|trip)",               # "in Bangalore"
            r"to ([A-Za-z][A-Za-z\s]+?)(?:,|\.|$|\?|what|where|let|plan|trip)",               # "to Paris"
            r"from ([A-Za-z][A-Za-z\s]+?)(?:,|\.|$|\?|what|where|let|plan|trip)",             # "from Mysore"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                place = match.group(1).strip()
                # Remove trailing common words that might be part of the sentence
                place = re.sub(r'\s+(what|where|when|how|let|plan|trip|from|to|going|visit).*$', '', place, flags=re.IGNORECASE)
                # Clean up common articles
                place = re.sub(r'^\s*(?:the|a|an)\s+', '', place, flags=re.IGNORECASE).strip()
                # Capitalize first letter of each word for better matching
                place = ' '.join(word.capitalize() for word in place.split())
                if place and len(place) > 2:
                    return place
        
        # Fallback: try to find any capitalized or significant words (place names)
        words = user_input.split()
        place_words = []
        skip_words = {'i', 'i\'m', 'let\'s', 'let', 'going', 'to', 'go', 'visit', 'from', 'in', 'the', 'a', 'an', 'what', 'where', 'when', 'how', 'plan', 'trip', 'is', 'are', 'there', 'and', 'or', 'but'}
        
        for i, w in enumerate(words):
            w_clean = w.strip('.,!?;:').lower()
            # Skip common words
            if w_clean in skip_words:
                continue
            # If word is capitalized or is a significant word (longer than 3 chars), it might be a place
            if (w and w[0].isupper()) or (len(w_clean) > 3 and w_clean not in skip_words):
                place_words.append(w.strip('.,!?;:'))
                # If next word is also significant, include it
                if i + 1 < len(words):
                    next_w = words[i + 1].strip('.,!?;:').lower()
                    if next_w not in skip_words and (len(next_w) > 2 or words[i + 1][0].isupper()):
                        place_words.append(words[i + 1].strip('.,!?;:'))
                        break
        
        if place_words:
            place = ' '.join(place_words)
            # Capitalize properly
            place = ' '.join(word.capitalize() for word in place.split())
            return place
        
        return ""
    
    def determine_intent(self, user_input: str) -> dict:
        """
        Determine what the user is asking for.
        
        Args:
            user_input: User's query
            
        Returns:
            Dictionary with 'weather' and 'places' boolean flags
        """
        user_lower = user_input.lower()
        
        # Weather keywords
        weather_keywords = ['temperature', 'temp', 'weather', 'rain', 'precipitation', 
                           'forecast', 'climate', 'hot', 'cold', 'sunny', 'cloudy']
        wants_weather = any(keyword in user_lower for keyword in weather_keywords)
        
        # Places keywords
        places_keywords = ['places', 'attractions', 'visit', 'see', 'tourist', 
                          'sightseeing', 'plan', 'trip', 'go', 'explore']
        wants_places = any(keyword in user_lower for keyword in places_keywords)
        
        # If neither is explicitly mentioned but "plan my trip" or similar, assume places
        if not wants_weather and not wants_places:
            if any(phrase in user_lower for phrase in ['plan', 'trip', 'visit', 'go to']):
                wants_places = True
        
        # If both are mentioned or neither, check for "and" or "both"
        if 'and' in user_lower or 'both' in user_lower:
            if wants_weather or wants_places:
                return {'weather': True, 'places': True}
        
        return {'weather': wants_weather, 'places': wants_places}
    
    def process_query(self, user_input: str) -> str:
        """
        Process user query and return response.
        ALWAYS returns both weather and places information.
        
        Args:
            user_input: User's query about a place
            
        Returns:
            Agent's response with both weather and places
        """
        try:
            # Extract place name
            place_name = self.extract_place_name(user_input)
            
            if not place_name:
                return "I couldn't identify the place name in your query. Please mention the place you want to visit (e.g., 'I'm going to Bangalore')."
            
            # ALWAYS call both agents
            weather_response = weather_agent(place_name)
            places_response = places_agent(place_name)
            
            # Combine responses - always include both
            weather_text = weather_response
            places_text = places_response
            
            # Extract just the places list from places_text
            if "these are the places you can go" in places_text.lower():
                # Find the part after "these are the places you can go"
                parts = re.split(r"these are the places you can go", places_text, flags=re.IGNORECASE)
                if len(parts) > 1:
                    places_list = parts[1].strip()
                    # Remove leading comma if present
                    if places_list.startswith(","):
                        places_list = places_list[1:].strip()
                    # Ensure it starts with newline for formatting
                    if not places_list.startswith("\n"):
                        places_list = "\n" + places_list
                    return f"{weather_text} And these are the places you can go:{places_list}"
                else:
                    return f"{weather_text} {places_text}"
            else:
                return f"{weather_text} {places_text}"
                
        except Exception as e:
            return f"Error processing query: {str(e)}"

