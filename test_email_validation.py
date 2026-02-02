"""
Test script to verify student email validation
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_student_registration():
    """Test student registration with valid and invalid emails"""
    
    # Test 1: Try to register with a valid student email from the database
    print("\n=== Test 1: Valid Student Email ===")
    valid_email = "abhinavs.23civil@kongu.edu"  # From the imported data
    
    # First send OTP
    print(f"Sending OTP to {valid_email}...")
    response = requests.post(f"{BASE_URL}/auth/send-otp", json={"email": valid_email})
    print(f"OTP Response: {response.status_code} - {response.json()}")
    
    if response.status_code == 200:
        # Get OTP from console (for testing)
        otp = input("Enter OTP from console: ")
        
        # Verify OTP
        print(f"Verifying OTP...")
        response = requests.post(f"{BASE_URL}/auth/verify-otp", json={"email": valid_email, "otp": otp})
        print(f"Verify Response: {response.status_code} - {response.json()}")
        
        if response.status_code == 200:
            # Register
            print(f"Registering user...")
            response = requests.post(f"{BASE_URL}/auth/register", json={
                "name": "Abhinav S",
                "email": valid_email,
                "password": "test123456",
                "department": "Civil Engineering",
                "role": "student"
            })
            print(f"Register Response: {response.status_code} - {response.json()}")
    
    # Test 2: Try to register with an invalid email
    print("\n=== Test 2: Invalid Student Email ===")
    invalid_email = "notastudent@example.com"
    
    # First send OTP
    print(f"Sending OTP to {invalid_email}...")
    response = requests.post(f"{BASE_URL}/auth/send-otp", json={"email": invalid_email})
    print(f"OTP Response: {response.status_code} - {response.json()}")
    
    if response.status_code == 200:
        # Get OTP from console (for testing)
        otp = input("Enter OTP from console: ")
        
        # Verify OTP
        print(f"Verifying OTP...")
        response = requests.post(f"{BASE_URL}/auth/verify-otp", json={"email": invalid_email, "otp": otp})
        print(f"Verify Response: {response.status_code} - {response.json()}")
        
        if response.status_code == 200:
            # Try to register (should fail)
            print(f"Attempting registration (should fail)...")
            response = requests.post(f"{BASE_URL}/auth/register", json={
                "name": "Invalid User",
                "email": invalid_email,
                "password": "test123456",
                "department": "Computer Science",
                "role": "student"
            })
            print(f"Register Response: {response.status_code} - {response.json()}")
    
def test_student_login():
    """Test student login with valid email"""
    print("\n=== Test 3: Login with Valid Student Email ===")
    valid_email = "abhinavs.23civil@kongu.edu"
    
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": valid_email,
        "password": "test123456",
        "role": "student"
    })
    print(f"Login Response: {response.status_code} - {response.json()}")

def test_event_manager():
    """Test event_manager role with student email"""
    print("\n=== Test 4: Event Manager Registration ===")
    valid_email = "abisheckr.23civil@kongu.edu"  # Another valid student email
    
    # Send OTP
    print(f"Sending OTP to {valid_email}...")
    response = requests.post(f"{BASE_URL}/auth/send-otp", json={"email": valid_email})
    print(f"OTP Response: {response.status_code} - {response.json()}")
    
    if response.status_code == 200:
        otp = input("Enter OTP from console: ")
        
        # Verify OTP
        response = requests.post(f"{BASE_URL}/auth/verify-otp", json={"email": valid_email, "otp": otp})
        print(f"Verify Response: {response.status_code} - {response.json()}")
        
        if response.status_code == 200:
            # Register as event_manager
            response = requests.post(f"{BASE_URL}/auth/register", json={
                "name": "Abisheck R",
                "email": valid_email,
                "password": "test123456",
                "department": "Civil Engineering",
                "role": "event_manager"
            })
            print(f"Register Response: {response.status_code} - {response.json()}")

if __name__ == "__main__":
    print("Student Email Validation Test")
    print("=" * 50)
    
    choice = input("\nChoose test:\n1. Student Registration\n2. Student Login\n3. Event Manager Registration\n4. All\nChoice: ")
    
    if choice == "1":
        test_student_registration()
    elif choice == "2":
        test_student_login()
    elif choice == "3":
        test_event_manager()
    elif choice == "4":
        test_student_registration()
        test_student_login()
        test_event_manager()
    else:
        print("Invalid choice")
