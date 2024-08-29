import os
import yaml
import openai
from sentence_transformers import CrossEncoder

from context import load_web_data, rerank_context
from llm import get_response_from_llm
from bash_utils import extract_bash, scan_bash_command, prompt_user, execute_bash
# -----------------------------------------------------------------------------
# Default configuration
RERANK_TOP_K = 5  # Top k ranked search results going into context of LLM
RERANK_MODEL = 'cross-encoder/ms-marco-MiniLM-L-12-v2'  # Max tokens = 512 # https://www.sbert.net/docs/pretrained-models/ce-msmarco.html
LLM_MODEL = 'gpt-4o-mini-2024-07-18'  
# -----------------------------------------------------------------------------


# Load the saved web data
def main():

    # Load YAML configuration file
    with open('prompts.yaml', 'r') as file:
        config = yaml.safe_load(file)

    # Accessing values from the config
    system_prompt = config['system_prompt']
    initial_response_prompt = config['initial_response_prompt']
    general_QA_prompt = config['general_QA_prompt']
    answer_bash_command_prompt = config['answer_bash_command_prompt']
    answer_with_terminal_output_prompt = config['answer_with_terminal_output_prompt']

    pickle_file_path = 'web_data/web_data.pkl'
    local_context = load_web_data(pickle_file_path)

    # Set up OpenAI API key
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    if OPENAI_API_KEY is None:
        raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    rerank_model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-12-v2' )

    msg_history = []

    while True:
        # get user query 
        query = input("Enter your query: ")

        # initial response
        initial_response, _ = get_response_from_llm(
                    initial_response_prompt.format(initial_question=query),
                    client=client,
                    model=LLM_MODEL,
                    system_message=system_prompt,
                    msg_history=msg_history,
                    max_tokens=100
                )

        # get context using the initial response, use rerank model
        # Rerank the combined search results
        reranked_context = rerank_context(initial_response, local_context, rerank_model, rerank_top_k=RERANK_TOP_K)

        # if initial response contains ```bash```
        initial_bash_string = extract_bash(initial_response)
        if initial_bash_string:
            # llm with terminal output as context 
            intermediate_response, msg_history = get_response_from_llm(
                        answer_bash_command_prompt.format(
                            query=query,
                            context_block=reranked_context
                        ),
                        client=client,
                        model=LLM_MODEL,
                        system_message=system_prompt,
                        msg_history=msg_history,
                        max_tokens=1000
                    )

            intermediate_bash_string = extract_bash(intermediate_response)

            # check intermediate bash step
            bash_string = intermediate_bash_string or initial_bash_string
            warnings = scan_bash_command(bash_string)
            if warnings: 
                print(warnings)
                continue
            else:
                print('No harmful command detected.')

            action = prompt_user(bash_string)
            if action == 'execute':
                terminal_output = execute_bash(bash_string)
            elif action == 'abort':
                continue
            else:
                terminal_output = execute_bash(action)
            

            print(terminal_output)
            
            #TODO
            # if  terminal_output has error, retry generating with llm again


            if not terminal_output:
                continue

            # llm with terminal output as context 
            final_response, msg_history = get_response_from_llm(
                        answer_with_terminal_output_prompt.format(
                            query=query,
                            command=bash_string,
                            terminal_output=terminal_output
                        ),
                        client=client,
                        model=LLM_MODEL,
                        system_message=system_prompt,
                        msg_history=msg_history,
                        max_tokens=1000
                    )
        
         
        else:
            # llm for general Q&A 
            final_response, msg_history = get_response_from_llm(
                        general_QA_prompt.format(
                            query=query,
                            context_block=reranked_context
                        ),
                        client=client,
                        model=LLM_MODEL,
                        system_message=system_prompt,
                        msg_history=msg_history,
                        max_tokens=1000
                    )


if __name__ == "__main__":
    main()