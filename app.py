import json

with open("data/korea.json", "r", encoding="utf-8") as f:
    data = json.load(f)

menus = data["menus"]
print(menus)