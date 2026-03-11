import streamlit as st
import json
import pandas as pd
import os
import time

st.set_page_config(page_title="HR Dashboard", layout="wide", page_icon="👔")

def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return None

st.title("👔 AI Interview Analysis Dashboard")
st.markdown("---")

json_path = "data_save/predictedFeatures.json"
data = load_data(json_path)

if not data:
    st.warning(f"No prediction data found at `{json_path}`. Run `python main.py` first.")
    st.stop()
    
# Layout
col1, col2 = st.columns([1, 2])

# Left Column - Overall Score
with col1:
    st.subheader(f"Candidate: {data['candidate_id']}")
    score = data['predicted_traits']['hireability_score']
    
    # Determine color
    if score >= 80:
        color = "green"
    elif score >= 65:
        color = "orange"
    else:
        color = "red"
        
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; border-radius: 10px; border: 2px solid {color};">
        <h1 style="color: {color}; font-size: 60px; margin: 0;">{score}%</h1>
        <h3 style="color: {color}; margin: 0;">{data['recommendation']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.write(f"**Session Duration:** {time.strftime('%M:%S', time.gmtime(data['session_duration_seconds']))} mins")
    st.write(f"**Primary Emotion:** {data['raw_cues_averages']['visual']['fer2013_primary_emotion'].title()}")

# Right Column - Radar Chart
with col2:
    st.subheader("Predicted Personality Traits")
    
    traits = data['predicted_traits']
    
    df_traits = pd.DataFrame(dict(
        r=[traits['stress_resistance'], traits['passion'], traits['confidence'], traits['cooperation'], traits['leadership'], traits['eye_contact']],
        theta=['Stress Resistance', 'Passion', 'Confidence', 'Cooperation', 'Leadership', 'Eye Contact']
    ))
    
    import plotly.express as px
    fig = px.line_polar(df_traits, r='r', theta='theta', line_close=True, range_r=[0,100], markers=True)
    fig.update_traces(fill='toself', line_color='#0056b3')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Bottom Row - Raw Data
st.subheader("Extracted Raw Cues & Evaluator Feedback")
col_visual, col_audio, col_traits = st.columns(3)

cues = data['raw_cues_averages']

with col_visual:
    st.write("### 🎥 Visual Metrics")
    st.write(f"- **Smile Score (FER):** {cues['visual']['smile_score']} / 1.0")
    st.write(f"- **Eye Opening Distance:** {cues['visual']['eye_opening_distance']} px")
    st.write(f"- **Lip Corner Distance:** {cues['visual']['lip_corner_distance']} px")

with col_audio:
    st.write("### 🎤 Audio / Text Metrics")
    st.write(f"- **Avg Pitch (F0):** {cues['audio']['average_pitch_hz']} Hz")
    st.write(f"- **Intensity:** {cues['audio']['intensity_db']} dB")
    st.write(f"- **Verbal Sentiment:** {cues['lexical']['vader_sentiment_compound']} (VADER)")

with col_traits:
    st.write("### 🧠 Regression Output")
    st.write(f"- **Stress Resistance:** {traits['stress_resistance']}%")
    st.write(f"- **Passion:** {traits['passion']}%")
    st.write(f"- **Leadership:** {traits['leadership']}%")
    st.write(f"- **Cooperation:** {traits['cooperation']}%")
    
if st.button("Refresh Data"):
    st.rerun()
