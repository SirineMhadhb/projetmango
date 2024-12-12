import unittest
from app import app, mongo

class FlaskTestCase(unittest.TestCase):

    # Set up test environment
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.app.testing = True
        
    # Test to check the /get_abonne route
  
    def test_get_abonne(self):
        response = self.app.get('/getabonne')  # Update the route name here
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('abonnes', json_data)
    # Test invalid ObjectId for get_abonne/<id>
    def test_get_abonne_invalid_id(self):
        response = self.app.get('/get_abonne/invalid_id')
        self.assertEqual(response.status_code, 400)
        json_data = response.get_json()
        self.assertIn('error', json_data)

    # Test valid ObjectId for get_abonne/<id>
    def test_get_abonne_valid_id(self):
        # Insert a test abonne into the DB
        abonne = {
            "nom": "Test",
            "prenom": "User",
            "adresse": "123 Test Street",
            "date_inscription": "2024-12-11"
        }
        abonne_id = mongo.db.abonnes.insert_one(abonne).inserted_id
        response = self.app.get(f'/get_abonne/{str(abonne_id)}')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['nom'], 'Test')
        self.assertEqual(json_data['prenom'], 'User')

    # Test POST to add_abonne
    def test_add_abonne(self):
        new_abonne = {
            "nom": "John",
            "prenom": "Doe",
            "adresse": "456 Test Lane",
            "date_inscription": "2024-12-11"
        }
        response = self.app.post('/add_abonne', json=new_abonne)
        self.assertEqual(response.status_code, 201)
        json_data = response.get_json()
        self.assertIn("message", json_data)

    # Test PUT to update an abonne
    def test_update_abonne(self):
        abonne = {
            "nom": "Jane",
            "prenom": "Doe",
            "adresse": "789 Update Ave",
            "date_inscription": "2024-12-11"
        }
        abonne_id = mongo.db.abonnes.insert_one(abonne).inserted_id
        updated_abonne = {
            "nom": "Updated Jane",
            "prenom": "Updated Doe",
            "adresse": "789 Updated Ave",
            "date_inscription": "2024-12-11"
        }
        response = self.app.put(f'/update_abonne/{str(abonne_id)}', json=updated_abonne)
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn("message", json_data)

    # Test DELETE to delete an abonne
    def test_delete_abonne(self):
        abonne = {
            "nom": "Delete",
            "prenom": "User",
            "adresse": "999 Delete St",
            "date_inscription": "2024-12-11"
        }
        abonne_id = mongo.db.abonnes.insert_one(abonne).inserted_id
        response = self.app.delete(f'/delete_abonne/{str(abonne_id)}')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn("message", json_data)

if __name__ == '__main__':
    unittest.main()
