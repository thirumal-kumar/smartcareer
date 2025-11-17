from recommender import Recommender

def test_recommender():
    rc = Recommender("course_catalog.csv")

    user = "Education: Bachelors. Technical skills: python, sql. Soft skills: communication. Career goal: Data Analyst."
    out = rc.recommend(user_text=user, user_skills=["python","sql"], user_level="Beginner", top_k=5)

    assert isinstance(out, list)
    assert len(out) > 0
    print("Recommender working ✔")

if __name__ == "__main__":
    test_recommender()
