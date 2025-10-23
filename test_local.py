#!/usr/bin/env python3
"""
Local testing script for Konflux MCP Server

This script tests the chatbot API directly without MCP protocol,
useful for debugging and verification.
"""

import asyncio
import os
import sys
import warnings
import httpx
from dotenv import load_dotenv

# Suppress SSL warnings for internal Red Hat certificates
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# Load environment variables
load_dotenv()

CHATBOT_URL = os.getenv(
    "KONFLUX_CHATBOT_URL",
    "https://chatbot-deployment-sp-support-chatbot--runtime-int.apps.int.stc.ai.prod.us-east-1.aws.paas.redhat.com"
)


async def test_invoke():
    """Test the /rag-with-sources/invoke endpoint"""
    print("🧪 Testing /rag-with-sources/invoke endpoint...")
    print(f"📍 URL: {CHATBOT_URL}/rag-with-sources/invoke")
    print()
    
    try:
        print("ℹ️  No authentication required (network-level access)")
        print()
        
        test_question = "What is Konflux?"
        print(f"❓ Question: {test_question}")
        print()
        
        # Note: verify=False for internal Red Hat self-signed certificates
        async with httpx.AsyncClient(timeout=120.0, verify=False) as client:
            response = await client.post(
                f"{CHATBOT_URL}/rag-with-sources/invoke",
                json={
                    "input": {
                        "question": test_question,
                        "urgency": "medium"
                    }
                }
            )
            
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Success!")
                print()
                print("📝 Response:")
                print("=" * 80)
                
                if isinstance(result, dict) and "output" in result:
                    print(result["output"])
                else:
                    print(result)
                
                print("=" * 80)
                return True
            else:
                print(f"❌ Error: HTTP {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
    except httpx.ConnectError:
        print("❌ Connection Error: Could not connect to the chatbot")
        print("   - Check if the URL is correct")
        print("   - Verify you have network access (VPN?)")
        print(f"   - URL: {CHATBOT_URL}")
        return False
    except httpx.TimeoutException:
        print("❌ Timeout: The chatbot took too long to respond")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_stream():
    """Test the /rag-with-sources/stream endpoint"""
    print("\n" + "=" * 80)
    print("🧪 Testing /rag-with-sources/stream endpoint...")
    print(f"📍 URL: {CHATBOT_URL}/rag-with-sources/stream")
    print()
    
    try:
        test_question = "How do I troubleshoot a failed Konflux pipeline?"
        print(f"❓ Question: {test_question}")
        print()
        print("📝 Streaming Response:")
        print("=" * 80)
        
        accumulated = ""
        
        # Note: verify=False for internal Red Hat self-signed certificates
        async with httpx.AsyncClient(timeout=120.0, verify=False) as client:
            async with client.stream(
                "POST",
                f"{CHATBOT_URL}/rag-with-sources/stream",
                json={
                    "input": {
                        "question": test_question,
                        "urgency": "medium"
                    }
                }
            ) as response:
                
                print(f"📊 Status Code: {response.status_code}")
                
                if response.status_code != 200:
                    print(f"❌ Error: HTTP {response.status_code}")
                    print(f"Response: {await response.aread()}")
                    return False
                
                print()
                
                async for chunk in response.aiter_bytes():
                    if chunk:
                        text = chunk.decode('utf-8', errors='ignore')
                        accumulated += text
                        print(text, end='', flush=True)
        
        print()
        print("=" * 80)
        
        if accumulated:
            print("✅ Streaming successful!")
            return True
        else:
            print("⚠️  No content received from stream")
            return False
            
    except httpx.ConnectError:
        print("❌ Connection Error: Could not connect to the chatbot")
        return False
    except httpx.TimeoutException:
        print("❌ Timeout: The chatbot took too long to respond")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def check_playground():
    """Check if the playground is accessible"""
    print("\n" + "=" * 80)
    print("🧪 Checking /playground endpoint...")
    print(f"📍 URL: {CHATBOT_URL}/playground")
    print()
    
    try:
        # Note: verify=False for internal Red Hat self-signed certificates
        async with httpx.AsyncClient(timeout=30.0, verify=False) as client:
            response = await client.get(f"{CHATBOT_URL}/playground")
            
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Playground is accessible!")
                print(f"🌐 Open in browser: {CHATBOT_URL}/playground")
                return True
            else:
                print(f"⚠️  Unexpected status code: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


async def main():
    """Run all tests"""
    print("🚀 Konflux Chatbot MCP Server - Local Testing")
    print("=" * 80)
    print()
    print("ℹ️  Note: This chatbot uses network-level authentication")
    print("   Ensure you're on Red Hat VPN if accessing internal services")
    print()
    
    # Run tests
    results = []
    
    # Test playground
    results.append(("Playground", await check_playground()))
    
    # Test invoke
    results.append(("Invoke", await test_invoke()))
    
    # Test streaming
    results.append(("Stream", await test_stream()))
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 Test Summary")
    print("=" * 80)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
    
    print()
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("🎉 All tests passed! The MCP server should work correctly.")
        print()
        print("Next steps:")
        print("1. Configure Cursor with your MCP server settings")
        print("2. Use the konflux_chat tool from within Cursor")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print()
        print("Common issues:")
        print("- Network connectivity (VPN required for Red Hat internal services)")
        print("- Incorrect chatbot URL")
        print("- Chatbot service is down")
        print("- Firewall/proxy blocking the connection")
    
    print()


if __name__ == "__main__":
    asyncio.run(main())

