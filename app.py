import os
import json
import random

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

def select_recommend_type():
    print("\n추천 방식을 선택하세요")
    print("1: 상황 기반 추천 (식사 시간 + 인원)")
    print("2: 태그 기반 추천")

    return input("번호 입력: ").strip()

def get_condition_input():
    print("=== 메뉴 추천 프로그램 ===")

    meal_time = input("식사 시간 입력 (아침/점심/저녁): ").strip()

    print("인원 수 선택")
    print("1: 1명")
    print("2: 2명")
    print("3: 3명")
    print("4: 4명")
    print("5: 5명 이상")

    people = int(input("번호 입력: ").strip())

    return meal_time, people

def collect_all_tags(menus):
    tag_set = set()

    for menu in menus:
        for tag in menu["tags"]:
            tag_set.add(tag)
    
    return sorted(tag_set)

def get_tag_input(all_tags):
    print("\n원하는 태그를 선택하세요 (복수 선택 가능)")

    for idx, tag in enumerate(all_tags, start=1):
        print(f"{idx}: {tag}")

    raw_input = input("번호 입력 (쉼표로 구분, 예: 1,3): ").strip()
    selected_indexes = raw_input.split(",")

    selected_tags = []

    for idx in selected_indexes:
        idx = idx.strip()
        if idx.isdigit():
            num = int(idx)
            if 1 <= num <= len(all_tags):
                selected_tags.append(all_tags[num - 1])

    return selected_tags

def recommend_by_condition(menus, meal_time, people):
    candidates = []

    for menu in menus:
        if meal_time in menu["meal_time"]:
            if menu["min_people"] <= people <= menu["max_people"]:
                candidates.append(menu)
        
    if not candidates:
        return None

    return random.choice(candidates)

def recommend_by_tags(menus, selected_tags):
    candidates = []

    for menu in menus:
        if any(tag in menu["tags"] for tag in selected_tags):
            candidates.append(menu)

    if not candidates:
        return None

    return random.choice(candidates)

def print_result(menu):
    print("\n=== 추천 결과 ===")

    if menu is None:
        print("조건에 맞는 메뉴가 없습니다.")
        return

    print(f"🍽 메뉴 이름: {menu['name']}")
    print(f"👥 추천 인원: {menu['min_people']} ~ {menu['max_people']}명")
    print(f"🕒 가능한 시간: {', '.join(menu['meal_time'])}")
    print(f"🏷 태그: {', '.join(menu['tags'])}")

def main():
    menus = load_all_menus()
    all_tags = collect_all_tags(menus)

    print("=== 메뉴 추천 프로그램 ===")
    mode = select_recommend_type()

    if mode == "1":
        meal_time, people = get_condition_input()
        result = recommend_by_condition(menus, meal_time, people)

    elif mode == "2":
        selected_tags = get_tag_input(all_tags)
        result = recommend_by_tags(menus, selected_tags)

    else:
        print("잘못된 입력입니다.")
        return

    print_result(result)

if __name__ == "__main__":
    main()