from flask import Flask, request, jsonify
from utils.data_handler import read_data, write_data 

app = Flask(__name__)

data_file_path = 'data/airbnb.json'

#initial data
listings_data = read_data(data_file_path)

#GET Endpoints
@app.route('/listings', methods=['GET'])
def get_all_listings():
    return jsonify(listings_data)

#Based on Id , records are extracted
@app.route('/listings/<int:listing_id>', methods=['GET'])
def get_listing_by_id(listing_id):
    listing = next((item for item in listings_data if item['id'] == listing_id), None)
    if listing:
        return jsonify(listing)
    return jsonify({'error': 'Listing not found'}), 404

#Based on query , records are given
# Example: /listings?price_gt=500&neighbor=ABC
@app.route('/listings', methods=['GET'])
def get_listings_by_query():
    query_params = request.args
    filtered_listings = filter_listings(query_params)
    return jsonify(filtered_listings)

#Based on filters, ecords are retreived
def filter_listings(query_params):
    filtered_listings = listings_data
    for key, value in query_params.items():
        filtered_listings = [item for item in filtered_listings if str(item.get(key)) == value]
    return filtered_listings

# POST Endpoint
@app.route('/listings', methods=['POST'])
def create_listing():
    new_listing = request.json
    new_listing['id'] = len(listings_data) + 1
    listings_data.append(new_listing)
    write_data(listings_data, data_file_path)
    return jsonify(new_listing), 201

@app.route('/listing/search', methods=['POST'])
def search_listings():
    search_terms = request.json
    search_results = []
    for term in search_terms:
        search_results.extend([item for item in listings_data if term.lower() in item['name'].lower()])
    return jsonify(search_results)

#PATCH Endpoint
@app.route('/listings/<int:listing_id>', methods=['PATCH'])
def update_listing(listing_id):
    listing = next((item for item in listings_data if item['id'] == listing_id), None)
    if listing:
        updated_data = request.json
        listing.update(updated_data)
        write_data(listings_data, data_file_path)
        return jsonify(listing)
    return jsonify({'error': 'Listing not found'}), 404

#DELETE Endpoint
@app.route('/listings/<int:listing_id>', methods=['DELETE'])
def delete_listing(listing_id):
    global listings_data
    listings_data = [item for item in listings_data if item['id'] != listing_id]
    write_data(listings_data, data_file_path)
    return jsonify({'message': 'Listing deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
