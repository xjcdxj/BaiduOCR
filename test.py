import re

a = "file:///C:/Users/YuXjc/Pictures/批注 2019-11-11 205119.png"
result = re.match(r'file:///(.+)', a)
print(result.groups(1))
