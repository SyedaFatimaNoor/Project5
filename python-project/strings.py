# Strings and strings methods: 
#  Strings are a sequence of characters enclosed in single or double quotes.
#  Strings are immutable, meaning they cannot be changed after they are created.

name = "Noor ul ain Fatima";
print(name);
number = "1234567890";
print(name[0:3])  # Slicing: start from 0 and go all the way till 2 (3-1)
# print(name[a:b])  # Slicing: start from a and go all the way till b (b-1)

print(name.upper()); # Upper case
print(name.lower()); # Lower case
print(name.capitalize()); # Capitalize first letter
print(name.count("o")); # Count the number of times "o" appears in the string
print(name.find("o")); # Find the first occurrence of "o"
print(number.isnumeric()); # Check if the string is numeric
print(name.replace("Noor", "Farah")); # Replace "Noor" with "Punum"


