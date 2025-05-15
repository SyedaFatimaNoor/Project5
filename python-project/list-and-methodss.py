# ?List and Methods:
    # ""List is a collection of items in a particular order. Lists are mutable, meaning they can be changed. Lists are defined by having values between square brackets [ ]. This is a built in data type in Python. Lists can contain any data type, including other lists.""
l1 = [1, 2, 3, 4, "Noor", 5]
# print(type(l1));
# print(l1);


# List methods:
l1.remove("Noor");
print(l1);
l1.count(234);
l1.sort()
print(l1)
l1.pop(0) # remove the first element
print(l1)
l1.append(100) # add 100 at the end of the list
print(l1);
# l1.clear() # clear the list
# print(l1);
l1.extend([22, 34, 57]) # add the list [1, 2, 3] at the end of the list
print(l1);
print(l1.index(100)) # find the index of 22;