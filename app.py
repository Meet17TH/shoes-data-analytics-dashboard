from flask import Flask, render_template, jsonify, request
import pandas as pd
from ml_models import load_data, perform_kmeans_clustering, get_elbow_data

app = Flask(__name__)

# Path to the cleaned CSV file
DATA_PATH = "cleaned_output.csv"

@app.route('/')
def home():
    # Renders the dashboard HTML page
    return render_template("dashboard.html")

@app.route('/api/discounts')
def get_avg_discount_per_brand():
    df = load_data(DATA_PATH)
    # Group by brand and compute mean discount
    brand_discounts = df.groupby("Brand")["Computed Discount %"].mean().sort_values(ascending=False)
    return jsonify(brand_discounts.to_dict())

@app.route('/api/top-products')
def get_top_products():
    df = load_data(DATA_PATH)
    # Get top 10 discounted products
    top_products = df.nlargest(10, "Computed Discount %")[[
        "Product Name", "Brand", "Price", "Original Price", "Computed Discount %"
    ]]
    return jsonify(top_products.to_dict(orient="records"))

@app.route('/api/price-distribution')
def get_price_distribution():
    df = load_data(DATA_PATH)
    # Define price bins
    bins = [0, 500, 1000, 2000, 3000, 5000, 10000, 20000, 50000]
    df['Price Range'] = pd.cut(df['Price'], bins)
    # Count products in each price range
    distribution = df['Price Range'].value_counts().sort_index()
    result = {
        f"{int(interval.left)}-{int(interval.right)}": int(count)
        for interval, count in distribution.items()
    }
    return jsonify(result)

@app.route('/api/kmeans')
def get_kmeans_result():
    k = int(request.args.get("k", 3))  # Default to 3 clusters
    df = load_data(DATA_PATH)
    clustered_df = perform_kmeans_clustering(df, n_clusters=k)
    return jsonify(clustered_df.to_dict(orient="records"))

@app.route('/api/elbow')
def get_elbow_result():
    df = load_data(DATA_PATH)
    elbow_data = get_elbow_data(df)
    return jsonify(elbow_data)

if __name__ == "__main__":
    # Start the Flask app on port 8000 (matches frontend requests)
    app.run(debug=True, port=8000)
