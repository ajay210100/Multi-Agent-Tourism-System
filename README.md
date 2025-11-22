# Multi-Agent Tourism System

A multi-agent system for tourism planning that provides weather information and tourist attraction suggestions for any place.

## Architecture

- **Parent Agent**: Tourism AI Agent (orchestrates the system)
- **Child Agent 1**: Weather Agent (checks current/forecast weather using Open-Meteo API)
- **Child Agent 2**: Places Agent (suggests up to 5 tourist attractions using Overpass API)

## Features

- Get current weather and forecast for any place
- Get up to 5 tourist attractions for any location
- Handles queries about weather, places, or both
- Error handling for non-existent places

## APIs Used

1. **Nominatim API** (Geocoding): https://nominatim.openstreetmap.org/search
   - Converts place names to coordinates

2. **Open-Meteo API** (Weather): https://api.open-meteo.com/v1/forecast
   - Provides current temperature and precipitation probability

3. **Overpass API** (Places): https://overpass-api.de/api/interpreter
   - Finds tourist attractions, monuments, parks, and other points of interest

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

**No API keys required!** The system uses only free, open-source APIs.

## Usage

### Web Interface (Recommended)

Run the Flask web server:
```bash
python app.py
```

Then open your browser and navigate to:
```
http://localhost:5000
```

The web interface provides a modern, user-friendly way to interact with the tourism system.

### Command Line Interface

Alternatively, run the command-line version:
```bash
python main.py
```

### Example Queries

1. **Places only:**
   - Input: "I'm going to go to Bangalore, let's plan my trip."
   - Output: List of tourist attractions

2. **Weather only:**
   - Input: "I'm going to go to Bangalore, what is the temperature there"
   - Output: Current temperature and precipitation probability

3. **Both weather and places:**
   - Input: "I'm going to go to Bangalore, what is the temperature there? And what are the places I can visit?"
   - Output: Weather information followed by list of tourist attractions

## Project Structure

```
.
├── app.py               # Flask backend API server
├── main.py              # Command-line interface
├── tourism_agent.py     # Parent Tourism AI Agent
├── tools.py             # Weather and Places agent tools
├── static/              # Frontend files
│   ├── index.html      # Main HTML page
│   ├── styles.css      # Styling
│   └── script.js        # Frontend JavaScript
├── requirements.txt     # Python dependencies
├── Procfile            # Deployment configuration (Heroku/Railway)
├── runtime.txt         # Python version specification
└── README.md           # This file
```

## Error Handling

The system handles non-existent places gracefully. If a place cannot be found:
- The geocoding service will return None
- The agents will respond: "I don't know if this place exists: [place_name]"

## Deployment

### Deploy to Heroku

1. Install Heroku CLI and login:
```bash
heroku login
```

2. Create a new Heroku app:
```bash
heroku create your-app-name
```

3. Deploy:
```bash
git push heroku main
```

4. Open your app:
```bash
heroku open
```

### Deploy to Railway

1. Install Railway CLI:
```bash
npm i -g @railway/cli
```

2. Login and initialize:
```bash
railway login
railway init
```

3. Deploy:
```bash
railway up
```

### Deploy to Render

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python app.py`
5. Deploy!

### Environment Variables

No environment variables are required! The system uses only free APIs.

However, if you want to customize the port, you can set:
```bash
PORT=5000  # Default is 5000
```

## Notes

- **100% Free** - No paid AI services required. Uses only free, open-source APIs.
- The parent agent uses rule-based logic to orchestrate child agents
- All place and weather data comes from open-source APIs (no AI knowledge used for data)
- The system respects API rate limits and includes proper error handling
- Uses Nominatim, Open-Meteo, and Overpass APIs as specified
- Modern, responsive web interface included

