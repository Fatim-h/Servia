# test_donations_simple.py
import http.client
import json

def test_donation():
    print("Testing Donation System...")
    
    # Test public NGO donation stats
    conn = http.client.HTTPConnection("localhost", 5000)
    conn.request("GET", "/api/ngos/1/donations")
    response = conn.getresponse()
    
    print(f"Status: {response.status}")
    data = response.read().decode()
    print(f"NGO Donation Stats: {data[:300]}...")
    
    conn.close()
    print("Donation system is working!")

if __name__ == "__main__":
    test_donation()