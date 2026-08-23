from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model import sentiment_model

app = FastAPI(title="Early Depression Detection Portal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputData(BaseModel):
    name: str 
    age: int
    text: str
    
    
    q1_mood: int          
    q2_anxiety: int
    q3_irritability: int
    
    
    q4_stress: int
    q5_overthinking: int
    

    q6_sleep: int         
    q7_energy: int
    
    
    q8_work_pressure: int 
    q9_focus: int         
    
    
    q10_social: int       
    q11_activities: int   
    q12_future: int       

@app.post("/analyze")
def analyze_sentiment(input_data: InputData):
    if not input_data.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
    
        ai_results = sentiment_model.analyze_text(input_data.text)
        emotions = ai_results['emotions']
        sentiment = ai_results['sentiment']
        
        
        ai_positivity = 0
        if sentiment['label'] == 'POSITIVE':
            ai_positivity = sentiment['score'] * 100
        else:
            ai_positivity = (1.0 - sentiment['score']) * 100

        
        
        
        raw_anxiety = input_data.q2_anxiety + input_data.q5_overthinking
        score_anxiety = (raw_anxiety / 6) * 100
        
    
        raw_stress = input_data.q3_irritability + input_data.q4_stress + input_data.q8_work_pressure
        score_stress = (raw_stress / 9) * 100
        
        
        
        
        mood_risk = input_data.q1_mood + (3 - input_data.q12_future)
        score_mood_balance = 100 - ((mood_risk / 6) * 100)

     
        risk_direct = (
            input_data.q1_mood + input_data.q2_anxiety + input_data.q3_irritability + 
            input_data.q4_stress + input_data.q5_overthinking + input_data.q8_work_pressure
        ) 
        
        risk_reverse = (
            (3 - input_data.q6_sleep) + (3 - input_data.q7_energy) + (3 - input_data.q9_focus) + 
            (3 - input_data.q10_social) + (3 - input_data.q11_activities) + (3 - input_data.q12_future) 
        )
        
        total_risk_points = risk_direct + risk_reverse
        max_possible_points = 36
        q_risk_norm = total_risk_points / max_possible_points

        
        ai_risk_score = 1.0 - (ai_positivity / 100)

        
        final_risk_score = ((q_risk_norm * 0.7) + (ai_risk_score * 0.3)) * 100
        
        
        

        dominant_emotion = emotions[0]['label'].lower() if emotions else "neutral"

        if final_risk_score < 40:
            category = "NORMAL"
        elif final_risk_score < 75:
            category = "MODERATE"
        else:
            category = "SEVERE"

        # 1. Intelligent Summary Generation
        if category == "NORMAL":
            condition_msg = "You are doing absolutely well. Your emotional health appears stable."
        elif category == "MODERATE":
            condition_msg = "You may be experiencing some level of stress or emotional imbalance."
        else:
            condition_msg = "Your responses indicate significant emotional distress. It is recommended to consult a qualified doctor or mental health expert."

        # Behavioral insights
        issues = []
        if input_data.q6_sleep <= 1: issues.append("reduced sleep quality")
        else: issues.append("good sleep patterns")
        
        if input_data.q10_social <= 1: issues.append("social withdrawal")
        else: issues.append("active social interactions")
        
        if (input_data.q2_anxiety + input_data.q5_overthinking) >= 4: issues.append("signs of anxiety")
        
        if input_data.q1_mood >= 2: issues.append("depressed mood")

        behavioral_insight = f"Behavioral check: We noticed {', '.join(issues)}."

        sec_summary = f"Hello {input_data.name},<br>{condition_msg}<br>{behavioral_insight}"

        # Emotional Analysis
        sec_emotional = f"Based on your written input, the predominant emotion is <b>{dominant_emotion}</b>. "
        if dominant_emotion in ['sadness', 'fear', 'anger', 'disgust', 'grief']:
            sec_emotional += "It is completely valid to experience these challenging emotions. It's important to acknowledge them."
        elif dominant_emotion in ['joy', 'love', 'optimism', 'caring', 'approval']:
            sec_emotional += "Your text reflects an uplifting and positive outlook."
        else:
            sec_emotional += "This reflects a generally mixed or neutral state of mind."

        # Stress Level
        if score_stress < 40:
            sec_stress = f"Score: {round(score_stress)}%. Your stress is well managed and within a very healthy range."
        elif score_stress < 75:
            sec_stress = f"Score: {round(score_stress)}%. You are carrying a moderate stress load, likely from daily or academic pressures."
        else:
            sec_stress = f"Score: {round(score_stress)}%. You are facing a significantly high stress load right now."

        summary_text = f"<div style='margin-bottom:12px;'><b>Overall Summary</b><br>{sec_summary}</div><div style='margin-bottom:12px;'><b>Emotional Analysis</b><br>{sec_emotional}</div><div><b>Stress Level</b><br>{sec_stress}</div>"

        # Dynamic Response Logic
        advice_title = "Recommendations"
        advice_list = []

        if category == "NORMAL":
            advice_list = [
                "Ensure you get proper sleep each night.",
                "Engage in regular physical exercise.",
                "Maintain active social interaction with peers."
            ]
        elif category == "MODERATE":
            advice_list = [
                "Practice relaxation techniques and mindfulness.",
                "Talk to your friends or family members about how you feel.",
                "Consider reducing your screen time, especially before bed."
            ]
        else:
            advice_list = [
                "Consider consulting a professional mental health counselor or therapist.",
                "Reach out for dedicated support from a trusted friend, adult, or helpline.",
                "It is recommended to consult a qualified doctor or mental health expert."
            ]

        # Emotion-specific personalized suggestions
        emo_mapped = dominant_emotion
        if emo_mapped in ['sadness', 'grief', 'remorse']:
            advice_list.append("For sadness: Try journaling your thoughts or talking to someone you trust.")
        elif emo_mapped in ['anxiety', 'fear', 'nervousness']:
            advice_list.append("For anxiety: Practice deep breathing exercises and meditation.")
        elif emo_mapped in ['anger', 'annoyance', 'disapproval']:
            advice_list.append("For anger: Engage in physical activity or mindfulness to release tension constructively.")

        return {
            "name": input_data.name,
            "category": category,
            "final_score": round(final_risk_score),
            "breakdown": {
                "anxiety": round(score_anxiety),
                "stress": round(score_stress),
                "mood_balance": round(score_mood_balance),
                "positivity": round(ai_positivity)
            },
            "summary": summary_text,
            "advice": {
                "title": advice_title,
                "steps": advice_list
            },
            "ai_analysis": {
                "emotion": emotions[0]['label'],
                "sentiment": sentiment['label']
            }
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
