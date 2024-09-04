# What are the files in my directory?

## Sources
 1. https://docs.restech.unsw.edu.au/software/environment_modules/
2. https://github.com/unsw-restech/unsw-restech.github.io
3. https://docs.restech.unsw.edu.au/using_katana/running_jobs/
4. https://docs.restech.unsw.edu.au/using_katana/tips_katana/
5. https://docs.restech.unsw.edu.au/help_support/glossary/

 ## Answer

### Explain:
To check the files in your current directory on a PBS cluster, you can use the `ls` command. This command lists all the files and directories present in the current working directory where your session is active. It's essential to use this command after you've logged into the cluster to ensure you are viewing the correct path where your files are stored. 

The `ls` command is simple and effective for quickly examining the contents of your directory without requiring any additional parameters. If you want more details, you could use `ls -l` for a long listing format that includes file permissions, ownership, size, and modification dates. 

The PBS system allows you to interact with the file system, and utilizing basic Linux commands is a fundamental skill when working in this environment. 

### Command:
```bash
ls
```

### Terminal Output: 
```bash
README.md
__pycache__
bash_utils.py
context.py
conversation.md
find_yay.pbs
llm.py
playground copy.md
playground.md
prompts.yaml
prototype copy.py
prototype.py
questions.txt
requirements.txt
utils.py
venv
web_data
```

The terminal output from the `ls` command shows a list of files and directories present in your current working directory. Here's a breakdown of the items listed:

### Files and Directories:

- **README.md**: 
  - A markdown file typically containing information about the project, its purpose, and instructions on how to use or contribute to it.

- **__pycache__**: 
  - A directory created by Python that contains compiled bytecode files for modules imported in your Python scripts. This helps speed up program execution.

- **bash_utils.py**: 
  - A Python script likely containing utility functions or classes that assist with bash command operations or related tasks.

- **context.py**: 
  - This may be a Python script that defines a context for other operations or functions, potentially related to the handling of conversation or data states.

- **conversation.md**: 
  - A markdown file, possibly used to document conversations or interactions, maybe for a chat application or similar project.

- **find_yay.pbs**: 
  - A script, likely for submitting a job using the Portable Batch System (PBS), which is commonly used for managing jobs on computing clusters.

- **llm.py**: 
  - A Python script that might be related to a "language model" or "large language model", which could be part of a machine learning or natural language processing application.

- **playground copy.md** and **playground.md**: 
  - These markdown files may contain notes or experiments related to a "playground" project where testing and development occur.

- **prompts.yaml**: 
  - A YAML file likely used to define prompts or configurations for a program, potentially related to natural language processing or user interaction.

- **prototype copy.py** and **prototype.py**: 
  - These Python scripts may represent different iterations of a prototype application, with the copy indicating a modified or experimental version.

- **questions.txt**: 
  - A text file that might contain a list of questions, possibly for data collection, quizzes, or task prompts.

- **requirements.txt**: 
  - A standard file in Python projects that lists the packages and their versions required to run the project. It's essential for setting up the environment.

- **utils.py**: 
  - A Python script that likely includes various utility functions that can be reused across different parts of your project.

- **venv**: 
  - A directory representing a Python virtual environment, which is used to isolate project dependencies from the system-wide Python installation.

- **web_data**: 
  - This could be a directory that contains data scraped from the web or datasets used for your project.

### Summary:
Your current directory houses a variety of files and directories, including Python scripts, markdown files, a virtual environment, and a batch job script. This setup suggests you might be working on a Python project that involves data processing, potentially in the realms of machine learning or natural language processing, along with documentation and utility scripts to assist with development.

