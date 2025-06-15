"""
Test API endpoints for Render deployment
Tests the simple research API that returns only string reports
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any
import time


class TestRenderAPI:
    """Test suite for Render deployment API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}
    
    async def test_simple_research(self) -> Dict[str, Any]:
        """Test the /api/research endpoint"""
        test_cases = [
            {
                "name": "Basic Research Report",
                "payload": {
                    "task": "What are the latest trends in renewable energy in 2024?",
                    "report_type": "research_report",
                    "report_source": "web",
                    "tone": "Objective"
                }
            },
            {
                "name": "Detailed Report",
                "payload": {
                    "task": "Analyze the impact of AI on healthcare industry",
                    "report_type": "detailed_report",
                    "report_source": "web",
                    "tone": "Analytical"
                }
            },
            {
                "name": "Resource Report",
                "payload": {
                    "task": "Find resources about Python web frameworks",
                    "report_type": "resource_report",
                    "report_source": "web",
                    "tone": "Informative"
                }
            }
        ]
        
        results = []
        
        async with aiohttp.ClientSession() as session:
            for test_case in test_cases:
                print(f"\n{'='*50}")
                print(f"Testing: {test_case['name']}")
                print(f"{'='*50}")
                
                start_time = time.time()
                
                try:
                    async with session.post(
                        f"{self.base_url}/api/research",
                        json=test_case["payload"],
                        headers=self.headers
                    ) as response:
                        response_data = await response.json()
                        elapsed_time = time.time() - start_time
                        
                        result = {
                            "test_name": test_case["name"],
                            "status_code": response.status,
                            "success": response.status == 200,
                            "elapsed_time": f"{elapsed_time:.2f}s",
                            "response": response_data
                        }
                        
                        if response.status == 200:
                            print(f"✅ Success! Report generated in {elapsed_time:.2f}s")
                            print(f"Report length: {len(response_data.get('report', ''))} characters")
                            if response_data.get('research_costs'):
                                print(f"Research costs: {response_data['research_costs']}")
                        else:
                            print(f"❌ Failed with status code: {response.status}")
                            print(f"Error: {response_data}")
                        
                        results.append(result)
                        
                except Exception as e:
                    print(f"❌ Exception occurred: {str(e)}")
                    results.append({
                        "test_name": test_case["name"],
                        "status_code": None,
                        "success": False,
                        "error": str(e)
                    })
        
        return results
    
    async def test_health_check(self) -> Dict[str, Any]:
        """Test the health check endpoint"""
        print(f"\n{'='*50}")
        print("Testing: Health Check")
        print(f"{'='*50}")
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.base_url}/health") as response:
                    data = await response.json()
                    
                    if response.status == 200:
                        print(f"✅ Health check passed: {data}")
                        return {"success": True, "data": data}
                    else:
                        print(f"❌ Health check failed: {response.status}")
                        return {"success": False, "status": response.status}
                        
            except Exception as e:
                print(f"❌ Health check exception: {str(e)}")
                return {"success": False, "error": str(e)}
    
    async def test_minimal_request(self) -> Dict[str, Any]:
        """Test with minimal parameters (using defaults)"""
        print(f"\n{'='*50}")
        print("Testing: Minimal Request")
        print(f"{'='*50}")
        
        payload = {
            "task": "What is quantum computing?"
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.base_url}/api/research",
                    json=payload,
                    headers=self.headers
                ) as response:
                    data = await response.json()
                    
                    if response.status == 200:
                        print(f"✅ Minimal request succeeded")
                        print(f"Report generated: {len(data.get('report', ''))} characters")
                        return {"success": True, "report_length": len(data.get('report', ''))}
                    else:
                        print(f"❌ Minimal request failed: {response.status}")
                        return {"success": False, "error": data}
                        
            except Exception as e:
                print(f"❌ Exception: {str(e)}")
                return {"success": False, "error": str(e)}
    
    async def test_error_handling(self) -> Dict[str, Any]:
        """Test error handling with invalid parameters"""
        print(f"\n{'='*50}")
        print("Testing: Error Handling")
        print(f"{'='*50}")
        
        test_cases = [
            {
                "name": "Empty task",
                "payload": {
                    "task": ""
                }
            },
            {
                "name": "Invalid report type",
                "payload": {
                    "task": "Test query",
                    "report_type": "invalid_type"
                }
            },
            {
                "name": "Invalid tone",
                "payload": {
                    "task": "Test query",
                    "tone": "InvalidTone"
                }
            }
        ]
        
        results = []
        
        async with aiohttp.ClientSession() as session:
            for test_case in test_cases:
                print(f"\nTesting: {test_case['name']}")
                
                try:
                    async with session.post(
                        f"{self.base_url}/api/research",
                        json=test_case["payload"],
                        headers=self.headers
                    ) as response:
                        data = await response.json()
                        
                        print(f"Status: {response.status}")
                        print(f"Response: {data}")
                        
                        results.append({
                            "test": test_case["name"],
                            "status": response.status,
                            "response": data
                        })
                        
                except Exception as e:
                    print(f"Exception: {str(e)}")
                    results.append({
                        "test": test_case["name"],
                        "error": str(e)
                    })
        
        return results


async def main():
    """Run all tests"""
    print("🚀 Starting API tests for Render deployment")
    print(f"{'='*70}")
    
    # Initialize test suite
    tester = TestRenderAPI()
    
    # Run health check
    print("\n1. Health Check Test")
    health_result = await tester.test_health_check()
    
    if not health_result.get("success"):
        print("\n⚠️  Server appears to be down. Make sure the server is running.")
        print("Run: python -m uvicorn backend.server.server:app --reload")
        return
    
    # Run minimal request test
    print("\n2. Minimal Request Test")
    minimal_result = await tester.test_minimal_request()
    
    # Run main research tests
    print("\n3. Research API Tests")
    research_results = await tester.test_simple_research()
    
    # Run error handling tests
    print("\n4. Error Handling Tests")
    error_results = await tester.test_error_handling()
    
    # Summary
    print(f"\n{'='*70}")
    print("📊 Test Summary")
    print(f"{'='*70}")
    
    successful_tests = sum(1 for r in research_results if r.get("success", False))
    print(f"Research Tests: {successful_tests}/{len(research_results)} passed")
    print(f"Minimal Request: {'✅ Passed' if minimal_result.get('success') else '❌ Failed'}")
    print(f"Error Handling: {len(error_results)} test cases executed")
    
    print("\n✅ All tests completed!")


if __name__ == "__main__":
    asyncio.run(main())