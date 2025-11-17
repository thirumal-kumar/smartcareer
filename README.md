# 🎯 SmartCareer – AI-Powered Course & Certification Recommender

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

SmartCareer is an **AI-powered learning path recommender** that analyzes a user’s **education**, **degree**, **technical skills**, **soft skills**, **career goal**, and **preferred study duration** to recommend the most relevant **courses, certifications, and learning programs**.

Built using **SentenceTransformers**, **Python**, and **Streamlit**, the system ranks courses, explains the reasoning, identifies skill gaps, and generates a personalized learning timeline.

---

# 🚀 Features

### ✅ Core Functionalities
- Intelligent course recommendations using **MiniLM sentence embeddings**
- Skill-gap analysis (identifies missing skills for each course)
- Prerequisite and level-aware matching
- Timeline classification (short-term vs long-term courses)
- Rich explanations for *why* each course is recommended
- Major/Degree input (NEW)
- Preferred study duration (NEW)
- JSON export of final recommendations (safe serialization)

### 🎨 UI & Experience
- Clean and simple Streamlit interface
- Instant feedback with top-ranked course list
- Human-readable cards
- Downloadable JSON output
- Zero setup beyond running `streamlit run app.py`

---

# 🧠 How It Works

### **1. Input Collection**
User provides:
- Education level  
- **Major/Degree**  
- Technical skills  
- Soft skills  
- Career goal  
- **Preferred study duration**  
- Self-assessed skill level  

---

### **2. Course Representation**
Each course includes:
- Title  
- Provider  
- Duration (weeks)  
- Prerequisites  
- Skill tags  
- Difficulty level  
- Link  

Stored in `course_catalog.csv` (50 curated entries).

---

### **3. Embedding-Based Matching**
- Converts user profile + course text into embeddings  
- Computes cosine similarity  
- Penalizes advanced courses for beginners  
- Penalizes missing prerequisites  
- Produces normalized **Fit Score (0–100)**  

---

### **4. Skill Gap Analysis**
Compares:
```
course.skill_tags vs user.tech_skills
```

Identifies:
- Matching skills  
- Missing skills  
- Required preparation  

---

### **5. Timeline Reasoning**
Short-term (≤12 weeks):  
> Ideal for foundational learning.

Long-term (>12 weeks):  
> Recommended for advanced specialization after basics.

---

# 📂 Project Structure

```
smartcareer/
│
├── app.py
├── recommender.py
├── utils.py
├── course_catalog.csv
├── sample_profiles.json
├── requirements.txt
└── tests.py
```

---

# 🛠 Installation

## 1. Clone the repository

```bash
git clone https://github.com/<your-username>/smartcareer.git
cd smartcareer
```

## 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the App

```bash
streamlit run app.py
```

Your browser will open at:

```
http://localhost:8501
```

---

# 📟 Example Output

```
Recommended Course: Python for Everybody
Fit Score: 92/100
Prep Required: No
Why recommended:
- You already have the relevant skills.
- Short-term course ideal for foundations.
```

---

# 🧪 Tests

```bash
python tests.py
```

Expected:

```
Recommender working ✔
```

---

# 🛠 Tech Stack

- Python 3.10+
- Streamlit
- SentenceTransformers
- Torch
- Pandas / NumPy

---

# 📜 License

MIT License.

---

# ⭐ Support

If you found this project useful, please give it a ⭐ on GitHub!
