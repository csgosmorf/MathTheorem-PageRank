import json

def read_json_to_dict(file_path):
    """
    Reads a JSON file and returns its content as a dictionary.

    :param file_path: str, the path to the JSON file
    :return: dict, the content of the JSON file as a dictionary
    """
    try:
        with open(file_path, 'r', encoding='utf8') as json_file:
            data = json.load(json_file)
        return data
    except Exception as e:
        print(f"An error occurred while reading the JSON file: {e}")
        return None

# Before running this program, I ran rank.py until it reached output:
# i = 85: error = 1.8378147248534777e-06
# Dictionary successfully saved to ranks17.json

ranks_dict = read_json_to_dict('ranks17.json')
ranks = ranks_dict['ranks']

nondef_ranks = [(name, value) for name, value in ranks if 'Definition' not in name and 'Axiom' not in name]

theorem_ranks = [(name, value) for name, value in nondef_ranks if 'Theorem' in name]

defn_ranks = [(name[name.index('Definition:') + len('Definition:'):], value) for name, value in ranks if 'Definition:' in name]

def writeRanks(filePath, rankList):
    with open(filePath, mode='w', encoding='utf8') as outfile:
        for i, (name, value) in enumerate(rankList, start=1):
            outfile.write(f"{i}. {name}\n")

props_dict = read_json_to_dict('propositions.json')
props = set(props_dict['Theorems'])

prop_ranks = [(name, value) for name, value in ranks if name in props]

writeRanks('all_ranks.txt', ranks)
writeRanks('nondef_ranks.txt', nondef_ranks)
writeRanks('theorem_ranks.txt', theorem_ranks)
writeRanks('definition_ranks.txt', defn_ranks)
writeRanks('proposition_ranks.txt', prop_ranks)