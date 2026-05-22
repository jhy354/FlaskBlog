import json
from pathlib import Path
from datetime import datetime

from flask import Flask, render_template, abort

app = Flask(__name__)

DATA_DIR = Path(__file__).parent
CONTENT_DIR = DATA_DIR / "content"


def load_posts():
    with open(DATA_DIR / "posts.json", encoding="utf-8") as f:
        posts = json.load(f)
    for post in posts:
        post["date"] = datetime.strptime(post["date"], "%Y-%m-%d")
    return posts


def load_reports():
    with open(DATA_DIR / "reports.json", encoding="utf-8") as f:
        reports = json.load(f)
    return reports


def load_content(post_id):
    file = CONTENT_DIR / f"{post_id}.html"
    if not file.exists():
        return None
    return file.read_text(encoding="utf-8")


def get_courses(reports_list):
    seen = set()
    result = []
    for r in reports_list:
        if r["course"] not in seen:
            seen.add(r["course"])
            result.append(r["course"])
    return result


posts = load_posts()
reports = load_reports()


@app.route("/")
def index():
    return render_template("index.html", posts=posts[:2], reports=reports[:2],
                           total_posts=len(posts), total_reports=len(reports),
                           now=datetime.now(), nav_active="home",
                           page_title="My Blog")


@app.route("/blog")
def blog():
    return render_template("blog.html", posts=posts,
                           now=datetime.now(), nav_active="blog",
                           page_title="文章 — My Blog")


@app.route("/post/<int:post_id>")
def post_detail(post_id):
    post = next((p for p in posts if p["id"] == post_id), None)
    if post is None:
        abort(404)
    content = load_content(post_id)
    if content is None:
        abort(404)
    return render_template("post.html", post=post, content=content,
                           nav_active="blog", now=datetime.now(),
                           page_title=post["title"] + " — My Blog")


@app.route("/reports")
def reports_page():
    courses = get_courses(reports)
    return render_template("reports.html", reports=reports, courses=courses,
                           nav_active="reports",
                           page_title="实验报告 — My Blog",
                           now=datetime.now())


@app.route("/reports/<int:report_id>")
def report_detail(report_id):
    report = next((r for r in reports if r["id"] == report_id), None)
    if report is None:
        abort(404)
    courses = get_courses(reports)
    return render_template("report.html", report=report, courses=courses,
                           nav_active="reports",
                           page_title=report["title"] + " — My Blog",
                           now=datetime.now())


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", nav_active="",
                           page_title="页面未找到 — My Blog",
                           now=datetime.now())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
