import json

def save_dict_to_json(data_dict, file_path):
    """
    Save a Python dictionary as a JSON file.

    Parameters:
    data_dict (dict): The dictionary to save as JSON.
    file_path (str): The file path where the JSON file will be saved.
    """
    try:
        with open(file_path, 'w') as json_file:
            json.dump(data_dict, json_file, indent=4)
        print(f"Dictionary successfully saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving the dictionary: {e}")

def file_to_string(path):
    with open(path, mode='r', encoding='utf8') as file:
        return file.read()

def get_blocks(file_str, open_tag, close_tag):
    """
    Extracts blocks of text sandwiched between open_tag and close_tag from file_str,
    and returns a list of tuples where each tuple contains the block between the tags 
    and the block of text after the closing tag up to the next opening tag.

    Parameters:
    file_str (str): The string to search within.
    open_tag (str): The opening tag.
    close_tag (str): The closing tag.

    Returns:
    list of (str, str): A list of tuples where the first element is the text between the tags
                        and the second element is the text following the closing tag up to the next opening tag.
    """
    
    # Initialize the list to store the blocks of text
    blocks = []
    
    # Initialize the search position
    start_pos = 0
    
    while True:
        # Find the next occurrence of the opening tag
        start_idx = file_str.find(open_tag, start_pos)
        if start_idx == -1:  # No more opening tags found
            break
        
        # Find the corresponding closing tag
        end_idx = file_str.find(close_tag, start_idx)
        if end_idx == -1:  # No corresponding closing tag found
            break
        
        # Extract the block of text between the tags
        block = file_str[start_idx + len(open_tag):end_idx].strip()  # Strip any leading/trailing whitespace
        
        # Find the text after the closing tag up to the next opening tag
        next_open_idx = file_str.find(open_tag, end_idx + len(close_tag))
        if next_open_idx == -1:
            following_text = file_str[end_idx + len(close_tag):].strip()
        else:
            following_text = file_str[end_idx + len(close_tag):next_open_idx].strip()
        
        # Append the tuple (block, following_text) to the list
        blocks.append((block, following_text))
        
        # Move the search position forward
        start_pos = next_open_idx
    
    return blocks

site_str = file_to_string('latest.xml')
pages = get_blocks(site_str, '<page>', '</page>')

theorem_pages = []
definition_pages = []

graph = dict()

for i,(page, remainder) in enumerate(pages):
    title = get_blocks(page, '<title>', '</title>')[0][0]
    sections = dict(get_blocks(page, '== ', ' =='))
    if 'Theorem' in sections or 'Definition' in sections or 'Proof' in sections:
        graph[title] = []
        if 'Theorem' in sections:
            theorem_pages.append(title)

for i,(page, remainder) in enumerate(pages):
    title = get_blocks(page, '<title>', '</title>')[0][0]
    sections = dict(get_blocks(page, '== ', ' =='))
    page_links = []
    for section_name in sections:
        if section_name in ('Theorem', 'Definition', 'Proof'):
            section = sections[section_name]
            links = [name for name, _ in get_blocks(section, '[[', ']]')]
            for i, link in enumerate(links):
                if '|' in link:
                    links[i] = link[0:link.index('|')]
            page_links.extend([name for name in links if name != title and name in graph])
        
    if 'Theorem' in sections or 'Definition' in sections or 'Proof' in sections:
        graph[title] = page_links

weighted_graph = dict()
for name in graph:
    weighted_graph[name] = dict()
    num_links = len(graph[name])
    for link_name in graph[name]:
        weighted_graph[name][link_name] = 0.0

    for link_name in graph[name]:
        weighted_graph[name][link_name] += 1.0 / num_links

save_dict_to_json(weighted_graph, 'weighted_graph.json')

thms_dict = dict()
thms_dict['Theorems'] = theorem_pages

save_dict_to_json(thms_dict, 'propositions.json')
