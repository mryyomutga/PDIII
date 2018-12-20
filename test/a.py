a = [{"a":0, "b":0},{"a":2, "b":2}]
b = []
c = []

for i in a:
    b.append(i)

for i in a:
    c.append(i.copy())

for i in a:
    i["a"] = 1

print(a, b, c)
