import os
import json
import random

def load_all_menus(data_dir = "data"):
    all_menus = []

    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            file_path = os.path.json(data_dir, filename)

            with open(file_path, "r", endcoding="utf-8") as f:
                data = json.load(f)
                menus = data.get("menus", [])
                all_menus.extend(menus)

    return all_menus

def get_user_input():
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

def recommend_menu(menus, meal_time, people):
    candidates = []

    for menu in menus:
        if meal_time in menu["meal_time"]:
            if menu["min_people"] <= people <= menu["max_people"]:
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
    meal_time, people = get_user_input()
    result = recommend_menu(menus, meal_time, people)
    print_result(result)

if __name__ == "__main__":
    main()