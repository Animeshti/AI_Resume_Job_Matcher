import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_jobs(user_skills):
    jobs = pd.read_csv("jobs.csv")

    tfidf = TfidfVectorizer()
    vectors = tfidf.fit_transform(jobs["Skills"].tolist() + [user_skills])

    similarity = cosine_similarity(vectors[-1], vectors[:-1])

    jobs["Match %"] = similarity[0] * 100
    jobs = jobs.sort_values(by="Match %", ascending=False)

    return jobs, round(jobs.iloc[0]["Match %"], 2) 