
# === Python Debugging Exercises ===
## Exercise 1: average_calculator.py

def calculate_average(grades):
    total = 0
    count = 0
    for grade in grades:
        if isinstance(grade, (int, float)):
            total += grade
            count += 1
    if count == 0:
        return 0  # or raise an error if you prefer
    average = total / count
    return average
student_grades = [85, 90, "A", 92, 88]
avg = calculate_average(student_grades)
print("Average grade:", avg)
# Task: Debug the crash and make sure the function handles non-numeric values properly.

## Exercise 2: reverse_string.py
def reverse_string(s):
    reversed = ""
    for i in range(len(s) - 1, -1, -1):
        reversed += s[i]
    return reversed

print(reverse_string("hello"))

# Task: Use the debugger to identify the IndexError and fix the loop.


## Exercise 3: find_max.py
def find_max(numbers):
    max_value = -100000000000000
    for num in numbers:
        if num > max_value:
            max_value = num
    return max_value

print(find_max([-5, -10, -3]))

# Task: Step through with the debugger and observe why this doesn't work with negative numbers. Fix the logic.


## Exercise 4: fibonacci.py
def fibonacci(n):
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib

print(fibonacci(5))

# Task: Debug the crash caused by list index errors. Fix the logic using .append().


## Exercise 5: append_item.py
def append_item(item, item_list=[]):
    item_list=[]
    item_list.append(item)
    return item_list

print(append_item(1))
print(append_item(10))
print(append_item(3))

# Task: Fix the unexpected behavior caused by the mutable default argument.



# === Python Programming Exercises ===

## Exercise 1: Palindrome Checker
# Write a function `is_palindrome(s)` that checks whether a string is a palindrome.
# Example: is_palindrome("radar") -> True


def is_palindrome(s):
    s = s.lower()
    return s == s[::-1]
print(is_palindrome("Radar"))
## Exercise 2: Prime Number Finder
# Write a function `get_primes(n)` that returns a list of all prime numbers up to n.
def get_prime(n):
    primes = []
    for num in range(2, n + 1):
        for i in range(2, num):
            if num % i == 0:
                break
        else:
            primes.append(num)
    return primes


print(get_prime(20))

## Exercise 3: Word Frequency Counter
# Given a string of text, count the frequency of each word and return a dictionary.

def word_frequency_counter(text):
    # Heq disa prej pikësimeve
    for p in '.,!?':
        text = text.replace(p, '')

    words = text.lower().split()
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1

    return freq


# Test:
text = "Hello world! Hello, universe. Welcome to the world of code."
print(word_frequency_counter(text))


## Exercise 4: Shopping Cart
# Create a class `ShoppingCart` with methods to add, remove items, and calculate the total.
class ShoppingCart:
    def __init__(self):
        self.cart = {}

    def add_item(self, name, price, quantity=1):
        if name in self.cart:
            self.cart[name][1] += quantity
        else:
            self.cart[name] = [price, quantity]

    def remove_item(self, name, quantity=1):
        if name in self.cart:
            self.cart[name][1] -= quantity
            if self.cart[name][1] <= 0:
                del self.cart[name]

    def get_total(self):
        total = 0
        for item in self.cart.values():
            total += item[0] * item[1]
        return total


## Exercise 5: Student Gradebook
# Build a program that stores students and their grades, and allows:
# - Adding a new student
# - Adding grades
# - Getting average per student
class StudentGradebook:
    def __init__(self):
        self.students = {}  # format: {'student_name': [grades]}

    def add_student(self, name):
        if name not in self.students:
            self.students[name] = []
        else:
            print(f"{name} is already in the gradebook.")

    def add_grade(self, name, grade):
        if name in self.students:
            self.students[name].append(grade)
        else:
            print(f"{name} is not in the gradebook. Add them first!")

    def get_average(self, name):
        if name in self.students and self.students[name]:
            return sum(self.students[name]) / len(self.students[name])
        elif name in self.students:
            return 0  # No grades yet
        else:
            print(f"{name} is not in the gradebook.")
            return None

    def show_all_averages(self):
        for name, grades in self.students.items():
            avg = self.get_average(name)
            print(f"{name}: Average grade = {avg if avg is not None else 'N/A'}")
gradebook = StudentGradebook()

gradebook.add_student("Harry")
gradebook.add_student("Emma")
gradebook.add_grade("Harry", 85)
gradebook.add_grade("Emma", 100)
gradebook.add_grade("Emma", 234)


print(f"Harry's average: {gradebook.get_average('Harry')}")
print(f"Emma's average: {gradebook.get_average('Emma')}")

gradebook.show_all_averages()
