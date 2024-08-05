import re

def generate_conkyrc(input_file, output_file):
    # Read lines from the input text file
    with open(input_file, 'r') as file:
        lines = file.read().split('\n')  # Currently does not support multiline-todos
		
    # Format lines as bullet points
    bullet_points = ['${voffset 10}$alignr • ' + re.sub(r'\n', '$alignr\n       ', line) for line in lines]

    # Read the existing content of the .conkyrc file
    with open(output_file, 'r') as file:
        conkyrc_content = file.read()

    # Find the positions of #todo-start and #todo-end
    start_pos = conkyrc_content.find('#todo_start') + len('#todo_start')
    end_pos = conkyrc_content.find('#todo_end')

    # Replace the content between #todo-start and #todo-end with the formatted bullet points
    updated_conkyrc = conkyrc_content[:start_pos] + '\n'.join(bullet_points) + conkyrc_content[end_pos:]

    # Write the updated content to the .conkyrc file
    with open(output_file, 'w') as file:
        file.write(updated_conkyrc)

if __name__ == "__main__":
    input_file_path = '/home/pgroon/Downloads/todo.md'   # Change this to the path of your input text file
    output_file_path = '/home/pgroon/.conkyrc'    # Change this to the desired output .conkyrc file name

    generate_conkyrc(input_file_path, output_file_path)
