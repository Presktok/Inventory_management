import requests
import json

def test_inventory_api():
    base_url = 'http://localhost:5000/api'
    
    # Test creating an item
    create_data = {
        "name": "Test Item",
        "quantity": 10,
        "category": "Test",
        "price": 99.99
    }
    
    print("Testing create inventory item...")
    response = requests.post(f'{base_url}/inventory', json=create_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    print("\nTesting get inventory...")
    response = requests.get(f'{base_url}/inventory')
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    test_inventory_api() 