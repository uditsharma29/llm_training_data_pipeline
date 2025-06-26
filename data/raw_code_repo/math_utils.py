import math

def calculate_sum(numbers):
  """
  This function takes a list of numbers and returns their sum.
  It handles integers and floats.
  """
  total = 0
  for number in numbers:
    total += number
  return total

def is_prime(n):
  """Checks if a number is prime using a simple algorithm."""
  if n <= 1:
    return False
  for i in range(2, int(n**0.5) + 1):
    if n % i == 0:
      return False
  return True

# This function has no docstring and should be ignored by our script.
def get_pi():
    return math.pi 