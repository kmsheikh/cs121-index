# QUERY PROCESSING

# Using vocab.txt for byte positions, 
# seek the lines in index to solve query

from tokenizer import *


def search_engine():
 
    vocab_dict = dict()

    with open("vocab.txt", "r", encoding="utf-8") as vocab_file:        # Write vocab index to memory
        for line in vocab_file:
            (word, byte) = line.split()
            vocab_dict[word] = int(byte)
    
    query = input("Search: ")
    query_list = tokenize_words(query)
    query_set = set(query_list)                                         # Lose duplicates in query
    
    found_list = []
    
    with open("index.txt", "r", encoding="utf-8") as index_file:        # Find line in index
        for word in query_set:
            if word in vocab_dict:
                index_file.seek(vocab_dict[word])
                found_list.append(index_file.readline())                # Append line found in index
            else:
                found_list.append("")                                   # Add blank entry for word not found, so we can skip?

    for found in found_list:    # PRINT CHECK index entries
        print(found)
    

if __name__ == "__main__":
    search_engine()
