# MathTheorem-PageRank
A ranking of math theorems and definitions using the PageRank algorithm

# Details
The ranking of theorems is in theorem_ranks.txt
The ranking of definitions is in definition_ranks.txt
The ranking of every proofwiki page containing a 'Proof' or 'Definition' or 'Theorem' section is in all_ranks.txt

The weighted graph fed into the pagerank algorithm is in weighted_graph.json

The full output (with numerical scores) from the PageRank algorithm is in ranks17.json (17 because there were ranks{i}.json for i=0 to i=16 from the 0th to 16*5=80th iterations of the PageRank alg).

Before running list_them.py, I ran rank.py until it reached the output:
i = 85: error = 1.8378147248534777e-06

# Source of Data
The data was sourced from proofwiki.org, from the download at the bottom of https://proofwiki.org/wiki/Help:Questions#Is_it_possible_to_download_your_definitions_as_a_data_file.3F

# Source of PageRank Algorithm
Copy-pasted from the PageRank wikipedia page.
