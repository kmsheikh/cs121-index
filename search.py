# QUERY PROCESSING

# Using vocab.txt for byte positions, 
# seek the lines in index to solve query


# TO DO:
#       Implment ranking, calculate tf-idf with document weights
#       Offer continuous input for user?


from tokenizer import *
import glob
from ntpath import basename
import sys
import asyncio
import signal
import time

def search_engine():
 
    # LOADING AUXILARY FILES INTO MEMORY
    vocab_dict = dict()
    with open("vocab.txt", "r", encoding="utf-8") as vocab_file:        # vocab_dict stores token byte_position
        for line in vocab_file:
            (word, byte) = line.split()
            vocab_dict[word] = int(byte)
    
    with open("stopwords.txt", "r") as stop_file:                       # Stop words for filtering queries
        stop_list = stop_file.read()
    
    lookup_dict = dict()
    with open("docID.txt", "r", encoding="utf-8") as lookup_file:       # lookup_dict stores docID website
        for line in lookup_file:
            (ID, doc) = line.split()
            lookup_dict[int(ID)] = doc

    
    # OPEN INDEX FILES, save opened files in dict for closing later
    index_dict = {}
    index_files = glob.glob("patial-index/*") 
    for file in index_files:
        txt = basename(file)                                            # Retrieve tail of path "a.txt" with basename
        index_dict[txt[0]] = open(file, "r", encoding="utf=8")

    
    # INTRO TEXT
    # explain what to search
    # how to quit (after every timestamp?)


    # GET KEYBOARD INPUT
    while(1):
        query = input("Enter your query:\n\t")
        start = time.time()                                         # TIME SEARCH RESULTS        
        doc_list = answer_query(query)

    
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
            
        count = 0
    
        for answer in doc_answers:
            count += 1
            print("{}:\t {}\n".format(count, lookup_dict[answer]))
    
        end = time.time()
        elapsed_time = end - start
        print("\t{} results found in {} seconds.\n".format(count, elapsed_time))
    

    # CLOSE ALL OPEN INDEXES
    for key in index_dict.keys():
        index_dict[key].close()


def answer_query(the_query: str)->list:
    query_list = tokenize_words(the_query)
    query_set = set()
    for word in query_list:
        if word not in stop_list:
            query_set.add(word)                                     # Lose duplicates and stop words in query

    # GET WORD and POSTINGS FROM THE INDEX
    found_list = [] 
    for word in query_set:
        if word in vocab_dict:
            index_dict[word[0]].seek(vocab_dict[word])  
            found_list.append(index_dict[word[0]].readline())       # Append line found in partial_index

    if len(found_list) < len(query_set) or len(found_list) == 0:    # If not all search terms found, return empty list
        return []

    # PARSE POSTING ENTRY, remove tokens
    doc_list = []                                                
    for found in found_list:    
        entry_list = found.split()                                  # Split entry by whitespace: [word  1/0.0  2/0.0] 
        entry_list.pop(0)                                           # Remove token from parsed entry_list
        doc_list.append(entry)                                      # Append [1/0.0 2/0.0] to doc_list






async def sigint_handler(signum, frame):
    print("\n\tExiting...\n")
    sys.exit(0)



if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler)                # Instal signal handler for crtl+C

    search_engine()
