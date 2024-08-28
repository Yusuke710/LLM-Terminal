# LLM-Terminal: Bridging the Gap Between Users and HPC Systems with LLM

**Work in Progress**

key points
- LLM agents and RAG 
- LLM outputs terminal commands for users to run
- LLM takes terminal output as context in RAG

A Summary of the Code Workflow:
- Determine if the question can be answered by LLM or requires running a terminal command.
- If terminal commands are involved, detect them with the string ```bash```.
- For LLM responses:
  - Use Retrieval-Augmented Generation (RAG) with the initial response and add citations.
- For terminal commands:
  - Use RAG with the initial response, add citations, and explain commands with citations if necessary.
  - Write a one-line command and detect it with the string ```bash```.
  - Check if the command is valid and secure by running a simple test command.
  - Ensure harmful commands are flagged
  - Prompt the user to execute, modify, or abort the command.
- Manually run the command on the terminal (for now).
- Display or append the output in ```bash```.
- Use the terminal output to run the LLM again with the initial question and response.
