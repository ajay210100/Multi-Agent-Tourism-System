"""
Flask backend API for the Multi-Agent Tourism System.
"""
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from tourism_agent import TourismAgent
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Initialize the Tourism Agent
agent = TourismAgent()

# Single-page HTML with inline CSS and JS
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multi-Agent Tourism System</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
        
        * { 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box; 
        }
        
        body {
            font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            min-height: 100vh;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            overflow-x: hidden;
        }
        
        /* Animated background elements */
        body::before {
            content: '';
            position: fixed;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="rgba(255,255,255,0.1)"/><circle cx="80" cy="40" r="1.5" fill="rgba(255,255,255,0.1)"/><circle cx="40" cy="80" r="1" fill="rgba(255,255,255,0.1)"/></svg>');
            animation: float 20s linear infinite;
            pointer-events: none;
            z-index: 0;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        @keyframes float {
            0% { transform: translate(0, 0) rotate(0deg); }
            100% { transform: translate(-50px, -50px) rotate(360deg); }
        }
        
        .container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 30px;
            box-shadow: 0 25px 80px rgba(0,0,0,0.2), 0 0 0 1px rgba(255,255,255,0.3);
            max-width: 900px;
            width: 100%;
            padding: 50px;
            position: relative;
            z-index: 1;
            animation: containerSlideIn 0.8s ease-out;
        }
        
        @keyframes containerSlideIn {
            from {
                opacity: 0;
                transform: translateY(30px) scale(0.95);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }
        
        h1 {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
            font-size: 2.5rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            animation: titleGlow 2s ease-in-out infinite alternate;
        }
        
        @keyframes titleGlow {
            from { filter: drop-shadow(0 0 5px rgba(102, 126, 234, 0.3)); }
            to { filter: drop-shadow(0 0 15px rgba(102, 126, 234, 0.6)); }
        }
        
        .subtitle {
            color: #666;
            margin-bottom: 40px;
            font-size: 1.1rem;
            font-weight: 400;
            animation: fadeInUp 0.8s ease-out 0.2s both;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .input-group {
            display: flex;
            gap: 15px;
            margin-bottom: 25px;
            animation: fadeInUp 0.8s ease-out 0.4s both;
        }
        
        input {
            flex: 1;
            padding: 18px 25px;
            border: 2px solid #e0e0e0;
            border-radius: 15px;
            font-size: 16px;
            font-family: 'Poppins', sans-serif;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            background: #fff;
        }
        
        input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
            transform: translateY(-2px);
        }
        
        input::placeholder {
            color: #999;
        }
        
        button {
            padding: 18px 35px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 15px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            position: relative;
            overflow: hidden;
        }
        
        button::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }
        
        button:hover::before {
            width: 300px;
            height: 300px;
        }
        
        button:hover { 
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
        }
        
        button:active {
            transform: translateY(-1px);
        }
        
        button:disabled { 
            opacity: 0.6; 
            cursor: not-allowed;
            transform: none;
        }
        
        button span {
            position: relative;
            z-index: 1;
        }
        .examples {
            margin: 25px 0;
            padding: 20px;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
            border-radius: 15px;
            border: 1px solid rgba(102, 126, 234, 0.1);
            animation: fadeInUp 0.8s ease-out 0.6s both;
        }
        
        .examples p { 
            margin-bottom: 15px; 
            color: #555; 
            font-size: 14px; 
            font-weight: 500;
        }
        
        .example-btn {
            background: white;
            color: #667eea;
            border: 2px solid #667eea;
            padding: 10px 20px;
            margin: 5px;
            font-size: 14px;
            border-radius: 10px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .example-btn::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: width 0.4s, height 0.4s;
            z-index: 0;
        }
        
        .example-btn:hover::before {
            width: 200px;
            height: 200px;
        }
        
        .example-btn span {
            position: relative;
            z-index: 1;
        }
        
        .example-btn:hover { 
            color: white;
            border-color: #667eea;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
        .response-container {
            margin-top: 40px;
            display: none;
            animation: fadeInUp 0.6s ease-out;
        }
        
        .weather-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 20px;
            margin-bottom: 25px;
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
            animation: weatherCardSlide 0.8s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .weather-card::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: shimmer 3s ease-in-out infinite;
        }
        
        @keyframes weatherCardSlide {
            from {
                opacity: 0;
                transform: translateX(-30px) scale(0.95);
            }
            to {
                opacity: 1;
                transform: translateX(0) scale(1);
            }
        }
        
        @keyframes shimmer {
            0%, 100% { transform: translate(0, 0) rotate(0deg); }
            50% { transform: translate(20px, 20px) rotate(180deg); }
        }
        .weather-header {
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 20px;
            position: relative;
            z-index: 1;
        }
        
        .weather-icon {
            font-size: 4rem;
            animation: weatherIconFloat 3s ease-in-out infinite;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
        }
        
        @keyframes weatherIconFloat {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-10px) rotate(5deg); }
        }
        
        .weather-info h3 {
            font-size: 1.8rem;
            margin-bottom: 5px;
            font-weight: 700;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        
        .weather-info p {
            opacity: 0.9;
            font-size: 0.95rem;
        }
        
        .weather-details {
            display: flex;
            gap: 20px;
            margin-top: 20px;
            flex-wrap: wrap;
            position: relative;
            z-index: 1;
        }
        
        .weather-item {
            display: flex;
            align-items: center;
            gap: 15px;
            background: rgba(255,255,255,0.25);
            backdrop-filter: blur(10px);
            padding: 15px 20px;
            border-radius: 15px;
            transition: all 0.3s ease;
            flex: 1;
            min-width: 150px;
        }
        
        .weather-item:hover {
            background: rgba(255,255,255,0.35);
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        }
        
        .weather-item span:first-child {
            font-size: 2rem;
            animation: iconPulse 2s ease-in-out infinite;
        }
        
        @keyframes iconPulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        .places-section {
            margin-top: 30px;
            animation: fadeInUp 0.6s ease-out 0.3s both;
        }
        
        .places-title {
            font-size: 1.5rem;
            color: #333;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 700;
        }
        
        .places-title span:first-child {
            font-size: 1.8rem;
            animation: locationPulse 2s ease-in-out infinite;
        }
        
        @keyframes locationPulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.2) rotate(5deg); }
        }
        
        .places-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 20px;
        }
        
        .place-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            padding: 25px 20px;
            border-radius: 20px;
            text-align: center;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            border: 2px solid transparent;
            position: relative;
            overflow: hidden;
            animation: cardSlideIn 0.6s ease-out both;
        }
        
        .place-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
            transition: left 0.5s;
        }
        
        .place-card:hover::before {
            left: 100%;
        }
        
        .place-card:nth-child(1) { animation-delay: 0.1s; }
        .place-card:nth-child(2) { animation-delay: 0.2s; }
        .place-card:nth-child(3) { animation-delay: 0.3s; }
        .place-card:nth-child(4) { animation-delay: 0.4s; }
        .place-card:nth-child(5) { animation-delay: 0.5s; }
        .place-card:nth-child(n+6) { animation-delay: 0.6s; }
        
        @keyframes cardSlideIn {
            from {
                opacity: 0;
                transform: translateY(20px) scale(0.9);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }
        
        .place-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 12px 30px rgba(102, 126, 234, 0.3);
            border-color: #667eea;
        }
        
        .place-icon {
            font-size: 3rem;
            margin-bottom: 15px;
            display: inline-block;
            transition: all 0.3s ease;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
        }
        
        .place-card:hover .place-icon {
            transform: scale(1.2) rotate(5deg);
            filter: drop-shadow(0 4px 8px rgba(102, 126, 234, 0.4));
        }
        
        .place-name {
            font-weight: 600;
            color: #333;
            font-size: 1rem;
            line-height: 1.4;
            position: relative;
            z-index: 1;
        }
        .response {
            margin-top: 30px;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            white-space: pre-wrap;
            line-height: 1.6;
        }
        .error {
            margin-top: 20px;
            padding: 20px;
            background: linear-gradient(135deg, #fee 0%, #fdd 100%);
            border-radius: 15px;
            border-left: 4px solid #f44;
            color: #c33;
            animation: shake 0.5s ease;
            box-shadow: 0 4px 15px rgba(244, 68, 68, 0.2);
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-10px); }
            75% { transform: translateX(10px); }
        }
        
        .loading {
            display: inline-block;
            width: 24px;
            height: 24px;
            border: 3px solid rgba(255,255,255,0.3);
            border-top: 3px solid white;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        footer {
            margin-top: 40px;
            text-align: center;
            color: #999;
            font-size: 13px;
            padding-top: 20px;
            border-top: 1px solid rgba(0,0,0,0.1);
            animation: fadeInUp 0.8s ease-out 0.8s both;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .container {
                padding: 30px 20px;
                border-radius: 20px;
            }
            
            h1 {
                font-size: 2rem;
            }
            
            .input-group {
                flex-direction: column;
            }
            
            button {
                width: 100%;
            }
            
            .places-grid {
                grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
                gap: 15px;
            }
            
            .weather-details {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌍 Multi-Agent Tourism System</h1>
        <p class="subtitle">Plan your trips with weather and attraction information</p>
        
        <div class="input-group">
            <input type="text" id="queryInput" placeholder="Enter your query (e.g., 'I'm going to go to Bangalore, let's plan my trip.')">
            <button id="submitBtn" onclick="processQuery()"><span>Search</span></button>
        </div>
        
        <div class="examples">
            <p><strong>Try these examples:</strong></p>
            <button class="example-btn" onclick="fillExample(0)"><span>Example 1</span></button>
            <button class="example-btn" onclick="fillExample(1)"><span>Example 2</span></button>
            <button class="example-btn" onclick="fillExample(2)"><span>Example 3</span></button>
        </div>
        
        <div id="responseContainer" class="response-container">
            <div id="weatherCard" style="display:none;"></div>
            <div id="placesSection" style="display:none;"></div>
        </div>
        <div id="error" style="display:none;" class="error"></div>
        
        <footer>Powered by Open-Meteo, Nominatim, and Overpass APIs</footer>
    </div>
    
    <script>
        const examples = [
            "I'm going to go to Bangalore, let's plan my trip.",
            "I'm going to Mysore, what is the temperature there",
            "I'm going to Udupi, what are the places I can visit?"
        ];
        
        function fillExample(i) {
            document.getElementById('queryInput').value = examples[i];
        }
        
        async function processQuery() {
            const input = document.getElementById('queryInput');
            const query = input.value.trim();
            const btn = document.getElementById('submitBtn');
            const container = document.getElementById('responseContainer');
            const errorDiv = document.getElementById('error');
            
            if (!query) {
                errorDiv.textContent = 'Please enter a query';
                errorDiv.style.display = 'block';
                container.style.display = 'none';
                return;
            }
            
            errorDiv.style.display = 'none';
            container.style.display = 'none';
            btn.disabled = true;
            btn.innerHTML = '<span class="loading"></span>';
            
            try {
                const res = await fetch('/api/query', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query })
                });
                
                const data = await res.json();
                
                if (data.success) {
                    displayResponse(data.response);
                } else {
                    errorDiv.textContent = data.error || 'An error occurred';
                    errorDiv.style.display = 'block';
                }
            } catch (err) {
                errorDiv.textContent = 'Network error: ' + err.message;
                errorDiv.style.display = 'block';
            } finally {
                btn.disabled = false;
                btn.innerHTML = '<span>Search</span>';
            }
        }
        
        function displayResponse(response) {
            console.log('Raw response:', response);
            const container = document.getElementById('responseContainer');
            const weatherCard = document.getElementById('weatherCard');
            const placesSection = document.getElementById('placesSection');
            
            // Reset
            weatherCard.style.display = 'none';
            placesSection.style.display = 'none';
            weatherCard.innerHTML = '';
            placesSection.innerHTML = '';
            
            // Parse weather information - fix regex for JavaScript
            let weatherMatch = null;
            // Try different patterns
            weatherMatch = response.match(/In ([^,]+) it's currently (\\d+)°C with a chance of (\\d+)% to rain/) ||
                          response.match(/In ([^,]+) it's currently (\\d+)°C/) ||
                          response.match(/currently (\\d+)°C/);
            
            console.log('Weather match:', weatherMatch);
            if (weatherMatch) {
                const place = weatherMatch[1].trim();
                const temp = weatherMatch[2];
                const rain = weatherMatch[3] || '0';
                const rainNum = parseInt(rain);
                const weatherIcon = rainNum > 50 ? '🌧️' : rainNum > 30 ? '⛅' : '☀️';
                
                weatherCard.innerHTML = `
                    <div class="weather-card">
                        <div class="weather-header">
                            <div class="weather-icon">${weatherIcon}</div>
                            <div class="weather-info">
                                <h3>${place}</h3>
                                <p>Current Weather</p>
                            </div>
                        </div>
                        <div class="weather-details">
                            <div class="weather-item">
                                <span>🌡️</span>
                                <div>
                                    <div style="font-size: 1.8rem; font-weight: bold;">${temp}°C</div>
                                    <div style="font-size: 0.9rem; opacity: 0.9;">Temperature</div>
                                </div>
                            </div>
                            <div class="weather-item">
                                <span>💧</span>
                                <div>
                                    <div style="font-size: 1.8rem; font-weight: bold;">${rain}%</div>
                                    <div style="font-size: 0.9rem; opacity: 0.9;">Rain Chance</div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                weatherCard.style.display = 'block';
            }
            
            // Parse places - simpler approach
            let places = [];
            if (response.includes('places you can go')) {
                const parts = response.split('places you can go');
                if (parts.length > 1) {
                    let placesText = parts[1];
                    // Clean up
                    placesText = placesText.replace(/^And\\s*:/, '').replace(/^,/, '').trim();
                    // Split by newlines - handle both \\n and actual newlines
                    const lines = placesText.split(/[\\n\\r]+/).filter(line => line.trim());
                    places = lines
                        .map(p => p.trim())
                        .filter(p => {
                            const trimmed = p.trim();
                            return trimmed.length > 2 
                                && !trimmed.toLowerCase().includes('in ')
                                && !trimmed.includes('°C') 
                                && !trimmed.toLowerCase().includes('and')
                                && !trimmed.match(/^In [A-Z]/)
                                && !trimmed.match(/^\\d+%/)
                                && !trimmed.toLowerCase().includes('temperature');
                        })
                        .slice(0, 20);
                }
            }
            console.log('Places found:', places);
                
                if (places.length > 0) {
                    // Extended icon set for all categories: National parks, Zoos, Art galleries, Beaches, 
                    // Hiking, Famous streets, Adventure spots, Temples/Churches/Mosques, Viewpoints
                    const placeIcons = [
                        '🏛️', '🏞️', '🏰', '🎭', '🎨', '🌳', '🎪', '🕌', '⛪', '🕍', 
                        '🏯', '🌊', '🏖️', '⛰️', '🌺', '🎡', '🎢', '🎠', '🏕️', '🏜️',
                        '🦁', '🐘', '🦒', '🎨', '🖼️', '🏛️', '⛰️', '🏔️', '🌋', '🏝️',
                        '🚶', '🥾', '🧗', '🪂', '🏄', '🏊', '🚣', '⛷️', '🏂', '🚴',
                        '🛤️', '🛣️', '🏛️', '⛩️', '🕉️', '☪️', '✡️', '☦️', '🕎', '🛕'
                    ];
                    let placesHTML = '<div class="places-section"><div class="places-title"><span>📍</span><span>Tourist Attractions</span></div>';
                    placesHTML += '<div class="places-grid">';
                    
                    places.forEach((place, index) => {
                        const icon = placeIcons[index % placeIcons.length];
                        placesHTML += `
                            <div class="place-card">
                                <div class="place-icon">${icon}</div>
                                <div class="place-name">${place.trim()}</div>
                            </div>
                        `;
                    });
                    
                    placesHTML += '</div>';
                    placesSection.innerHTML = placesHTML;
                    placesSection.style.display = 'block';
                }
            
            // Always show container, even if parsing failed
            container.style.display = 'block';
            
            // If no structured data found, show raw response as fallback
            if (!weatherMatch && places.length === 0) {
                // Remove any existing fallback
                const existingFallback = container.querySelector('.response-fallback');
                if (existingFallback) existingFallback.remove();
                
                const fallbackDiv = document.createElement('div');
                fallbackDiv.className = 'response response-fallback';
                fallbackDiv.textContent = response;
                container.appendChild(fallbackDiv);
            } else {
                // Remove fallback if we have structured data
                const existingFallback = container.querySelector('.response-fallback');
                if (existingFallback) existingFallback.remove();
            }
        }
        
        document.getElementById('queryInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                processQuery();
            }
        });
    </script>
</body>
</html>
'''


@app.route('/')
def index():
    """Serve the main HTML page."""
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/query', methods=['POST'])
def process_query():
    """
    API endpoint to process tourism queries.
    
    Expected JSON:
    {
        "query": "I'm going to go to Bangalore, let's plan my trip."
    }
    
    Returns:
    {
        "success": true/false,
        "response": "Agent response text",
        "error": "Error message if any"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing "query" field in request body'
            }), 400
        
        user_query = data['query'].strip()
        
        if not user_query:
            return jsonify({
                'success': False,
                'error': 'Query cannot be empty'
            }), 400
        
        # Process the query using the Tourism Agent
        response = agent.process_query(user_query)
        
        return jsonify({
            'success': True,
            'response': response
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'Multi-Agent Tourism System'
    })




if __name__ == '__main__':
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

