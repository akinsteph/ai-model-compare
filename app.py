from flask import Flask, render_template, jsonify, request
import json
from datetime import datetime
import threading
import time
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from services.price_fetcher import PriceFetcher

app = Flask(__name__)
price_fetcher = PriceFetcher()

# Rate limiter configuration
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day"],
    storage_uri="memory://"
)

# Configuration
app.config['GA_TRACKING_ID'] = 'YOUR-GA-TRACKING-ID'  # Replace with your Google Analytics tracking ID

def load_stats():
    try:
        with open('data/stats.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        stats = {"visit_count": 0, "api_calls": 0, "last_updated": None}
        save_stats(stats)
        return stats

def save_stats(stats):
    with open('data/stats.json', 'w') as f:
        json.dump(stats, f, indent=4)

def increment_stat(stat_name):
    stats = load_stats()
    stats[stat_name] += 1
    stats['last_updated'] = datetime.now().isoformat()
    save_stats(stats)
    return stats[stat_name]

def load_ai_models():
    with open('data/models.json', 'r') as f:
        return json.load(f)

def load_current_pricing():
    try:
        with open('data/current_pricing.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def update_pricing_background():
    while True:
        try:
            pricing = price_fetcher.fetch_all_pricing()
            price_fetcher.save_pricing(pricing)
            print(f"Pricing updated at {datetime.now()}")
            time.sleep(3600)  # Update every hour
        except Exception as e:
            print(f"Error updating pricing: {e}")
            time.sleep(300)  # Retry after 5 minutes on error

@app.route('/')
def index():
    visit_count = increment_stat('visit_count')
    stats = load_stats()
    
    models = load_ai_models()
    current_pricing = load_current_pricing()
    return render_template('index.html', 
                         models=models, 
                         current_pricing=current_pricing,
                         last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                         visit_count=visit_count,
                         api_calls=stats['api_calls'],
                         ga_id=app.config['GA_TRACKING_ID'])

@app.route('/api/pricing')
@limiter.limit("60 per minute")
def get_pricing():
    api_calls = increment_stat('api_calls')
    current_pricing = load_current_pricing()
    return jsonify(current_pricing)

@app.route('/api/docs')
def api_docs():
    return render_template('api_docs.html')

@app.route('/api/refresh-pricing')
@limiter.limit("1 per minute")
def refresh_pricing():
    try:
        pricing = price_fetcher.fetch_all_pricing()
        price_fetcher.save_pricing(pricing)
        return jsonify({"status": "success", "data": pricing})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Start background pricing update thread
    pricing_thread = threading.Thread(target=update_pricing_background, daemon=True)
    pricing_thread.start()
    
    app.run(debug=True)
