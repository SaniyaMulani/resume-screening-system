# skills.py

skills_list = [

    "python",
    "java",
    "c",
    "c++",
    "sql",
    "html",
    "css",
    "javascript",
    "react",
    "nodejs",
    "mongodb",
    "machine learning",
    "data science",
    "data analysis",
    "excel",
    "power bi",
    "tableau",
    "aws",
    "cloud computing",
    "flask",
    "django",
    "communication",
    "teamwork",
    "leadership"
]


def extract_skills(text):

    found_skills = []

    text = text.lower()

    for skill in skills_list:

        if skill.lower() in text:

            found_skills.append(skill)

    return found_skills