from flask import Flask, render_template, request, jsonify
import requests
import pandas as pd
import os
import time
from googletrans import Translator
import redis
import json

# Initialize Flask app with template folder explicitly set
app = Flask(__name__, template_folder='public')

# Initialize Redis connection
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Initialize the translator
translator = Translator()

# Debug: Print the current working directory
print("Working directory:", os.getcwd())

# Function to fetch data from OpenFoodFacts API
def fetch_all_food_data(limit=100, max_pages=10):
    """
    Fetches product data across multiple pages from OpenFoodFacts API.
    """
    all_products = []
    for page in range(1, max_pages + 1):
        url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms=&search_simple=1&action=process&json=true&page={page}&page_size={limit}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            products = data.get('products', [])
            all_products.extend(products)
            # Break if fewer products are returned than requested (indicates end of data)
            if len(products) < limit:
                break
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            break
        time.sleep(1)  # Respect API rate limits
    return all_products

# Function to extract relevant data (nutritional values and other attributes)
def extract_nutritional_data(products_data):
    """
    Extracts relevant columns from the OpenFoodFacts product data
    """
    rows = []
    for product in products_data:
        # Extract product-level data
        row = {
            'product_name': product.get('product_name', 'N/A'),
            'ingredients_text': product.get('ingredients_text', 'N/A'),
            'brands': product.get('brands', 'N/A'),
            'quantity': product.get('quantity', 'N/A'),
            'code': product.get('code', 'N/A'),
        }

        # Flatten the nutritional data
        nutriments = product.get('nutriments', {})
        row.update({
            key: nutriments.get(key, 0) for key in [
                'energy-kcal_100g', 'fat_100g', 'carbohydrates_100g',
                'sugars_100g', 'proteins_100g', 'salt_100g',
                'fiber_100g', 'vitamin-a_100g', 'vitamin-c_100g',
                'calcium_100g', 'iron_100g', 'magnesium_100g',
                'potassium_100g', 'sodium_100g', 'zinc_100g',
                'phosphorus_100g', 'vitamin-d_100g', 'vitamin-e_100g',
                'vitamin-k_100g', 'folate_100g', 'vitamin-b12_100g',
                'vitamin-b6_100g', 'copper_100g', 'manganese_100g', 'selenium_100g'
            ]
        })
        rows.append(row)

    # Create DataFrame from the list of rows
    products_df = pd.DataFrame(rows)
    return products_df

# Function to fetch news articles using NewsData.io API
def fetch_news_articles(api_key, query=""):
    """
    Fetches news articles using the NewsData.io API.
    """
    url = f"https://newsdata.io/api/1/news?apikey={api_key}&q={query}&language=en"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('results', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

# Function to translate text using googletrans
def translate_text(text, dest_language):
    """
    Translates the given text to the specified destination language.
    """
    try:
        translated = translator.translate(text, dest=dest_language)
        return translated.text
    except Exception as e:
        print(f"Error translating text: {e}")
        return text

# Function to cache product data in Redis
def cache_data_in_redis(key, data, ttl=3600):
    """
    Caches the data in Redis with a time-to-live (TTL).
    """
    redis_client.setex(key, ttl, json.dumps(data))

# Function to retrieve cached data from Redis
def get_cached_data_from_redis(key):
    """
    Retrieves cached data from Redis if available.
    """
    cached_data = redis_client.get(key)
    if cached_data:
        return json.loads(cached_data)
    return None

# Flask Routes
@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Error rendering template: {e}")
        return "Template not found. Ensure the 'public/index.html' file exists.", 500

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    try:
        # Validate inputs
        page = int(request.form.get('page', 1))
        limit = int(request.form.get('limit', 100))
        max_pages = int(request.form.get('max_pages', 10))
        dest_language = request.form.get('language', 'en')  # Default to English

        if page < 1 or limit < 1 or max_pages < 1:
            return jsonify({'status': 'error', 'message': 'Page, limit, and max_pages must be positive integers.'}), 400

        cache_key = f"products_{page}_{limit}_{max_pages}_{dest_language}"
        cached_data = get_cached_data_from_redis(cache_key)
        if cached_data:
            return jsonify({'status': 'success', 'data': cached_data})

        # Fetch data from the OpenFoodFacts API
        products_data = fetch_all_food_data(limit=limit, max_pages=max_pages)

        if not products_data:
            return jsonify({'status': 'error', 'message': 'No products were fetched. Please try again.'})

        # Extract and process the nutritional data
        products_df = extract_nutritional_data(products_data)

        # Translate product names and ingredients
        products_df['product_name'] = products_df['product_name'].apply(lambda x: translate_text(x, dest_language))
        products_df['ingredients_text'] = products_df['ingredients_text'].apply(lambda x: translate_text(x, dest_language))

        data_json = products_df.to_dict(orient='records')  # Convert DataFrame to a list of dictionaries

        # Cache the data in Redis
        cache_data_in_redis(cache_key, data_json)

        return jsonify({'status': 'success', 'data': data_json})
    except Exception as e:
        print(f"Error in fetch_data: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/fetch_news', methods=['GET'])
def fetch_news():
    try:
        api_key = "pub_63226fb5b460b34f9a0c3a06124eb21cf3260"  # Replace with your actual NewsData.io API key
        query = request.args.get('query', '')  # Optional query parameter
        news_data = fetch_news_articles(api_key, query)
        return jsonify({'status': 'success', 'articles': news_data})
    except Exception as e:
        print(f"Error in fetch_news: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
