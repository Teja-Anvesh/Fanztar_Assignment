from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# Define the price for each component
prices = {
    "A": 10.28, "B": 24.07, "C": 33.30,
    "D": 25.94, "E": 32.39, "F": 18.77,
    "G": 15.13, "H": 20.00, "I": 42.31,
    "J": 45.00, "K": 45.00, "L": 30.00
}

# Define the valid combinations of components
valid_combinations = {
    "Screen": ["A", "B", "C"],
    "Camera": ["D", "E"],
    "Port": ["F", "G", "H"],
    "OS": ["I", "J"],
    "Body": ["K", "L"]
}

def calculate_total(components):
    total = 0
    parts = []
    for component in components:
        if component in prices:
            total += prices[component]
            parts.append(get_part_name(component))
        else:
            return None, None  # Invalid component code
    return total, parts

def get_part_name(component):
    parts_map = {
        "A": "LED Screen", "B": "OLED Screen", "C": "AMOLED Screen",
        "D": "Wide-Angle Camera", "E": "Ultra-Wide-Angle Camera",
        "F": "USB-C Port", "G": "Micro-USB Port", "H": "Lightning Port",
        "I": "Android OS", "J": "iOS OS", "K": "Metallic Body", "L": "Plastic Body"
    }
    return parts_map.get(component, "Unknown Part")

def is_valid_order(components):
    # Check if all required part types are present in the components
    required_part_types = valid_combinations.keys()
    provided_part_types = set()

    for component in components:
        for part_type, valid_codes in valid_combinations.items():
            if component in valid_codes:
                provided_part_types.add(part_type)

    return required_part_types == provided_part_types

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    if not data or 'components' not in data:
        return jsonify({"error": "Invalid request format"}), 400

    components = data['components']
    if not components:
        return jsonify({"error": "No components provided"}), 400
    
    if not is_valid_order(components):
        return jsonify({"error": "Invalid combination of components"}), 400

    total, parts = calculate_total(components)
    if total is None:
        return jsonify({"error": "Invalid component code"}), 400
    
    order_id = str(uuid.uuid4())
    
    response = {
        "order_id": order_id,
        "total": total,
        "parts": parts
    }
    
    return jsonify(response), 201

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run(debug=True, port=8000)
