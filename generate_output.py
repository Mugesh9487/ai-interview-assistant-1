import json
import random
import os
from pathlib import Path

# Mocking the pipeline output for the HR Web Dashboard

def generate_mock_interview_output(candidate_id="CAND-10492"):
    """
    Generates a realistic JSON output that simulates the AI pipeline
    analyzing visual, audio, and lexical cues to predict HR traits.
    """
    # 1. Simulate Raw Cues Averages
    smile_score = round(random.uniform(0.60, 0.95), 2)
    eye_opening_dist = round(random.uniform(0.35, 0.50), 2)
    lip_corner_dist = round(random.uniform(0.50, 0.70), 2)
    
    avg_pitch = round(random.uniform(110.0, 210.0), 1)
    intensity = round(random.uniform(60.0, 75.0), 1)
    
    vader_sentiment = round(random.uniform(0.40, 0.85), 2)
    
    # 2. Simulate Predicted Traits (SVR/Ridge/Lasso Regression outputs)
    # Give the candidate a generally positive mock output
    stress_resistance = round(random.uniform(70.0, 95.0), 1)
    passion = round(random.uniform(75.0, 98.0), 1)
    confidence = round(random.uniform(70.0, 95.0), 1)
    cooperation = round(random.uniform(80.0, 99.0), 1)
    leadership = round(random.uniform(65.0, 90.0), 1)
    eye_contact = round(random.uniform(75.0, 95.0), 1)
    
    # Calculate Overall & Hireability based on traits
    general_overall = round(
        (stress_resistance + passion + confidence + cooperation + leadership + eye_contact) / 6, 
        1
    )
    
    # Weight hireability heavily on confidence, passion, and stress resistance
    hireability_score = round(
        (confidence * 0.3) + (passion * 0.25) + (stress_resistance * 0.25) + (general_overall * 0.2),
        1
    )
    
    if hireability_score >= 80:
         recommendation = "Strongly Consider"
    elif hireability_score >= 65:
         recommendation = "Consider"
    else:
         recommendation = "Do Not Hire"
         
    # 3. Assemble Final JSON Object
    output_data = {
        "candidate_id": candidate_id,
        "session_duration_seconds": random.randint(180, 900), # 3 to 15 mins
        "raw_cues_averages": {
            "visual": {
                "smile_score": smile_score,
                "eye_opening_distance": eye_opening_dist,
                "lip_corner_distance": lip_corner_dist,
                "fer2013_primary_emotion": "happy" if smile_score > 0.7 else "neutral"
            },
            "audio": {
                "average_pitch_hz": avg_pitch,
                "intensity_db": intensity
            },
            "lexical": {
                "vader_sentiment_compound": vader_sentiment
            }
        },
        "predicted_traits": {
            "stress_resistance": stress_resistance,
            "passion": passion,
            "confidence": confidence,
            "cooperation": cooperation,
            "leadership": leadership,
            "eye_contact": eye_contact,
            "general_overall": general_overall,
            "hireability_score": hireability_score
        },
        "recommendation": recommendation
    }
    
    return output_data

if __name__ == "__main__":
    # Ensure save directory exists
    save_dir = Path("ai_interview_assistant/data_save")
    save_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = save_dir / "predictedFeatures.json"
    
    print("Simulating AI Interview Analysis Pipeline...")
    output_data = generate_mock_interview_output()
    
    # Save the output
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=4)
        
    print(f"\nPipeline Complete. Output saved to: {output_path.absolute()}")
    print("\nSample Output Generated:")
    print(json.dumps(output_data, indent=4))
