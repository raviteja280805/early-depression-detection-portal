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
    
    # Emotional Stability
    q1_mood: int          # 0=Never, 3=Always
    q2_anxiety: int
    q3_irritability: int
    
    # Stress & Overthinking
    q4_stress: int
    q5_overthinking: int
    
    # Physical/Lifestyle
    q6_sleep: int         # 0=Never, 3=Always (Reverse)
    q7_energy: int
    
    # Academic/Work
    q8_work_pressure: int # 0=Never, 3=Always
    q9_focus: int         # 0=Never, 3=Always (Reverse)
    
    # Social/Motivation
    q10_social: int       # Reverse
    q11_activities: int   # Reverse
    q12_future: int       # Reverse

@app.post("/analyze")
def analyze_sentiment(input_data: InputData):
    if not input_data.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        # --- 1. AI Analysis ---
        ai_results = sentiment_model.analyze_text(input_data.text)
        emotions = ai_results['emotions']
        sentiment = ai_results['sentiment']
        
        # Calculate AI Positivity Score (0-100)
        # If Positive: Score is high. If Negative: Score is low.
        ai_positivity = 0
        if sentiment['label'] == 'POSITIVE':
            ai_positivity = sentiment['score'] * 100
        else:
            ai_positivity = (1.0 - sentiment['score']) * 100

        # --- 2. Sub-Category Scoring (0-100 Normalized) ---
        
        # ANXIETY (q2 + q5) -> Max 6
        raw_anxiety = input_data.q2_anxiety + input_data.q5_overthinking
        score_anxiety = (raw_anxiety / 6) * 100
        
        # STRESS (q3 + q4 + q8) -> Max 9
        raw_stress = input_data.q3_irritability + input_data.q4_stress + input_data.q8_work_pressure
        score_stress = (raw_stress / 9) * 100
        
        # MOOD BALANCE (Inverse of Risk)
        # Mood is good if q1 is low and q12 is high.
        # Let's calculate "Mood Risk" first: q1 + (3-q12). Max 6.
        mood_risk = input_data.q1_mood + (3 - input_data.q12_future)
        score_mood_balance = 100 - ((mood_risk / 6) * 100)

        # --- 3. Total Risk Calculation ---
        # Direct Risk (High value = High Risk)
        risk_direct = (
            input_data.q1_mood + input_data.q2_anxiety + input_data.q3_irritability + 
            input_data.q4_stress + input_data.q5_overthinking + input_data.q8_work_pressure
        ) 
        # Reverse Risk (Low value = High Risk)
        risk_reverse = (
            (3 - input_data.q6_sleep) + (3 - input_data.q7_energy) + (3 - input_data.q9_focus) + 
            (3 - input_data.q10_social) + (3 - input_data.q11_activities) + (3 - input_data.q12_future) 
        )
        
        total_risk_points = risk_direct + risk_reverse
        max_possible_points = 36
        q_risk_norm = total_risk_points / max_possible_points

        # AI Risk (Inverse of Positivity)
        ai_risk_score = 1.0 - (ai_positivity / 100)

        # Final Weighted Score (0-100 Risk)
        final_risk_score = ((q_risk_norm * 0.7) + (ai_risk_score * 0.3)) * 100
        
        # --- 4. Detailed Summary Generation ---
        
        # Categorization
        if final_risk_score < 30:
            category = "Good / Stable"
            tone = "positive"
        elif final_risk_score < 55:
            category = "Mild Stress"
            tone = "mild"
        elif final_risk_score < 75:
            category = "Moderate Stress"
            tone = "moderate"
        else:
            category = "High Emotional Distress"
            tone = "high"

        # Constructing the Detailed Report
        details = []
        
        # Emotional
        if score_mood_balance < 50:
            details.append("Emotional stability appears low, indicating feelings of sadness or hopelessness.")
        else:
            details.append("Your emotional balance reflects a generally stable outlook.")
            
        # Stress
        if score_stress > 60:
            details.append("Stress indicators are elevated, likely due to academic or work pressures.")
        elif score_stress > 30:
            details.append("You are experiencing manageable levels of daily stress.")
        else:
            details.append("Your stress levels are well within a healthy range.")
            
        # Behavioral
        behaviors = []
        if input_data.q6_sleep <= 1: behaviors.append("sleep quality")
        if input_data.q10_social <= 1: behaviors.append("social withdrawal")
        if behaviors:
            details.append(f"Behavioral patterns show potential concerns with {', '.join(behaviors)}.")
        else:
            details.append("Your behavioral patterns (sleep, social interaction) appear healthy.")

        summary_text = f"Hello {input_data.name}, here is your comprehensive analysis.\n\n"
        summary_text += " ".join(details)
        
        # Actionable Advice
        if tone == "positive":
            advice_title = "Maintain Your Momentum"
            advice_list = [
                "Keep up your regular sleep schedule.",
                "Continue engaging in hobbies you enjoy.",
                "Practice gratitude to boost your mood further."
            ]
        elif tone == "mild":
            advice_title = "Preventive Care Suggestions"
            advice_list = [
                "Take short 5-minute breaks during study/work.",
                "Try a simple breathing exercise before sleep.",
                "Ensure you are staying hydrated."
            ]
        elif tone == "moderate":
            advice_title = "Active Coping Strategies"
            advice_list = [
                "Prioritize 7-8 hours of sleep tonight.",
                "Talk to a friend or family member about what's bothering you.",
                "Engage in physical activity (walk/jog) to release tension."
            ]
        else: # high
            advice_title = "Support & Recovery"
            advice_list = [
                "Please reach out to a school counselor or trusted adult.",
                "Avoid isolating yourself; keep communication open.",
                "Focus on getting through one day at a time.",
                "Remember, asking for help is a sign of strength."
            ]

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
