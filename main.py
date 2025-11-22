"""
Main script to run the multi-agent tourism system.
"""
from tourism_agent import TourismAgent
import sys


def main():
    """
    Main function to run the tourism system.
    """
    print("=" * 60)
    print("Multi-Agent Tourism System")
    print("=" * 60)
    print("\nEnter a place you want to visit and ask about weather or places to visit.")
    print("Examples:")
    print("  - 'I'm going to go to Bangalore, let's plan my trip.'")
    print("  - 'I'm going to go to Bangalore, what is the temperature there'")
    print("  - 'I'm going to go to Bangalore, what is the temperature there? And what are the places I can visit?'")
    print("\nType 'exit' or 'quit' to stop.\n")
    
    try:
        # Initialize the Tourism Agent
        agent = TourismAgent()
        
        while True:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\nThank you for using the Tourism System. Goodbye!")
                break
            
            # Process query
            print("\nTourism Agent: ", end="", flush=True)
            response = agent.process_query(user_input)
            print(response)
            
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        print("\nPlease make sure you have installed all required packages:")
        print("pip install -r requirements.txt")
        sys.exit(1)


if __name__ == "__main__":
    main()

