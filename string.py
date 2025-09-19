#python string
a = "hello"
print(a)
print(len(a))
bv = "ayalaa aaa "
print("aaa" in bv)
if True:
    print("aaa is in bv")

#slicing string 
a = "Ayala Tileuzhan"
print(a[1:4]) #from index 1 to 3
print(a[:6]) #from index 0 to 5

#Modify strings 
x = "Helloo W "
print(x.upper())
print(x.lower())
print(x.strip())#removes whitespace from the beginning or at the end
print(x.replace("H", "A"))
print(x.split("W"))

#concatenate strings
a = "lll"
b = "aaa"
print(a + " " + b)


#format strings 
price = 60
cvc = f"the price: {price}"
print(cvc)

#escape characters 
sds = "i am soo \"tired\" uhhh "
print(sds)


#string methods 
a = "hEllo world"
print(a.capitalize())
print(a.casefold())
print(a.upper())