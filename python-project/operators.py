num1 = 10;
num2 = 3;

#? Operators:
#* Airthmetic Operators:
print("          ");
print("arithmetic operators:");

print("num1 + num2 is ", num1 + num2); # Addition
print("num1 - num2 is ", num1 - num2); # Subtraction
print("num1 * num2 is ", num1 * num2); # Multiplication
print("num1 / num2 is ", num1 / num2); # Division
print("num1 // num2 is ", num1 // num2); # Floor Division
print("num1 % num2 is ", num1 % num2); # Modulus
print("num1 ** num2 is ", num1 ** num2); # Exponentiation


# * Assignment Operators:
print("          ");
print("assignment operators:");
a = 4;
# a += 2; # now a = a + 2
# a -= 2; # now a = a - 2
a *= 2; # now a = a * 2
a /= 2; # now a = a / 2
a %= 2; # now a = a % 2
a **= 2; # now a = a ** 2
a //= 2; # now a = a // 2

print(a);


#* Comparision Operators:
#? Comparison Operators are used to compare two values. It returs a boolean value. 

x = 8;
y = 3;
z = 8;
print("          ");
print("comparison operators:");
print(x > y); # Greater than
print(x < y); # Less than
print(x != y); # Not equal to
print(x == y); # Equal to
print(x >= y); # Greater than or equal to
print(x <= y); # Less than or equal to
print(x == z); # Equal to

#* Logical Operators:
#? Logical Operators are used to combine conditional statements. It returns a boolean value.
print("          ");
print("logical operators:");
print(x > y and x == z); # and returns true if both statements are true
print(x > y or x == z); # or returns true if one of the statements is true
print(not(False)); # not returns true if the statement is false
print(not True); # not returns false if the statement is true
