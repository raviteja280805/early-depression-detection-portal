from transformers import pipeline

class SentimentModel:
    def __init__(self):
        # Initialize the emotion detection pipeline
        # Using 'bhadresh-savani/distilbert-base-uncased-emotion' which is good for detecting
        # emotions like sadness, fear, anger which are relevant for depression detection.
        print("Loading Emotion model...")
        self.emotion_classifier = pipeline(
            "text-classification", 
            model="bhadresh-savani/distilbert-base-uncased-emotion", 
            top_k=None
        )
        
        print("Models loaded successfully.")

    def analyze_text(self, text: str):
        """
        Runs emotion analysis and derives sentiment logic.
        """
        # 1. Emotion Analysis
        # Result is a list of lists (one list per input text). We take [0] for the first input.
        # This gives us a LIST of dicts: [{'label': 'joy', 'score': 0.9}, ...]
        emotion_results = self.emotion_classifier(text)[0]
        
        # 2. Derive Sentiment (Simplified for speed)
        # Check if top emotion (index 0) is positive
        top_emotion_data = emotion_results[0]
        top_emotion = top_emotion_data['label'] 
        score = top_emotion_data['score']
        
        if top_emotion in ['joy', 'love', 'surprise']:
            sentiment_result = {'label': 'POSITIVE', 'score': score}
        else:
            sentiment_result = {'label': 'NEGATIVE', 'score': score}
        
        return {
            "emotions": emotion_results,
            "sentiment": sentiment_result
        }

# Singleton instance to be reused
# Initializing it here effectively loads the model when this module is imported.
# In a larger app, you might want to load this lazily or in a startup event.
sentiment_model = SentimentModel()
