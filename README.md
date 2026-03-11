# ai-interview-assistant-1
# AI Interview Assistant - Quick Start Guide

This project captures live video and audio to analyze candidate behavior (facial expressions, pitch, etc.) and predicts an overall "Hireability Score" along with specific personality traits.

## How to Run the Project

You need two terminal windows open in the `ai_interview_assistant` folder to run the full system.

### Step 1: Start the Dashboard
In your first terminal, launch the Streamlit web dashboard. This UI will automatically update when new interview data is generated:
```cmd
cd "g:\New folder (2)\ai_interview_assistant"
python -m streamlit run app.py
```
*Leave this terminal running. It will open `http://localhost:8501` in your browser.*

### Step 2: Start an Interview Recording
Open a **second** terminal. When the candidate is ready, start the camera and microphone recording:
```cmd
cd "g:\New folder (2)\ai_interview_assistant"
python main.py
```
*Your webcam light should turn on, and a window showing your face with landmark dots will appear.*

### Step 3: Stop the Recording & Analyze
Once the interview is over, you need to tell the system to stop analyzing and generate the final scores. You can do this in two ways:
1. **Press 'q'** while clicked on the video window.
2. OR, open a third terminal and run:
   ```cmd
   python stop.py
   ```

### Step 4: View the Results
Go back to your browser where the Streamlit dashboard (`http://localhost:8501`) is running. 
Click the **"Refresh Data"** button at the bottom of the page to see the new candidate's evaluation, consisting of their Smile Score, Audio traits, and final predicted Hireability percentage!
