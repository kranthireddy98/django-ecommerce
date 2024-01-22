# integer to decimal


import decimal

integer = 47
dec = decimal.Decimal(integer)
# print(dec)
# print(type(dec))


def fibonacci(n, fib_list = []):
  """
  Generates the Fibonacci sequence up to the nth number using recursion and returns it as a list.

  Args:
    n: The index of the last number in the desired Fibonacci sequence.
    fib_list: An optional list to store the Fibonacci numbers.

  Returns:
    A list containing the Fibonacci sequence up to the nth number.
  """

  if n == 0:
    # Base case: return an empty list for n = 0
    return fib_list

  elif n == 1:
    # Base case: append the first Fibonacci number (1) and return
    fib_list.append(0)
    return fib_list
  elif n == 2:
    # Base case: append the first Fibonacci number (1) and return
    fib_list.extend([0,1])
    return fib_list

  else:
    # Recursive calls: generate previous Fibonacci numbers and append the current one
    fib_list = fibonacci(n-1, fib_list)  # Generate Fibonacci numbers up to n-1
    fib_list.append(fib_list[-1] + fib_list[-2])  # Calculate the nth number and append
    return fib_list

# Print the Fibonacci sequence up to the 10th number
print(fibonacci(10))  # Output: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]