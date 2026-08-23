import requests
import json

def test_recipe_endpoints():
    # Define the base URL
    base_url = "http://localhost:8000"  # FastAPI default port
    
    # Test data for creating a recipe
    test_recipe = {
        "recipe_name": "Test Recipe",
        "recipe_content": "This is a test recipe with ingredients and instructions."
    }
    
    print("=== Testing Recipe Endpoints ===")
    
    # Test 1: Create a new recipe
    print("\n1. Testing POST /recipes")
    response = requests.post(f"{base_url}/recipes", json=test_recipe)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        created_recipe = response.json()
        print(f"Created Recipe: {json.dumps(created_recipe, indent=2)}")
        recipe_id = created_recipe.get('id', 1)  # Fallback to 1 if id not returned
    else:
        print(f"Error: {response.text}")
        recipe_id = 1  # Fallback for testing subsequent endpoints
    
    # Test 2: Get a specific recipe
    print("\n2. Testing GET /recipes/{recipe_id}")
    response = requests.get(f"{base_url}/recipes/{recipe_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Retrieved Recipe: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")
    
    # Test 3: Update a recipe
    print("\n3. Testing PUT /recipes/{recipe_id}")
    updated_recipe = {
        "recipe_name": "Updated Test Recipe",
        "recipe_content": "This is an updated test recipe."
    }
    response = requests.put(f"{base_url}/recipes/{recipe_id}", json=updated_recipe)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Updated Recipe: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")
    
    # Test 4: Get all recipes for a user
    print("\n4. Testing GET /recipes?user_id=1")
    user_id = 1  # Assuming user_id 1 exists
    response = requests.get(f"{base_url}/recipes?user_id={user_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        recipes = response.json()
        print(f"Found {len(recipes)} recipes for user {user_id}")
        print(f"Recipes: {json.dumps(recipes, indent=2)}")
    else:
        print(f"Error: {response.text}")
    
    # Test 5: Delete a recipe
    print("\n5. Testing DELETE /recipes/{recipe_id}")
    response = requests.delete(f"{base_url}/recipes/{recipe_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Deleted Recipe: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")
    
    print("\n=== Testing Complete ===")

if __name__ == "__main__":
    test_recipe_endpoints()
