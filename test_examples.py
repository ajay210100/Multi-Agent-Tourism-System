"""
Test script to verify the tourism system works with the provided examples.
No API keys required - uses only free APIs.
"""
from tourism_agent import TourismAgent

def test_examples():
    """Test the system with the provided examples."""
    
    agent = TourismAgent()
    
    test_cases = [
        "I'm going to go to Bangalore, let's plan my trip.",
        "I'm going to go to Bangalore, what is the temperature there",
        "I'm going to go to Bangalore, what is the temperature there? And what are the places I can visit?"
    ]
    
    print("=" * 60)
    print("Testing Multi-Agent Tourism System")
    print("=" * 60)
    
    for i, query in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"Test Case {i}:")
        print(f"Input: {query}")
        print(f"\nOutput:")
        try:
            response = agent.process_query(query)
            print(response)
        except Exception as e:
            print(f"Error: {e}")
    
    print(f"\n{'='*60}")
    print("Testing complete!")

if __name__ == "__main__":
    test_examples()

