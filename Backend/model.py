from transformers import pipeline

class SentimentModel:
    def __init__(self):

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

        emotion_results = self.emotion_classifier(text)[0]


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


sentiment_model = SentimentModel()
