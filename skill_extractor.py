import spacy

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Common tech skills list
SKILLS_DB = [
"python","java","c++","sql","html","css","javascript","react","nodejs",
"django","flask","machine learning","deep learning","nlp","tensorflow",
"pytorch","pandas","numpy","excel","powerbi","tableau","aws","docker",
"kubernetes","linux","git","api","android","kotlin","swift",
"data analysis","statistics","spark","hadoop","mongodb","postgresql",
"data visualization","computer vision","transformers","ai"
]

def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS_DB:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))