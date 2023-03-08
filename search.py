# QUERY PROCESSING

# Using vocab.txt for byte positions, 
# seek the lines in index to solve query


# TO DO:
#       Implment ranking, calculate tf-idf with document weights
#       Offer continuous input for user?
#       In indexer.py, create partial lists


from tokenizer import *
import time

def search_engine():
 
    vocab_dict = dict()

    with open("vocab.txt", "r", encoding="utf-8") as vocab_file:        # Write vocab index to memory
        for line in vocab_file:
            (word, byte) = line.split()
            vocab_dict[word] = int(byte)
    
    query = input("Search: ")
    print("")

    start = time.time()                                         # TIME SEARCH RESULTS
    query_list = tokenize_words(query)

    query_set = set()

    with open("stopwords.txt", "r") as stop_file:
        stop_list = stop_file.read()

        for word in query_list:
            if word not in stop_list:
                query_set.add(word)                                     # Lose duplicates and stop words in query
    

    found_list = []                                             # LIST OF STRINGS
    
    with open("index.txt", "r", encoding="utf-8") as index_file:        # Find line in index
        for word in query_set:
            if word in vocab_dict:
                index_file.seek(vocab_dict[word])
                found_list.append(index_file.readline())                # Append line found in index
    
    if len(found_list) < len(query_set) or len(found_list) == 0:        # If not all search terms found, return
        print("\tNo results found.\n")
        return


    parsed_list = []                                            # LIST OF LIST OF POSTINGS

    for found in found_list:    
        entry = found.split()                                           # Split entry by whitespace: [word  1.0.0  2.0.0] 
        entry.pop(0)                                                    # Remove token from parsed entry
        parsed_list.append(entry)                                       # Append [1.0.0  2.0.0] to list


    doc_list = []                                               # LIST OF LIST OF DOCIDS
    
    for stats_list in parsed_list:
        docs = []
        
        for stat in stats_list:
            docID = stat.split(".")[0]                                  # Split posting by ".", only return elem[0] DOCID
            docs.append(docID)

        doc_list.append(docs)


    doc_answers = []                                            # LIST OF DOCS FOR QUERY

    smallest_list = min(doc_list, key=len)                              # Find smallest list in doc_list to compare with others

    for docID in smallest_list:
        the_flag = True                                                 # Set flag to searh each element

        for docs in doc_list:
            if docID not in docs:
                the_flag = False                                        # If not found in ANY other list, set flag to false

        if the_flag:
            doc_answers.append(int(docID))                                   # If true, docID is an answer for query
    

    if len(doc_answers) == 0:                                   # If no answers, return
        print("\tNo results found.\n")
    else:
        lookup_dict = dict()

        with open("docID.txt", "r", encoding="utf-8") as lookup_file:       # Write lookup index to memory
            for line in lookup_file:
                (ID, doc) = line.split()
                lookup_dict[int(ID)] = doc
    
        count = 0
    
        for answer in doc_answers:
            count += 1
            print("{}:\t {}\n".format(count, lookup_dict[answer]))
    
        end = time.time()
        elapsed_time = end - start
        print("\t{} results found in {} seconds.\n".format(count, elapsed_time))
    


if __name__ == "__main__":
    search_engine()
