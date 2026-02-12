from flask import Flask, render_template, request
import os
import json
import random

app = Flask(__name__)

# 데이터 로딩
def load_all_menus(data_dir = "data"):
    all_menus = []

    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(data_dir, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                menus = data.get("menus", [])
                all_menus.extend(menus)

    return all_menus

# 태그 목록 수집
def collect_all_tags(menus):
    tag_set = set()

    for menu in menus:
        for tag in menu["tags"]:
            tag_set.add(tag)
    
    return sorted(tag_set)


# 상황 기반 추천 로직
def recommend_by_condition(menus, meal_time, people):
    candidates = []

    for menu in menus:
        if meal_time in menu["meal_time"]:
            if menu["min_people"] <= people <= menu["max_people"]:
                candidates.append(menu)
        
    if not candidates:
        return None

    return random.choice(candidates)

# 태그 기반 추천 로직 (하나라도 포함되면 후보)
def recommend_by_tags(menus, selected_tags):
    candidates = []

    for menu in menus:
        if any(tag in menu["tags"] for tag in selected_tags):
            candidates.append(menu)

    if not candidates:
        return None

    return random.choice(candidates)

# 메인 페이지
@app.route("/", methods=["GET", "POST"])
def index():
    menus = load_all_menus()
    all_tags = collect_all_tags(menus)
    result = None

    if request.method == "POST":
        mode = request.form.get("mode")

        if mode == "condition":
            meal_time = request.form.get("meal_time")
            people = int(request.form.get("people", 1))
            result = recommend_by_condition(menus, meal_time, people)
        
        elif mode == "tags":
            selected_tags = request.form.getlist("tags")
            result = recommend_by_tags(menus, selected_tags)
    
    return render_template(
        "index.html",
        tags=all_tags,
        result=result
    )

# 실행
if __name__ == "__main__":
    app.run(debug=True)
