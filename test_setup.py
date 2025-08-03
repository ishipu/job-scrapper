from src.llm_client import LocalLLMClient

def main():
    print("🚀 Testing LinkedIn Job Agent Foundation...")
    
    # Test LLM connection
    print("\n1. Testing LLM Connection...")
    client = LocalLLMClient()
    
    if client.test_connection():
        print("✅ LMStudio server is running")
        
        # Test basic chat
        response = client.chat([
            {"role": "user", "content": "List 3 important skills for a software engineer job"}
        ])
        print("✅ LLM responding correctly")
        print("Sample response:", response[:100] + "...")
        
    else:
        print("❌ LMStudio server not running")
        print("Please:")
        print("1. Open LMStudio")
        print("2. Go to 'Local Server' tab") 
        print("3. Load a model (Llama-3.2-3B-Instruct recommended)")
        print("4. Start the server")
        return
    
    print("\n🎉 Foundation setup complete! Ready for Phase 2.")

if __name__ == "__main__":
    main()