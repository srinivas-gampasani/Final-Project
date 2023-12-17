import unittest
import json
from app import app

class TestEndpoints(unittest.TestCase):
    def setUp(self):
        # Set up a test client
        self.app = app.test_client()
        self.app.testing = True
    
    # GET Endpoints
    def test_get_all_listings_success(self):
        response = self.app.get('/listings')
        self.assertEqual(response.status_code, 200)

    def test_get_listing_by_id_success(self):
        response = self.app.get('/listings/1')
        self.assertEqual(response.status_code, 200)
    
    def test_get_listing_by_id_not_found(self):
        response = self.app.get('/listings/1000')
        self.assertEqual(response.status_code, 404)

    def test_get_listings_by_query_success(self):
        response = self.app.get('/listings?price_gt=100')
        self.assertEqual(response.status_code, 200)

    # POST Endpoint
    def test_create_listing_success(self):
        new_listing = {
           "id": 3890,
           "name": "Jimmy John House84 · 1 bedroom · 2 beds · 1 bath",
           "host_id": 4567,
           "host_name": "John Lincon",
           "neighbourhood": 73456,
           "latitude": "56.26234",
           "longitude": "-67.73441",
           "room_type": "Entire home/apt",
           "price": 176,
           "minimum_nights": 7,
           "number_of_reviews": 667,
           "last_review": "2022-05-17",
           "availability_365": 245
        }
        response = self.app.post('/listings', data=json.dumps(new_listing), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_create_listing_missing_data(self):
        # Test with incomplete data
        incomplete_listing = {
            "name": "Incomplete Listing",
            "price": 150,
            "neighborhood": "Test Neighborhood",
        }
        response = self.app.post('/listings', data=json.dumps(incomplete_listing), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    # PATCH Endpoint
    def test_update_listing_success(self):
        listing_id = 1  # Assuming this ID exists in the test data
        updated_data = {"price": 200}
        response = self.app.patch(f'/listings/{listing_id}', data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_update_listing_not_found(self):
        response = self.app.patch('/listings/1000', data=json.dumps({"price": 200}), content_type='application/json')
        self.assertEqual(response.status_code, 404)
    
     # DELETE Endpoint
    def test_delete_listing_success(self):
        listing_id = 1  
        response = self.app.delete(f'/listings/{listing_id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_listing_not_found(self):
        response = self.app.delete('/listings/1000')
        self.assertEqual(response.status_code, 404)

if __name__ == '_main_':
    unittest.main()
