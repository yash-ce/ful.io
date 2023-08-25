import re

def is_valid_contact_number(number):
    # Define the regular expression pattern to match valid contact numbers
    pattern = r'^(\+\d{1,2}\s?)?(\d{1,4}[-\.\s]?)?\(?\d{3}\)?[-\.\s]?\d{3}[-\.\s]?\d{4}$'

    # Use the re.match() function to check if the number matches the pattern
    if re.match(pattern, number):
        return True
    else:
        return False

# Test the function with example numbers
numbers = [
    "2124567890",
    "212-456-7890",
    "(212)456-7890",
    "(212)-456-7890",
    "212.456.7890",
    "212 456 7890",
    "+12124567890",
    "+1 212.456.7890",
    "+212-456-7890",
    "1-212-456-7890"
]

for number in numbers:
    if is_valid_contact_number(number):
        print(f"{number} is a valid contact number.")
    else:
        print(f"{number} is an invalid contact number.")
