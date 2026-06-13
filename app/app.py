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

    health_score = min(
        (total_repos * 2) +
        (followers * 3) +
        (len(languages) * 5),
        100
    )
    badge = "🏆 Open Source Contributor" if activity_score >= 40 else "🌱 Growing Contributor"

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
    }


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