import os
import subprocess
import re

def extract_bash(llm_output):
    """
    Extracts a bash script from the provided LLM output.
    """
    bash_start_marker = "```bash"
    bash_end_marker = "```"

    # Find the start and end indices of the bash string
    start_index = llm_output.find(bash_start_marker)
    if start_index == -1:
        return None  # bash markers not found

    start_index += len(bash_start_marker)  # Move past the marker
    end_index = llm_output.find(bash_end_marker, start_index)
    if end_index == -1:
        return None  # End marker not found

    # Extract the bash string
    bash_string = llm_output[start_index:end_index].strip()

    return bash_string

def save_and_verify_bash(bash_string):
    """
    Saves the bash string to a file and verifies its syntax.
    """
    file_name = "temp_bash_command.sh"
    with open(file_name, 'w') as file:
        file.write(bash_string)

    try:
        result = subprocess.run(['bash', '-n', file_name], capture_output=True, text=True)
        os.remove(file_name)
        return result.returncode == 0
    except Exception as e:
        print(f"An error occurred during verification: {e}")
        return False


def scan_bash_command(command):
    """
    Scans the provided bash command for potentially harmful patterns.
    """

    # Save and verify bash script
    if save_and_verify_bash(command):
        print("Bash script syntax is valid.")
    else:
        print("Invalid Bash script detected.")
        return 'abort'
    
    # check for harmful pattern
    harmful_patterns = {
        r"\brm\s+-rf\b": "This command forcefully deletes files and directories, which can lead to accidental data loss. Example: `rm -rf /home/user`",
        # Other patterns omitted for brevity
        r"\brm\b": "Any command containing `rm` should be flagged because it may delete files or directories. Example: `rm file.txt`"
    }

    flagged_warnings = [
        f"Warning: {description}" for pattern, description in harmful_patterns.items() if re.search(pattern, command)
    ]
    
    return flagged_warnings


def prompt_user(command):
    """
    Prompts the user to take action on the extracted command.
    """
    print(f"The following command has been extracted:\n{command}")
    while True:
        user_input = input("Do you want to [e]xecute, [m]odify, or [a]bort? ").strip().lower()
        if user_input == 'e':
            return 'execute'
        elif user_input == 'm':
            return input(f"Please modify {command}: ").strip()
        elif user_input == 'a':
            print("Operation aborted by the user.")
            return 'abort'
        else:
            print("Invalid input. Please enter 'e', 'm', or 'a'.")


def execute_bash(command):
    """
    Executes the provided bash command and returns the output.
    """
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        if error:
            print(f"Error occurred: {error.decode('utf-8').strip()}")
        return output.decode("utf-8").strip()
    except Exception as e:
        print(f"An error occurred while executing the command: {e}")
        return str(e)


if __name__ == "__main__":
    # Example usage
    response = """
    To check what files are there in your current directory resources, run the following command

    ```bash
    ls -la
    ```
    """

    bash_string = extract_bash(response)
    if bash_string:
        warnings = scan_bash_command(bash_string)
        if warnings:
            print("\n".join(warnings))
            exit()
        else:
            print('No harmful command detected.')

        action = prompt_user(bash_string)
        if action == 'execute':
            terminal_output = execute_bash(bash_string)
        else:
            terminal_output = execute_bash(action)

        print(terminal_output)
    else:
        print("No valid bash command found in the provided output.")
