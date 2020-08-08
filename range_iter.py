def main():
    x = input("Enter list: ")
    lst = x.split()
    for i in range(len(lst)-1, -1, -1):
        print(lst[i])
