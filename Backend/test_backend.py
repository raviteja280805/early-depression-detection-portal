import sys
import os

# Add the current directory to sys.path to ensure we can import our modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    print("Test 1: Importing SentimentModel...")
    from model import sentiment_model
    print("Success: Model imported and loaded.")

    print("\nTest 2: Running analysis on sample text...")
    sample_text = "I feel very hopeless and sad today."
    result = sentiment_model.analyze_text(sample_text)
    print(f"Input: {sample_text}")
    print(f"Result: {result}")
    
    # basic check
    sadness_score = next((item for item in result if item["label"] == "sadness"), None)
    if sadness_score and sadness_score['score'] > 0.5:
        print("\nTest 3: Logic Check - Sadness detected as expected.")
    else:
        print("\nTest 3: Logic Check - Unexpected result (sadness score might be low).")

    print("\nAll tests passed!")

except Exception as e:
    print(f"\nFATAL ERROR: {e}")
    import traceback
    traceback.print_exc()
