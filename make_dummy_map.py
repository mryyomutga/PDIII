import numpy as np
import json
import pprint

data = []
length = 3000

for i in range(360):
    dt = {"idx":i, "range":length, "angle":i, "radian":np.radians(i), "x":length*np.cos(np.radians(i)), "y":length*np.sin(np.radians(i))}
    data.append(dt)

with open("./map_data/dummy_map.json", "w") as f:
    json_dump = {"origin":{"x":200, "y":200}, "data":data}
    json.dump(json_dump, f, indent=4)
