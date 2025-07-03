import re

def generate_conkyrc(input_file):
    # Read paragraphs from the input text file
    with open(input_file, 'r') as file:
        paragraphs = file.read().split('\n\n')  # Assuming paragraphs are separated by two newline characters

    # Format paragraphs as bullet points
    # "template0" is defined within .conkyrc
    bullet_points = ['${template0}  ' + re.sub(r'\n', '\n       ', paragraph) for paragraph in paragraphs]

    # Print the formatted bullet points to stdout
    print('\n'.join(bullet_points))

if __name__ == "__main__":
    input_file_path = '/home/groon/Downloads/todo.md'   # Change this to the path of your input text file

    generate_conkyrc(input_file_path)
