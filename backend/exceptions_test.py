try:
    number = int(input("Please enter a number to divide by 1: "))
    print(1/number)
except ZeroDivisionError:
    print("You cannot divide by 0 DUMBASS")
except TypeError:
    print("We asked to input a number")
except Exception:
    print("Something went wrong")
finally:
    print("Do some cleanup")