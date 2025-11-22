# test_crud.py (using built-in libraries)
import urllib.request
import urllib.parse
import json

BASE_URL = "http://localhost:5000"

def make_request(url, method='GET', data=None, headers=None):
    """Helper function to make HTTP requests"""
    if headers is None:
        headers = {}
    
    if data and method in ['POST', 'PUT']:
        data = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            return response.getcode(), json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))
    except Exception as e:
        return None, str(e)

def get_auth_token():
    """Get JWT token for testing protected routes"""
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    status, data = make_request(f"{BASE_URL}/admin/login", 'POST', login_data)
    if status == 200:
        return data['access_token']
    return None

def test_all_operations():
    print("TESTING ALL CRUD OPERATIONS")
    print("=" * 50)
    
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    # 1. Test GET all NGOs
    print("1. Testing GET all NGOs...")
    status, data = make_request(f"{BASE_URL}/api/ngos")
    if status == 200:
        print(f"SUCCESS: Found {data['count']} NGOs")
        ngo_count = data['count']
    else:
        print(f"FAILED: {status}")
        return
    
    # 2. Test GET single NGO
    print("2. Testing GET single NGO...")
    status, data = make_request(f"{BASE_URL}/api/ngos/1")
    if status == 200:
        print("SUCCESS: Retrieved NGO details")
        print(f"NGO Name: {data.get('name', 'N/A')}")
    else:
        print(f"FAILED: {status}")
    
    # 3. Test SEARCH
    print("3. Testing SEARCH...")
    search_url = f"{BASE_URL}/api/ngos/search?q=education"
    status, data = make_request(search_url)
    if status == 200:
        print(f"SUCCESS: Found {data['count']} results for 'education'")
        if data['count'] > 0:
            print(f"First result: {data['data'][0]['name']}")
    else:
        print(f"FAILED: {status}")
    
    # 4. Test categories
    print("4. Testing GET categories...")
    status, data = make_request(f"{BASE_URL}/api/categories")
    if status == 200:
        print(f"SUCCESS: Found {data['count']} categories")
    else:
        print(f"FAILED: {status}")
    
    # 5. Test FILTER by category
    print("5. Testing FILTER by category...")
    status, data = make_request(f"{BASE_URL}/api/categories/1/ngos")
    if status == 200:
        print(f"SUCCESS: Found {data['count']} NGOs in category 1")
    else:
        print(f"FAILED: {status}")
    
    # 6. Test CREATE NGO (if we have auth)
    if token:
        print("6. Testing CREATE NGO...")
        new_ngo = {
            "name": "Test NGO CRUD",
            "description": "This is a test NGO for CRUD operations",
            "location_id": 1,
            "category_id": 1,
            "contact": "+1234567890",
            "email": "test@example.com"
        }
        status, data = make_request(f"{BASE_URL}/api/ngos", 'POST', new_ngo, headers)
        if status == 201:
            test_ngo_id = data['ngo_id']
            print(f"SUCCESS: Created NGO with ID {test_ngo_id}")
            
            # 7. Test UPDATE NGO
            print("7. Testing UPDATE NGO...")
            update_data = {
                "description": "Updated description for test NGO",
                "contact": "+0987654321"
            }
            status, data = make_request(f"{BASE_URL}/api/ngos/{test_ngo_id}", 'PUT', update_data, headers)
            if status == 200:
                print("SUCCESS: Updated NGO")
            else:
                print(f"FAILED: {status}")
            
            # 8. Test DELETE NGO
            print("8. Testing DELETE NGO...")
            status, data = make_request(f"{BASE_URL}/api/ngos/{test_ngo_id}", 'DELETE', headers=headers)
            if status == 200:
                print("SUCCESS: Deleted NGO")
            else:
                print(f"FAILED: {status}")
        else:
            print(f"FAILED to create NGO: {status}")
    else:
        print("6.SKIPPED: No auth token for CREATE/UPDATE/DELETE tests")
        print("Make sure admin user exists: username='admin', password='admin123'")
    
    print("\nCRUD Testing Complete!")
    print("\nAvailable Endpoints Summary:")
    print("   GET  /api/ngos              - List all NGOs")
    print("   GET  /api/ngos/<id>         - Get NGO details") 
    print("   GET  /api/ngos/search?q=... - Search NGOs")
    print("   GET  /api/categories        - List categories")
    print("   POST /api/ngos              - Create NGO (auth required)")
    print("   PUT  /api/ngos/<id>         - Update NGO (auth required)")
    print("   DELETE /api/ngos/<id>       - Delete NGO (auth required)")

if __name__ == "__main__":
    test_all_operations()