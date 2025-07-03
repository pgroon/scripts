import random

def char_to_numeric_value(char):
    # Convert a character to its numeric value (a=1, b=2, ..., z=26)
    if char.isalpha():
        return ord(char.lower()) - ord('a') + 1
    elif char == ' ':
        return 0  # Encode space as 0
    else:
        return None  # Ignore punctuation

#def make_tuple():
#    num1 = random.randint(0, 9)
#    num2 = random.randint(0, 9)
#    tuple_sum = num1 + num2
#    result = [num1, num2, tuple_sum]
#    return result

def generate_numbers(target_value):
    # Generate two random positive, single-digit numbers
    num1 = random.randint(0, 9)
    num2 = random.randint(0, 9)

    # Check if the sum of the first two numbers is too great, or too small to reach the target value with a third number:
    while (num1 + num2 > target_value) | (num1 + num2 + 9 < target_value):
        # If true, regenerate both numbers
        num1 = random.randint(0, 9)
        num2 = random.randint(0, 9)

    # Calculate the third number to make the sum equal to the target value
    num3 = (target_value - (num1 + num2))

    # Randomize the order of num1, num2, and num3
    sequence = [num1, num2, num3]
    random.shuffle(sequence)

    # Convert the triple to a string without brackets or commas
    sequence_str = ''.join(map(str, sequence))

    return sequence_str

def process_input(input_filename, output_filename):
    with open(input_filename, 'r') as input_file, open(output_filename, 'w') as output_file:
        sequences = []  # Store sequences before writing to output file
        for char in input_file.read().replace('\n', ''):
            numeric_value = char_to_numeric_value(char)
            if numeric_value is not None:
                # Use the numeric value directly without multiplying by 10
                target_value = numeric_value
                sequence_str = generate_numbers(target_value)
                sequences.append(sequence_str)

                # Write sequences to output file with a space between each three-digit sequence
                if len(sequences) == 10:
                    output_file.write(' '.join(sequences) + ' ')
                    sequences = []  # Clear the list for the next sequence

        # Write the remaining sequences to the output file
        if sequences:
            output_file.write(' '.join(sequences))

# Set input and output filenames
input_filename = "input.txt"
output_filename = "output.txt"

# Process input and write output
process_input(input_filename, output_filename)
