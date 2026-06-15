import requests
from flask import Flask, render_template, request

app = Flask(__name__)


def fetch_github_profile(username):
    user_url = f"https://api.github.com/users/{username}"
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"

    user_response = requests.get(user_url)
    repos_response = requests.get(repos_url)

    if user_response.status_code != 200:
        return None

    user_data = user_response.json()
    repos_data = repos_response.json()

    repos_data = sorted(
        repos_data,
        key=lambda repo: repo["pushed_at"],
        reverse=True
    )
    if repos_data:
        repo_name = repos_data[0]["name"]
        if len(repo_name) > 18:
            most_active_repo = repo_name[:18] + "..."
        else:
            most_active_repo = repo_name
    else:
        most_active_repo = "N/A"

    total_repos = len(repos_data)
    total_stars = sum(repo["stargazers_count"] for repo in repos_data)
    total_forks = sum(repo["forks_count"] for repo in repos_data)

    languages = {}

    for repo in repos_data:
        language = repo["language"]
        if language:
            languages[language] = languages.get(language, 0) + 1

    top_language = max(languages, key=languages.get) if languages else "N/A"

    followers = user_data.get("followers", 0)
    following = user_data.get("following", 0)

    activity_score = (
        total_repos * 2
        + total_stars * 3
        + total_forks * 2
        + followers * 2
    )

    health_score = round(
    ((total_repos*2)+(len(languages)*10))/100*100,
    2
    )

    if health_score >= 80:
        badge = "🏆 Excellent"
    elif health_score >= 50:
        badge = "⭐ Good"
    else:
        badge = "🌱 Growing"

    created_at = user_data.get("created_at", "")[:10]

    return {
        "username": username,
        "name": user_data.get("name"),
        "bio": user_data.get("bio"),
        "avatar": user_data.get("avatar_url"),
        "profile_url": user_data.get("html_url"),
        "followers": followers,
        "following": following,
        "public_repos": user_data.get("public_repos"),
        "total_repos": total_repos,
        "total_stars": total_stars,
        "total_forks": total_forks,
        "top_language": top_language,
        "activity_score": activity_score,
        "languages": languages,
        "repos": repos_data,
        "language_count": len(languages),
        "created_at": created_at,
        "health_score": health_score,
        "badge": badge,
        "most_active_repo": most_active_repo,
    }

issues = [
    {
        "title": "Fix Flask login bug",
        "tags": "python flask auth bug",
        "level": "beginner",
        "link": "https://github.com/pallets/flask/issues"
    },
    {
        "title": "Improve React dashboard UI",
        "tags": "react css frontend ui",
        "level": "intermediate",
        "link": "https://github.com/facebook/react/issues"
    },
    {
        "title": "Optimize MySQL query performance",
        "tags": "sql mysql database backend",
        "level": "intermediate",
        "link": "https://github.com/mysql/mysql-server/issues"
    }
]

def get_top_skills():
    skill_count = {}

    for issue in issues:
        tags = issue["tags"].split()

        for tag in tags:
            skill_count[tag] = skill_count.get(tag, 0) + 1

    top_skills = sorted(
        skill_count.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    return top_skills

def calculate_match(user_skills, issue_text):
    user_skills = [s.lower().strip() for s in user_skills]
    issue_text = issue_text.lower()

    matched = []
    for skill in user_skills:
        if skill in issue_text:
            matched.append(skill)

    if not user_skills:
        return 0, []

    score = int((len(matched) / len(user_skills)) * 100)
    return score, matched

def fetch_github_issues(repo_name):
    url = f"https://api.github.com/repos/{repo_name}/issues"

    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()

    issues = []

    for issue in data[:10]:

        if "pull_request" in issue:
            continue

        issues.append({
            "title": issue["title"],
            "url": issue["html_url"],
            "state": issue["state"]
        })

    return issues


@app.route("/skill-match", methods=["GET", "POST"])
def skill_match():
    matched_issues = []
    github_issues = []

    if request.method == "POST":
        skills = request.form.get("skills", "")
        repo = request.form.get("repo", "")

        if repo:
            github_issues = fetch_github_issues(repo)
        user_skills = skills.split(",")

        for issue in issues:
            text = issue["title"] + " " + issue["tags"]
            score, matched = calculate_match(user_skills, text)

            issue_copy = issue.copy()
            issue_copy["score"] = score
            issue_copy["matched"] = matched

            if score > 0:
                matched_issues.append(issue_copy)

        matched_issues.sort(key=lambda x: x["score"], reverse=True)
    
    top_skills = get_top_skills()
    return render_template(
        "skill_match.html",
        matched_issues=matched_issues,
        top_skills=top_skills,
        github_issues=github_issues
    )



@app.route("/", methods=["GET", "POST"])
def index():
    profile = None
    error = None

    if request.method == "POST":
        username = request.form.get("username")

        if username:
            profile = fetch_github_profile(username.strip())

            if profile is None:
                error = "GitHub user not found. Please enter a valid username."

    return render_template("index.html", profile=profile, error=error)


if __name__ == "__main__":
    app.run(debug=True)