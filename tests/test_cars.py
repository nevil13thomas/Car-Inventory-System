import time

# Test that an owner can be created and a car associated with that owner can also be created successfully
def test_create_owner_and_car_success(client):
    print("\n[TEST] Creating a new owner...")
    owner_data = {"name": "Alice", "license_number": "ABC123"}
    r = client.post("/owners", json=owner_data)
    assert r.status_code == 201  # Expect HTTP 201 Created
    print("[PASS] Owner created successfully.")
    owner_id = r.json()["id"]  # Extract owner ID for use in car creation
    time.sleep(0.5)

    print("[TEST] Creating a new car linked to the owner...")
    car_data = {
        "color": "red",
        "make": "Toyota",
        "year": 2010,
        "picture": "http://example.com/car.png",
        "owner_id": owner_id
    }
    r = client.post("/cars", json=car_data)
    assert r.status_code == 201  # Expect HTTP 201 Created
    j = r.json()
    assert j["color"] == "red"
    assert j["owner"]["id"] == owner_id  # Verify correct owner association
    print("[PASS] Car created and linked to owner successfully.")
    time.sleep(0.5)

# Test that attempting to create a car with a non-existent owner returns 404
def test_create_car_missing_owner_returns_404(client):
    print("\n[TEST] Creating a car with non-existent owner...")
    car_data = {
        "color": "blue",
        "make": "Ford",
        "year": 2015,
        "picture": None,
        "owner_id": 999  # Non-existent owner
    }
    r = client.post("/cars", json=car_data)
    assert r.status_code == 404  # Expect HTTP 404 Not Found
    print("[PASS] Correctly returned 404 for missing owner.")
    time.sleep(0.5)

# Test the full get, update, and delete workflow for a car
def test_get_update_delete_flow(client):
    print("\n[TEST] Creating a new owner for workflow test...")
    r = client.post("/owners", json={"name": "Bob", "license_number": "XYZ999"})
    owner_id = r.json()["id"]
    print("[PASS] Owner created successfully.")
    time.sleep(0.5)

    print("[TEST] Creating a new car for the owner...")
    r = client.post("/cars", json={"color": "green", "make": "Honda", "year": 2012, "picture": "", "owner_id": owner_id})
    car_id = r.json()["id"]
    print("[PASS] Car created successfully.")
    time.sleep(0.5)

    print("[TEST] Retrieving the car and verifying make...")
    r = client.get(f"/cars/{car_id}")
    assert r.status_code == 200
    assert r.json()["make"] == "Honda"
    print("[PASS] Car retrieved and verified.")
    time.sleep(0.5)

    print("[TEST] Updating the car's color and year...")
    r = client.put(f"/cars/{car_id}", json={"color": "black", "year": 2013})
    assert r.status_code == 200
    assert r.json()["color"] == "black"
    print("[PASS] Car updated successfully.")
    time.sleep(0.5)

    print("[TEST] Deleting the car...")
    r = client.delete(f"/cars/{car_id}")
    assert r.status_code == 204
    print("[PASS] Car deleted successfully.")
    time.sleep(0.5)

    print("[TEST] Verifying the car no longer exists...")
    r = client.get(f"/cars/{car_id}")
    assert r.status_code == 404
    print("[PASS] Car deletion verified.")
