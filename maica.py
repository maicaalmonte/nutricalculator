from flask import Flask, render_template, request, jsonify
import requests
import pandas as pd
import os
import time

# Initialize Flask app with template folder explicitly set
app = Flask(__name__, template_folder='templates')

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

# Flask Routes
@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Error rendering template: {e}")
        return "Template not found. Ensure the 'templates/index.html' file exists.", 500

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    try:
        # Validate inputs
        page = int(request.form.get('page', 1))
        limit = int(request.form.get('limit', 100))
        max_pages = int(request.form.get('max_pages', 10))
        if page < 1 or limit < 1 or max_pages < 1:
            return jsonify({'status': 'error', 'message': 'Page, limit, and max_pages must be positive integers.'}), 400

        # Fetch data from the OpenFoodFacts API
        products_data = fetch_all_food_data(limit=limit, max_pages=max_pages)

        if not products_data:
            return jsonify({'status': 'error', 'message': 'No products were fetched. Please try again.'})

        # Extract and process the nutritional data
        products_df = extract_nutritional_data(products_data)
        data_json = products_df.to_dict(orient='records')  # Convert DataFrame to a list of dictionaries

        return jsonify({'status': 'success', 'data': data_json})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/fetch_news', methods=['GET'])
def fetch_news():
    try:
        api_key = "pub_63226fb5b460b34f9a0c3a06124eb21cf3260"  # Replace with your actual NewsData.io API key
        query = request.args.get('query', '')  # Optional query parameter
        news_data = fetch_news_articles(api_key, query)
        return jsonify({'status': 'success', 'articles': news_data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)