
---

# 🎓 Student Persona & Performance Analytics Dashboard

> An AI-Augmented Educational Intelligence System that transforms raw student data into actionable personas, behavioral insights, and intervention strategies.



## 📌 Overview

Traditional academic reporting focuses only on scores.
This project goes deeper.

The **Student Persona & Performance Analytics Dashboard** dynamically clusters student data to uncover hidden behavioral patterns, detect early disengagement signals, and generate AI-powered intervention insights.

It combines:

* 📊 Statistical clustering (K-Means)
* 🧠 AI-generated educational analysis (Google Gemini)
* 📈 Interactive visualization dashboard
* 🏫 School-wise & gender-wise breakdowns
* 🎯 Persona-level strategic recommendations





## 🚀 Why This Project Matters

Educational institutions often miss:

* Early disengagement signals
* Behavioral drivers behind academic performance
* Systemic gender or school-level disparities
* Actionable persona-based intervention strategies

This system transforms raw tabular data into:

* Meaningful student personas
* Academic trajectory clusters
* Behavioral spider profiles
* AI-driven strategic recommendations

It acts as a lightweight **Educational Decision Intelligence Engine**.



# 🧠 Models Used

## 1️⃣ 8-Feature Persona Model (5 Personas)

Clusters students based on behavioral + environmental factors:

* Study Hours
* Attendance
* Resource Access
* Motivation
* Sleep Hours
* Parental Involvement
* Tutoring
* Wellbeing
* Exam Scores

Outputs:

* Persona centroids
* Spider charts
* AI-based persona interpretation
* Actionable recommendations



## 2️⃣ 2-Feature Academic Trajectory Model (3 Clusters)

Clusters students into:

* 🟢 High Achievers & Engaged
* 🟡 Moderate / Average Performers
* 🔴 At-Risk / Low Engagement



# 📊 Dashboard Outputs



## 🏫 School-Wise Academic Distribution

### Public vs Private School Performance
<img width="1911" height="764" alt="image" src="https://github.com/user-attachments/assets/2e3115ea-b094-449a-b960-c73113b04ff8" />



**Insight Direction:**

* Compare systemic distribution differences
* Identify structural disparities
* Understand institutional impact patterns

---

## 🎭 8-Feature Persona Spider Charts

<img width="919" height="644" alt="image" src="https://github.com/user-attachments/assets/200d1a18-f5d7-427d-a0bc-7e1d523f2ae7" />




Personas include:

* Strivers
* At-Risk
* Stable Middle
* Elite Achievers
* Passive Beneficiaries
* High-Pressure

Each centroid is analyzed via AI to generate:

* Behavioral interpretation
* Hidden pattern detection
* Tailored interventions


## 👩‍🎓 Gender-Wise Academic Clustering

<img width="890" height="546" alt="image" src="https://github.com/user-attachments/assets/cbc261d2-801d-483c-b927-4deb3d9989cd" />



Breakdown:

* High Achievers
* Moderate Performers
* At-Risk Students

Used to detect:

* Performance skew
* Engagement asymmetry
* Structural participation gaps



## 🎯 Gender-Wise 8-Feature Personas

<img width="902" height="645" alt="image" src="https://github.com/user-attachments/assets/321d07c4-1800-477f-86ed-d6281e71b11a" />


Persona distribution analyzed across gender categories to surface:

* Behavioral divergence
* Motivation trends
* Support system gaps

---

# 🧠 AI-Powered Insight Engine

After clustering:

1. Dataset summary sent to Gemini API
2. AI returns structured JSON including:

```json
{
  "mega_pie_insights": "...",
  "trajectory_wise_persona": "...",
  "spider_chart_inferences": "...",
  "gender_insights": "...",
  "school_insights": "...",
  "actionable_recommendations": "..."
}
```

AI performs:

* Non-obvious pattern detection
* Persona naming & reasoning
* Strategic intervention suggestions
* Cross-dimensional analysis

---

# 🏗 System Architecture

```
CSV Upload
   ↓
Feature Engineering
   ↓
K-Means Clustering
   ↓
Gemini API (Insight Generation)
   ↓
Structured JSON Response
   ↓
Dashboard Rendering
```

---

# ⚙️ Tech Stack

* Python
* Flask
* Pandas
* NumPy
* Scikit-learn
* Requests
* python-dotenv
* Google Gemini API

---

# 📂 Project Structure

```
├── app.py
├── agent.py
├── utilities/
│   └── analyze.py
│   └── preprocessing.py
│   └── preprocessing.py
│    └── predict.py
├── templates/
│   └── index.html
├── static/
│   └── css/
│        └── style.css
│   └── js/
│        └── script.js
├── requirements.txt
└── README.md
```
---
# View Deployed Service
https://student-analysis-system.onrender.com

---

# 🛠 Installation

### 1️⃣ Clone Repository

```bash
git clone <your-repo-url>
cd <repo-folder>
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Add Environment Variables

Create a `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

---

# ▶️ Running the App

```bash
python app.py
```

Upload CSV → Click Analyze → View dashboard insights.

---

# 📈 Example Workflow

1. Upload student dataset (20 structured columns)
2. System clusters dynamically
3. Persona centroids generated
4. AI interprets behavioral patterns
5. Dashboard displays:

   * Distribution charts
   * Spider plots
   * Gender analysis
   * School-wise breakdown
   * Strategic interventions

---

# 🔮 Future Scope

* 🎮 Scenario Simulator
  Simulate feature changes and predict exam score shifts.

* 🗺 Student Spatial Mapping
  2D projection of students with clickable persona view.

* 🚨 Early Disengagement Detection Module

* 🔎 Outlier Detection (DBSCAN-based anomaly engine)

* 🧑‍🏫 Context-Aware Educational Counselor

---



---

# 👩‍💻 Contributors

* Suhani Sharma
* Ayushi Agrawal
* Mayank
* Neha Malhotra




