# 1
def generate_squares(n):
    for i in range(1, n + 1):
        yield i ** 2
for i in generate_squares(int(input())):
    print(i, end=" ")
print()

# 2
def even_numbers(n):
    for i in range(0, n + 1):
        if i % 2 == 0:
            yield i
print(",".join(str(i) for i in even_numbers(int(input()))))

# 3
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i
for i in divisible_by_3_and_4(int(input())):
    print(i, end=" ")
print()

# 4
def squares_range(a, b):
    for i in range(a, b + 1):
        yield i ** 2
a, b = map(int, input().split())
for i in squares_range(a, b):
    print(i, end=" ")
print()

# 5
def countdown(n):
    while n >= 0:
        yield n
        n -= 1
for i in countdown(int(input())):
    print(i, end=" ")
print()

# 6
from datetime import date, timedelta, datetime
print(date.today() - timedelta(days=5))

# 7
today = date.today()
print(today - timedelta(days=1))
print(today)
print(today + timedelta(days=1))

# 8
now = datetime.now()
print(now.replace(microsecond=0))

# 9
d1 = datetime(2025, 10, 1, 12, 0, 0)
d2 = datetime(2025, 10, 8, 12, 0, 0)
print((d2 - d1).total_seconds())

# 10
import math
print(math.radians(float(input())))

# 11
h = float(input())
a = float(input())
b = float(input())
print(0.5 * (a + b) * h)

# 12
n = int(input())
s = float(input())
print((n * s ** 2) / (4 * math.tan(math.pi / n)))

# 13
base = float(input())
height = float(input())
print(base * height)

# 14
import json
with open('sample-data.json') as f:
    data = json.load(f)
print("DN Description Speed MTU")
for item in data["imdata"]:
    k = next(iter(item))
    a = item[k]["attributes"]
    print(a["dn"], a["descr"], a["speed"], a["mtu"])
