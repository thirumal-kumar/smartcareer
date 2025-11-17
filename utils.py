def create_user_profile_text(edu, tech_skills, soft_skills, goal):
    tech = ", ".join(tech_skills) if tech_skills else "None"
    soft = ", ".join(soft_skills) if soft_skills else "None"

    return (
        f"Education: {edu}. "
        f"Technical skills: {tech}. "
        f"Soft skills: {soft}. "
        f"Career goal: {goal}."
    )

def simple_rationale(course_row, user_profile):
    title = course_row["title"]
    skills = course_row["skill_tags"]
    prereq = course_row["prerequisites"]

    if prereq.lower() in ["none", "nan", ""]:
        prep_msg = "No prerequisites required."
    else:
        prep_msg = f"Prerequisites include: {prereq}."

    return (
        f"The course '{title}' aligns with your interests in {skills}. "
        f"{prep_msg}"
    )
