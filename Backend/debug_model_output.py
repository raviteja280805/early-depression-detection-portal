from model import sentiment_model
import json

try:
    print("Analyzing text...")
    result = sentiment_model.analyze_text("I feel very hopeless and sad.")
    print(f"Type of result: {type(result)}")
    print(f"Result content: {result}")
    
    if isinstance(result, list):
        if len(result) > 0:
            print(f"Type of first item: {type(result[0])}")
            print(f"First item: {result[0]}")
            
except Exception as e:
    print(f"Error: {e}")
