import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pickle
from sentence_transformers import CrossEncoder

def save_web_data(url, output_dir='web_data'):
    # Fetch the webpage content
    response = requests.get(url)
    response.raise_for_status()  # Check that the request was successful

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all anchor tags
    anchors = soup.find_all('a')

    # Dictionary to store links and their corresponding texts
    data = {}

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Extract and fetch content for each unique link
    visited_urls = set()
    for anchor in anchors:
        href = anchor.get('href')
        if href and not href.startswith('#'):  # Ignore empty and in-page links
            full_url = urljoin(url, href)
            if full_url != 'https://docs.restech.unsw.edu.au/help_support/faq/' and full_url not in visited_urls:
                visited_urls.add(full_url)
                try:
                    link_response = requests.get(full_url)
                    link_response.raise_for_status()  # Check that the request was successful
                    # Parse the linked webpage content
                    link_soup = BeautifulSoup(link_response.content, 'html.parser')
                    
                    # Extract <p>, <code>, and heading tags <h1> to <h6>
                    paragraphs = link_soup.find_all('p')
                    code_blocks = link_soup.find_all('code')
                    headings = {f'h{i}': link_soup.find_all(f'h{i}') for i in range(1, 7)}

                    # Concatenate the extracted text into a single string
                    all_content = "\n".join([
                        "\n".join([f"{heading_tag.upper()}: {heading.get_text(strip=True)}" for heading_tag, heading_list in headings.items() for heading in heading_list]),
                        "\n".join([f"PARAGRAPH: {p.get_text(strip=True)}" for p in paragraphs]),
                        "\n".join([f"CODE: {code.get_text(strip=True)}" for code in code_blocks])
                    ])

                    # Store the concatenated content in the dictionary
                    data[full_url] = all_content
                    print(f'Saved content for {full_url}')
                except requests.RequestException as e:
                    print(f'Failed to fetch {full_url}: {e}')

    # Save the dictionary to a pickle file
    pickle_file_path = os.path.join(output_dir, 'web_data.pkl')
    with open(pickle_file_path, 'wb') as pickle_file:
        pickle.dump(data, pickle_file)

    print(f'All data saved to {pickle_file_path}')

def load_web_data(pickle_file_path):
    with open(pickle_file_path, 'rb') as pickle_file:
        data = pickle.load(pickle_file)
    return data


def rerank_context(query, search_dic, rerank_model, rerank_top_k=5):
    """Rerank search results based on relevance to the query using a CrossEncoder model."""
    query_context_pairs = [(query, content) for content in search_dic.values()]
    scores = rerank_model.predict(query_context_pairs)
    
    # Zip search results with their scores and sort them based on the scores
    top_results = sorted(zip(search_dic.keys(), search_dic.values(), scores), key=lambda x: x[2], reverse=True)[:rerank_top_k]
    
    # Correct the use of enumerate to iterate over the list of tuples
    context_list = [f"[{i+1}]({url}): {content}" for i, (url, content, score) in enumerate(top_results)]
    
    context_block = "\n".join(context_list)
    return context_block

# Example usage
if __name__ == "__main__":
    # URL of the document
    url = 'https://docs.restech.unsw.edu.au/'

    # Save the data
    #save_web_data(url)

    # Load the data
    data = load_web_data('web_data/web_data.pkl')

    # Example: print the content of a specific URL
    for key, value in data.items():
        print(key, len(value))
        break  # Only print the first one as an example

    # rerank model
    query = 'nvidia-smi'
    rerank_model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-12-v2' )
    reranked_search_dic = rerank_context(query, data, rerank_model, rerank_top_k=5)
    print(reranked_search_dic)
