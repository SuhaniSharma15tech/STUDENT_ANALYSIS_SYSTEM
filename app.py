import os
import requests
import json
import time
from flask import Flask,render_template,request,jsonify
from utilities import analyze
from dotenv import load_dotenv

load_dotenv()  # This specifically looks for the .env file in the current folder

# This pulls the key from Render's environment variables. 
# It keeps our API key safe and off of GitHub.
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")


app=Flask("__main__")

def get_ai_insights(data_summary):
    """
    Sends the data summary to Gemini API and returns structured JSON insights.
    """
    if not GEMINI_API_KEY:
        return {"error": "API Key not found"}
    # Updated URL in app.py
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
        
    
    prompt = f"""
    You are an expert Educational Data Scientist. Analyze the following student performance data:
    {json.dumps(data_summary)}

    TASK:
    1. MEGA PIE: Provide 2 non-obvious insights regarding the disconnect between student 'Persona' distribution and 'Academic' outcomes.
    2. TRAJECTORY: Provide 3 non-obvious insights from the trajectory mappings.
    3. SPIDER CHARTS: Infer deep behavioral traits for each persona based on attribute scores.
    4. GENDER & SCHOOL: Provide 2 non-obvious insights for each.
    5. ACTIONABLE STRATEGIES: Suggest specific interventions for each persona.

    CONSTRAINTS:
    - Use short, direct bullet points.
    - Focus on high-value analysis, not descriptions.
    - Return ONLY a valid JSON object.

    REQUIRED JSON FORMAT:
    {{
        "mega_pie_insights": "• Insight 1\\n• Insight 2",
        "trajectory_wise_persona": "• Insight 1\\n• Insight 2\\n• Insight 3",
        "spider_chart_inferences": "• Persona: Inference...",
        "gender_insights": "• Insight 1\\n• Insight 2",
        "school_insights": "• Insight 1\\n• Insight 2",
        "actionable_recommendations": "• Persona: Action..."
    }}
    
    """

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generation_config": {
            "response_mime_type": "application/json" # This now works because of 'v1beta'
        }
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        
        # Extract the text content from Gemini's response structure
        content_text = result['candidates'][0]['content']['parts'][0]['text']
        return json.loads(content_text)
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err.response.text}") # This tells you the EXACT reason
        return {"error": "Gemini API rejected the request"}
    except Exception as e:
        print(f"General Error: {e}")
        return {"error": "Failed to generate AI insights"}



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze_data():
    file = request.files["csv_file"]
    results = analyze.chart_ready(file) 
    
    # Generate AI insights based on the results
    ai_insights = get_ai_insights(results)
    
    # Merge insights into the main results object
    results['AI_insights'] = ai_insights
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)