import streamlit as st
from recommender import Recommender
from utils import create_user_profile_text
import json
import numpy as np

st.set_page_config(page_title="SmartCareer", layout="centered")
st.title("🎯 SmartCareer – AI Course & Certification Recommender")

reco = Recommender("course_catalog.csv")

# -------------------------------------------------------
# FUNCTIONAL ADDITION 1: MAJOR / DEGREE
# FUNCTIONAL ADDITION 2: PREFERRED DURATION
# -------------------------------------------------------
with st.form("form"):
    edu = st.selectbox("Education Level", ["High School", "Bachelors", "Masters", "PhD"])
    
    major = st.text_input("Major / Degree (e.g., Computer Science, Biotechnology)")  # NEW FIELD
    
    tech = st.multiselect(
        "Technical Skills",
        ["python","r","sql","ml","dl","cloud","devops","docker",
         "kubernetes","pandas","tensorflow","nlp","opencv","excel"]
    )
    
    soft = st.multiselect(
        "Soft Skills",
        ["communication","leadership","teamwork","problem-solving","time-management"]
    )
    
    goal = st.text_input("Career Goal", "Data Scientist")

    preferred_duration = st.selectbox(   # NEW FIELD
        "Preferred Study Duration",
        ["No preference", "1–3 months", "3–6 months", "6–12 months"]
    )
    
    level = st.selectbox("Self-assessed Level", ["Beginner","Intermediate","Advanced"])
    
    submit = st.form_submit_button("Get Recommendations")

# Build user text with new major field included
def build_user_text(edu, major, tech, soft, goal):
    return (
        f"Education: {edu}. Major: {major}. "
        f"Technical skills: {', '.join(tech)}. "
        f"Soft skills: {', '.join(soft)}. "
        f"Career goal: {goal}."
    )

# -------------------------------------------------------
# FUNCTIONAL ADDITION 3: SKILL-GAP EXPLANATION
# -------------------------------------------------------
def skill_gap_explanation(user_skills, course_skills):
    course_sk = [s.strip() for s in course_skills.split(",")]
    missing = [s for s in course_sk if s not in user_skills]

    if not missing:
        return "You already have the core skills needed for this course."
    else:
        return "You are missing these skills: " + ", ".join(missing)

# -------------------------------------------------------
# FUNCTIONAL ADDITION 4: TIMELINE EXPLANATION
# -------------------------------------------------------
def timeline_explanation(course):
    duration = int(str(course["duration_weeks"]).split('.')[0])
    level = course["level"]

    if duration <= 12:
        return (
            "This is a short-term course because it can be completed within 1–3 months, "
            "and it builds foundational skills."
        )
    else:
        return (
            "This is a long-term course because it requires more than 3 months to complete "
            "and builds deeper or advanced expertise."
        )


# -------------------------------------------------------
# RECOMMENDATION BLOCK
# -------------------------------------------------------
if submit:
    user_text = build_user_text(edu, major, tech, soft, goal)
    
    recs = reco.recommend(
        user_text=user_text,
        user_skills=tech,
        user_level=level,
        top_k=10
    )

    st.subheader("📌 Top Course Matches")

    for r in recs:
        gap_reason = skill_gap_explanation(tech, r["skill_tags"])
        time_reason = timeline_explanation(r)

        st.markdown(f"""
### {r['title']} ({r['provider']})
**Level:** {r['level']}  
**Duration:** {r['duration_weeks']} weeks  
**Fit Score:** {r['fit_score']} / 100  
**Skills:** {r['skill_tags']}  
**Prep Required:** {r['prep_required']}  
[View Course]({r['link']})

**Why recommended:**  
- {gap_reason}  
- {time_reason}

---
""")

    # -------------------------------------------------------
    # JSON SAFE EXPORT (from previous fix)
    # -------------------------------------------------------
    def clean_for_json(data):
        cleaned = []
        for item in data:
            new_item = {}
            for k, v in item.items():
                if k == "embedding":
                    continue
                if isinstance(v, (np.float32, np.float64)):
                    v = float(v)
                if isinstance(v, (np.int32, np.int64)):
                    v = int(v)
                if isinstance(v, (np.bool_)):
                    v = bool(v)
                try:
                    json.dumps(v)
                    new_item[k] = v
                except:
                    new_item[k] = str(v)
            cleaned.append(new_item)
        return cleaned

    cleaned_recs = clean_for_json(recs)

    st.subheader("📥 Download JSON Output")
    st.download_button(
        "Download Recommendations JSON",
        json.dumps(cleaned_recs, indent=2),
        file_name="recommendations.json",
        mime="application/json"
    )
