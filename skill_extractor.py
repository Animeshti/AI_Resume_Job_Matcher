import spacy

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Simple skill keywords list
SKILLS = [
    "python", "java", "c++", "html", "css", "javascript",
    "react", "nodejs", "django", "flask", "sql",
    "machine learning", "deep learning", "nlp",
    "data analysis", "pandas", "numpy", "tensorflow", "pytorch"
]


def extract_skills(text):
    doc = nlp(text.lower())

    found_skills = []

    for token in doc:
        if token.text in SKILLS:
            found_skills.append(token.text)

    return list(set(found_skills))  