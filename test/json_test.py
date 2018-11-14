import json

json_str = [{"idx":0, "range":0, "angle":0, "radian":0, "x":0, "y":0}]

print(json_str)

append_json = {"idx":1, "range":1, "angle":1, "radian":1, "x":1, "y":1}

json_str.append(append_json)

append_json = {"idx":2, "range":2, "angle":2, "radian":2, "x":2, "y":2}

json_str.append(append_json)

print(json_str)

for data in json_str:
    print(data)


update_json = {"idx":1, "range":3, "angle":3, "radian":3, "x":3, "y":3}

for data in json_str:
    if data["idx"] == update_json["idx"] and data["range"] <= update_json["range"]:
        data.update(update_json)

print(json_str)
