import pandas as pd
from sentence_transformers import SentenceTransformer, util
import numpy as np

MODEL_NAME = "all-MiniLM-L6-v2"

class Recommender:
    def __init__(self, catalog_path="course_catalog.csv"):
        # Load CSV
        self.df = pd.read_csv(catalog_path)

        # Ensure clean text fields
        self.df["skill_tags"] = self.df["skill_tags"].fillna("").astype(str)
        self.df["prerequisites"] = self.df["prerequisites"].fillna("").astype(str)
        self.df["level"] = self.df["level"].fillna("").astype(str)

        # Build combined searchable text
        self.df["text"] = (
            self.df["skill_tags"].fillna("") + " " +
            self.df["prerequisites"].fillna("")
        )

        # Load model
        self.model = SentenceTransformer(MODEL_NAME)

        # Precompute embeddings
        self.df["embedding"] = self.df["text"].apply(
            lambda x: self.model.encode(x)
        )

    def _penalty(self, course_row, user_skills, user_level):
        """
        Apply prerequisite / level penalties.
        Returns: (penalty_multiplier, prep_required_flag)
        """

        # Convert everything to safe lowercase strings
        level = str(course_row["level"]).strip().lower()
        prereq = str(course_row["prerequisites"]).strip().lower()

        # 1) Beginners should avoid Advanced courses unless allowed
        if user_level.lower() == "beginner" and level == "advanced":
            return 0.0, True   # block

        # 2) If no prerequisites
        if prereq in ["none", "nan", "", "null"]:
            return 1.0, False

        # 3) Check missing prerequisites
        prereq_list = [p.strip() for p in prereq.split(",") if p.strip()]
        user_skill_text = " ".join(user_skills).lower()

        missing = [p for p in prereq_list if p not in user_skill_text]

        if missing:
            return 0.6, True   # penalize 40%

        return 1.0, False

    def recommend(self, user_text, user_skills, user_level, top_k=10):
        """
        Main recommendation function.
        """

        user_emb = self.model.encode(user_text)

        results = []
        similarities = []

        # Compute similarity for each course
        for _, row in self.df.iterrows():
            course_emb = row["embedding"]
            sim = float(util.cos_sim(user_emb, course_emb))

            penalty, prep = self._penalty(row, user_skills, user_level)
            adj = sim * penalty

            similarities.append(sim)

            results.append({
                **row.to_dict(),
                "raw_similarity": sim,
                "adjusted_similarity": adj,
                "prep_required": prep
            })

        # Normalize similarity score 0–100
        minv, maxv = min(similarities), max(similarities)
        for r in results:
            if maxv == minv:
                r["fit_score"] = 0
            else:
                r["fit_score"] = int(
                    100 * (r["raw_similarity"] - minv) / (maxv - minv)
                )

        # Sort by adjusted similarity (penalized)
        ranked = sorted(results, key=lambda x: x["adjusted_similarity"], reverse=True)

        return ranked[:top_k]


if __name__ == "__main__":
    # Simple manual test
    rc = Recommender("course_catalog.csv")
    user = "Education: Bachelors. Technical skills: python, sql. Soft skills: communication. Career goal: Data Analyst."
    out = rc.recommend(user_text=user, user_skills=["python", "sql"], user_level="Beginner", top_k=5)
    print(out)
