

# REGEX
import re


string = "There are 123 apples and 456 bananas."
pattern = '\d+'
result = re.findall(pattern, string)
print(result)

string = """My email
addresses are example@example.com and test@test.org."""
pattern = r'\b[\w._%+-]+@[\w.-]+\.[a-zA-Z]{2,}\b'
result = re.search(pattern, string)
print(result.group())


string = 'hello 12 hi 89. Howdy 34'
pattern = r'\d+'
result = sum(float(x) for x in re.findall(pattern, string))
print(result)


array = ["apple", "banana", "cherry", "avocado", "blueberry"]
pattern = r'^a|^b'
result = [x for x in array if re.match(pattern, x)]
print(result)

string = "My phone number is 123-456-7890. Call me at 987-654-3210."
pattern = r'\b\d{3}-\d{3}-\d{4}\b'
result = re.sub(pattern, r'PHONE', string)
print(result)

string = "My phone number is 2.3 Call me at"
pattern = r'\b[+-]?\d+\b'

if re.search(pattern, string):
    print("Found a number in the string.")
else:
    print("No numbers found in the string.")
