import markdown2

def convert(s):
    s = markdown2.markdown(s)
    return s


string =input ("String ? ")
string2 = convert(string)
print (string2)

