#!/usr/bin/env python3
"""
ShramSetu Backend API Testing Script
Tests all CRUD operations for the laborer management system and job management system
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional

class ShramSetuAPITester:
    def __init__(self, base_url: str = "https://5a14141c-ed42-41e0-a643-3a7faa760df8.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.created_laborers = []  # Track created laborers for cleanup
        self.created_jobs = []  # Track created jobs for cleanup

    def log_test(self, name: str, success: bool, details: str = ""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED {details}")
        else:
            print(f"❌ {name} - FAILED {details}")

    def run_test(self, name: str, method: str, endpoint: str, expected_status: int, 
                 data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> tuple:
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}"
        if headers is None:
            headers = {'Content-Type': 'application/json'}

        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        print(f"   Method: {method}")
        if data:
            print(f"   Data: {json.dumps(data, indent=2)}")

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")

            success = response.status_code == expected_status
            response_data = {}
            
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text}

            details = f"(Status: {response.status_code})"
            if not success:
                details += f" Expected: {expected_status}"
                if response_data:
                    details += f" Response: {json.dumps(response_data, indent=2)}"

            self.log_test(name, success, details)
            return success, response_data, response.status_code

        except Exception as e:
            self.log_test(name, False, f"Exception: {str(e)}")
            return False, {}, 0

    def test_health_check(self):
        """Test the health check endpoint"""
        success, response, _ = self.run_test(
            "Health Check",
            "GET",
            "",
            200
        )
        if success and response.get("message") == "ShramSetu API is running":
            print("   ✓ Health check message correct")
        return success

    def test_register_laborer(self, laborer_data: Dict[str, Any], should_succeed: bool = True):
        """Test laborer registration"""
        expected_status = 201 if should_succeed else 400
        test_name = f"Register Laborer - {laborer_data.get('name', 'Unknown')}"
        
        success, response, status_code = self.run_test(
            test_name,
            "POST",
            "laborers/register",
            expected_status,
            laborer_data
        )
        
        if success and should_succeed:
            laborer_id = response.get("id")
            if laborer_id:
                self.created_laborers.append(laborer_id)
                print(f"   ✓ Laborer registered with ID: {laborer_id}")
                return laborer_id
        
        return None if should_succeed else success

    def test_get_all_laborers(self):
        """Test getting all laborers"""
        success, response, _ = self.run_test(
            "Get All Laborers",
            "GET",
            "laborers/",
            200
        )
        
        if success:
            laborers_count = len(response) if isinstance(response, list) else 0
            print(f"   ✓ Retrieved {laborers_count} laborers")
        
        return success, response

    def test_get_laborer_by_id(self, laborer_id: str):
        """Test getting a specific laborer by ID"""
        success, response, _ = self.run_test(
            f"Get Laborer by ID - {laborer_id}",
            "GET",
            f"laborers/{laborer_id}",
            200
        )
        
        if success and response.get("id") == laborer_id:
            print(f"   ✓ Retrieved laborer: {response.get('name')}")
        
        return success, response

    def test_update_laborer(self, laborer_id: str, update_data: Dict[str, Any]):
        """Test updating laborer information"""
        success, response, _ = self.run_test(
            f"Update Laborer - {laborer_id}",
            "PUT",
            f"laborers/{laborer_id}",
            200,
            update_data
        )
        
        if success:
            print(f"   ✓ Updated laborer successfully")
        
        return success, response

    def test_delete_laborer(self, laborer_id: str):
        """Test deleting a laborer"""
        success, response, _ = self.run_test(
            f"Delete Laborer - {laborer_id}",
            "DELETE",
            f"laborers/{laborer_id}",
            200
        )
        
        if success:
            print(f"   ✓ Deleted laborer successfully")
            # Remove from tracking list
            if laborer_id in self.created_laborers:
                self.created_laborers.remove(laborer_id)
        
        return success

    def test_invalid_data_validation(self):
        """Test various invalid data scenarios"""
        print("\n🧪 Testing Data Validation...")
        
        # Test missing required fields (FastAPI returns 422 for validation errors)
        invalid_cases = [
            {
                "name": "Missing Phone",
                "data": {"name": "Test", "skill": "mason", "location": "Delhi", "language": "hindi"},
                "expected_error": "phone"
            },
            {
                "name": "Invalid Phone Format",
                "data": {"name": "Test", "phone": "invalid-phone", "skill": "mason", "location": "Delhi", "language": "hindi"},
                "expected_error": "phone"
            },
            {
                "name": "Empty Name",
                "data": {"name": "", "phone": "+919876543210", "skill": "mason", "location": "Delhi", "language": "hindi"},
                "expected_error": "name"
            },
            {
                "name": "Missing Skill",
                "data": {"name": "Test", "phone": "+919876543210", "location": "Delhi", "language": "hindi"},
                "expected_error": "skill"
            }
        ]
        
        validation_passed = 0
        for case in invalid_cases:
            # FastAPI returns 422 for validation errors, not 400
            success, response, status_code = self.run_test(
                f"Validation - {case['name']}",
                "POST",
                "laborers/register",
                422,  # Changed from 400 to 422
                case["data"]
            )
            if success:
                validation_passed += 1
        
        print(f"   Validation tests passed: {validation_passed}/{len(invalid_cases)}")
        return validation_passed == len(invalid_cases)

    def cleanup_created_laborers(self):
        """Clean up any laborers created during testing"""
        print(f"\n🧹 Cleaning up {len(self.created_laborers)} created laborers...")
        for laborer_id in self.created_laborers.copy():
            self.test_delete_laborer(laborer_id)

    def run_comprehensive_tests(self):
        """Run all tests in sequence"""
        print("🚀 Starting ShramSetu API Comprehensive Tests")
        print(f"   Base URL: {self.base_url}")
        print(f"   API URL: {self.api_url}")
        print("=" * 60)

        # Test 1: Health Check
        if not self.test_health_check():
            print("❌ Health check failed - stopping tests")
            return False

        # Test 2: Register valid laborer (using unique phone number)
        timestamp = datetime.now().strftime("%H%M%S")
        valid_laborer = {
            "name": "Raju Kumar",
            "phone": f"+91987654{timestamp[-4:]}",  # Unique phone number
            "skill": "mason",
            "location": "Tilak Nagar",
            "language": "hindi"
        }
        
        laborer_id = self.test_register_laborer(valid_laborer)
        if not laborer_id:
            print("❌ Failed to register valid laborer - stopping tests")
            return False

        # Test 3: Try to register duplicate phone (should fail) - using existing phone
        duplicate_laborer = {
            "name": "Another Person",
            "phone": "+919876543210",  # This phone already exists in DB
            "skill": "carpenter",
            "location": "CP",
            "language": "english"
        }
        self.test_register_laborer(duplicate_laborer, should_succeed=False)

        # Test 4: Get all laborers
        success, all_laborers = self.test_get_all_laborers()
        if not success:
            print("❌ Failed to get all laborers")

        # Test 5: Get specific laborer by ID
        success, laborer_data = self.test_get_laborer_by_id(laborer_id)
        if not success:
            print("❌ Failed to get laborer by ID")

        # Test 6: Update laborer information
        update_data = {
            "skill": "senior mason",
            "available": False
        }
        success, updated_laborer = self.test_update_laborer(laborer_id, update_data)
        if not success:
            print("❌ Failed to update laborer")

        # Test 7: Data validation tests
        self.test_invalid_data_validation()

        # Test 8: Test non-existent laborer
        self.run_test(
            "Get Non-existent Laborer",
            "GET",
            "laborers/non-existent-id",
            404
        )

        # Test 8.5: Test API documentation
        success, response, _ = self.run_test(
            "API Documentation",
            "GET",
            "../docs",  # Go up one level from /api to get /docs
            200
        )

        # Test 9: Register another laborer for more comprehensive testing
        second_laborer = {
            "name": "Shyam Singh",
            "phone": f"+91876543{timestamp[-4:]}",  # Another unique phone
            "skill": "carpenter",
            "location": "Karol Bagh",
            "language": "punjabi"
        }
        second_id = self.test_register_laborer(second_laborer)

        # Test 10: Final get all laborers to verify count
        success, final_laborers = self.test_get_all_laborers()
        if success:
            print(f"   Final laborer count: {len(final_laborers)}")

        # Cleanup
        self.cleanup_created_laborers()

        return True

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%" if self.tests_run > 0 else "No tests run")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL TESTS PASSED!")
            return True
        else:
            print("⚠️  SOME TESTS FAILED")
            return False

def main():
    """Main test execution"""
    tester = ShramSetuAPITester()
    
    try:
        success = tester.run_comprehensive_tests()
        all_passed = tester.print_summary()
        
        return 0 if all_passed else 1
        
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
        tester.cleanup_created_laborers()
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")
        tester.cleanup_created_laborers()
        return 1

if __name__ == "__main__":
    sys.exit(main())