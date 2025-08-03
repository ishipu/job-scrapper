import requests
import json
from typing import List, Dict
import time

class LocalLLMClient:
    def __init__(self, base_url: str = "http://localhost:1234"):
        self.base_url = base_url
        self.endpoint = f"{base_url}/v1/chat/completions"
        
    def test_connection(self) -> bool:
        """Test if LMStudio server is running"""
        try:
            response = requests.get(f"{self.base_url}/v1/models", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def chat(self, messages: List[Dict], temperature: float = 0.3, max_tokens: int = 500) -> str:
        """Send chat request to local LLM"""
        if not self.test_connection():
            raise Exception("LMStudio server is not running. Please start it first.")
        
        data = {
            "model": "llama-3.2-3b-instruct",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(
                self.endpoint, 
                headers={"Content-Type": "application/json"}, 
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                raise Exception(f"LLM request failed: {response.status_code}")
                
        except requests.exceptions.Timeout:
            raise Exception("LLM request timed out. Model might be too large for your system.")
        except Exception as e:
            raise Exception(f"LLM request error: {str(e)}")
    
    def extract_job_info(self, job_html: str) -> Dict:
        """Use LLM to extract structured job information"""
        messages = [
            {
                "role": "system", 
                "content": """You are a job information extractor. Extract job details from HTML and return ONLY a JSON object with these fields:
- title: job title
- company: company name  
- location: job location
- description: brief description (max 200 chars)
- requirements: key requirements (max 150 chars)
- salary: salary if mentioned, else null

Return only valid JSON, no other text."""
            },
            {
                "role": "user", 
                "content": f"Extract job info from this HTML:\n{job_html[:1000]}..."
            }
        ]
        
        response = self.chat(messages, temperature=0.1)
        
        try:
            # Try to parse JSON response
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback parsing if LLM doesn't return pure JSON
            return {
                "title": "Parse Error",
                "company": "Unknown", 
                "location": "Unknown",
                "description": response[:200],
                "requirements": "Could not parse",
                "salary": None
            }

# Test the client
if __name__ == "__main__":
    client = LocalLLMClient()
    
    if client.test_connection():
        print("✅ LLM Client ready!")
        
        # Simple test
        test_response = client.chat([
            {"role": "user", "content": "Say 'Job Agent Ready!' if you can help with job searching."}
        ])
        print("Test response:", test_response)
    else:
        print("❌ LMStudio server not running. Please start it first.")