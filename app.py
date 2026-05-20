# app.py

from flask import Flask, render_template, request
from utils import extract_text, clean_text, extract_email, extract_phone
from skills import extract_skills
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Match Score Function
def match_score(resume, jd):

    tfidf = TfidfVectorizer()

    vectors = tfidf.fit_transform([resume, jd])

    score = cosine_similarity(vectors[0], vectors[1])

    return round(score[0][0] * 100, 2)


@app.route('/')
def home():

    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():

    try:

        file = request.files['resume']
        jd = request.form['jd']

        # Validation
        if file.filename == '':
            return render_template(
                'index.html',
                error="Please upload resume PDF."
            )

        if jd.strip() == '':
            return render_template(
                'index.html',
                error="Please enter job description."
            )

        filename = file.filename

        # Extract Resume Text
        text = extract_text(file)

        clean_resume = clean_text(text)

        clean_jd = clean_text(jd)

        # Extract Details
        email = extract_email(text)

        phone = extract_phone(text)

        # Skills Extraction
        resume_skills = extract_skills(clean_resume)

        jd_skills = extract_skills(clean_jd)

        # Matching Skills
        matched_skills = list(
            set(resume_skills) & set(jd_skills)
        )

        # Missing Skills
        missing_skills = list(
            set(jd_skills) - set(resume_skills)
        )

        # ATS Score
        score = match_score(clean_resume, clean_jd)

        # Recommendation
        if score >= 80:

            result = "Excellent Match"

            recommendation = "Highly Recommended for Interview"

            strength = "Strong Technical Profile"

        elif score >= 60:

            result = "Good Match"

            recommendation = "Can Be Considered"

            strength = "Average Profile"

        else:

            result = "Needs Improvement"

            recommendation = "Upskilling Recommended"

            strength = "Low Match Profile"

        # Suggestions
        suggestions = []

        if len(missing_skills) > 0:

            suggestions.append(
                f"Add skills like {', '.join(missing_skills)}"
            )

        if score < 70:

            suggestions.append(
                "Improve resume keywords based on job description."
            )

        if len(resume_skills) < 5:

            suggestions.append(
                "Add more technical skills and projects."
            )

        return render_template(

            'index.html',

            filename=filename,

            email=email,

            phone=phone,

            skills=resume_skills,

            matched_skills=matched_skills,

            missing_skills=missing_skills,

            score=score,

            result=result,

            recommendation=recommendation,

            strength=strength,

            suggestions=suggestions
        )

    except Exception as e:

        return render_template(
            'index.html',
            error=f"Error: {str(e)}"
        )


if __name__ == "__main__":

    app.run(debug=True)