# Arguments and keyword arguments
# def hi(*args):
#     for arg in args:
#         print(arg)
# hi("hi",19,"Deve",True)

# def hii(**kwargs):
#     for key,values in kwargs.items():
#         print(f"{key} = {values}")
# hi("hi",19,"Deve",True)
# hii(name="devesh",add="pune",no="1234567890")

#palindrome
# value = input("Please enter :")
# if value == value[::-1]:
#     print("Palindrome")
# else:print("Not a palindrome")

# Taking input from user as a list
# a=[1,1,2,3,4,5,5,6,7,7,8,9,9,0]
# u=[]
# s=[]
# for i in a:
#     if i not in u:
#         u.append(i)
#     elif i not in s:
#         s.append(i)
# print(s)


# def func(n):
#     v=0
#     while v < n:
#         yield v
#         v += 1
# for val in func(10):
#     print(val)

# decorator
# def tp(func):
#     def inner():
#         print("First")
#         func()
#         print("last")
#     return inner
# def baher():
#     print("middle")
    
# baher=tp(baher)
# baher()
 

# 
# value = int(input("value :"))
# n1,n2=0,1
# sum=0

# if value<=0:
#     print("Value must be Positive")
# elif value==1:
#     print(n2)
# while sum<value:
#        print(n1)
#        nth = n1 + n2
#        n1 = n2
#        n2 = nth
#        sum += 1

# from flask import Flask

# app=Flask(__name__)

# @app.route('/')
# def basic():
#     return "Hello World"

# app.run()
a=[]
def bas(n):
    v=1
    while v<n:
        yield v
        v+=1
for i in bas(10):
    a.append(i)
print(a)

def first(func):
    def main():
        print("First")
        func()
        print("last")
    return main
def middle():
    print("Middle")
    
middle=first(middle)
middle()