import random

s = input ("Search?")
list = ["item1", "item2", "item3", "Gaby1", "Gaby2", "New"]
entry = random.choice (list)
print (s.capitalize())
if (s in list) or (s.capitalize() in list):
    print ("Yes")
else:
    print ("No")

print (list)
print ("Random")
print (entry)