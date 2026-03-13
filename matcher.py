import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def match_jobs(resume_text):

    jobs = pd.read_csv("jobs.csv")

    job_descriptions = jobs["Skills"].tolist()

    data = job_descriptions + [resume_text]

    cv = CountVectorizer()

    matrix = cv.fit_transform(data)

    similarity = cosine_similarity(matrix[-1], matrix[:-1])

    scores = similarity[0]

    jobs["Match %"] = (scores * 100).round(2)

    jobs = jobs.sort_values(by="Match %", ascending=False)

    resume_score = round(jobs["Match %"].max(), 2)

    return jobs, resume_score