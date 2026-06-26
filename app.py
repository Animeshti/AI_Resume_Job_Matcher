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
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Check allowed file types
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "resume" not in request.files:
        return render_template("index.html", error="No file uploaded")

    file = request.files["resume"]

    if file.filename == "":
        return render_template("index.html", error="Please select a file")

    if not allowed_file(file.filename):
        return render_template("index.html", error="Only PDF or DOCX allowed")

    filename = secure_filename(file.filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(path)

    # Extract text
    resume_text = extract_text(path)

    if not resume_text:
        return render_template("index.html", error="Could not read file")

    # Extract skills
    skills = extract_skills(resume_text)

    if not skills:
        return render_template("index.html", error="No skills found")

    # Match jobs
    jobs, score = match_jobs(" ".join(skills))
    best_job = jobs.iloc[0]

    job_skills = best_job["Skills"].split()

    # Skill gap
    skill_gap = [s for s in job_skills if s not in skills]

    recommendations = []

    if "python" not in skills:
        recommendations.append("Learn Python")

    if "sql" not in skills:
        recommendations.append("Improve SQL skills")

    if "machine learning" not in skills:
        recommendations.append("Learn Machine Learning")

    if "projects" not in skills:
        recommendations.append("Add more projects to your resume")

    if not recommendations:
        recommendations.append("Your resume looks strong! 👍")

    # Top jobs
    top_jobs = jobs.head(5)

    labels = top_jobs["Job Title"].tolist()
    scores = top_jobs["Match %"].tolist()

    return render_template(
        "result.html",
        skills=skills,
        score=score,
        best_job=best_job["Job Title"],
        gap=skill_gap,
        labels=labels,
        scores=scores,
        recommendations=recommendations  
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)