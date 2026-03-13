from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename

from resume_parser import extract_text
from matcher import match_jobs
from skill_extractor import extract_skills

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Create uploads folder if not present
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Check allowed file types
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    # Check if file exists
    if "resume" not in request.files:
        return "No file uploaded"

    file = request.files["resume"]

    if file.filename == "":
        return "Please select a file"

    if not allowed_file(file.filename):
        return "Only PDF or DOCX files are allowed"

    # Secure file name
    filename = secure_filename(file.filename)

    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file.save(path)

    # Extract resume text
    resume_text = extract_text(path)

    # Extract skills
    skills = extract_skills(resume_text)

    # Match jobs
    jobs, score = match_jobs(" ".join(skills))

    # Best job
    best_job = jobs.iloc[0]

    job_skills = best_job["Skills"].split()

    # Skill gap analysis
    skill_gap = [s for s in job_skills if s not in skills]

    # Top jobs
    top_jobs = jobs.head(5)

    labels = top_jobs["Job Title"].tolist()
    scores = top_jobs["Match %"].tolist()

    return render_template(
        "result.html",
        tables=[top_jobs.to_html(classes="data", index=False)],
        skills=skills,
        score=score,
        best_job=best_job["Job Title"],
        gap=skill_gap,
        labels=labels,
        scores=scores
    )


if __name__ == "__main__":
    app.run(debug=True)