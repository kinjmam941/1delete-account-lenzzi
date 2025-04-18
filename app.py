from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# 🔐 Shopify credentials (update if needed)
SHOPIFY_ACCESS_TOKEN = "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"
SHOPIFY_STORE_URL = "https://m0dz2y-3z.myshopify.com"

# 🖥️ Simple test form (homepage)
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

# 🚫 Delete customer API (accepts form + JSON)
@app.route('/delete-customer', methods=['POST'])
def delete_customer():
    # Check for JSON or form data
    if request.is_json:
        customer_id = request.json.get('customer_id')
    else:
        customer_id = request.form.get('customer_id')

    if not customer_id:
        return jsonify({"message": "Missing customer_id"}), 400

    url = f"{SHOPIFY_STORE_URL}/admin/api/2024-04/customers/{customer_id}.json"
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        message = f"Customer {customer_id} deleted successfully"
    else:
        try:
            error = response.json()
            message = f"Failed to delete customer {customer_id}. Error: {error.get('message', 'Unknown error')}"
        except Exception:
            message = f"Failed to delete customer {customer_id}. Unknown error."

    # Return the message back to the frontend
    return render_template('result.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
