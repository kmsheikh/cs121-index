# QUERY PROCESSING
    # Signal hander installed to quit with crtl+c


from tokenizer import *
import time
import glob
from ntpath import basename
import sys
import asyncio
import signal
from functools import partial


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
    
    
    # INTRO TEXT
    # explain what to search
    # how to quit (after every timestamp?)


    # GET KEYBOARD INPUT
    while(1):
        query = input("Enter your query:\n\t")
        start = time.time()                                         # TIME SEARCH RESULTS        
        doc_list = answer_query(query)

     

        

    if len(doc_answers) == 0:                                   # If no answers, return
        print("\tNo results found.\n")
            
        count = 0
    
        for answer in doc_answers:
            count += 1
            print("{}:\t {}\n".format(count, lookup_dict[answer]))
    
        end = time.time()
        elapsed_time = end - start
        print("\t{} results found in {} seconds.\n".format(count, elapsed_time))
     

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
    parsed_list = []                                                
    for found in found_list:    
        entry_list = found.split()                                  # Split entry by whitespace: [word  1/0.0  2/0.0] 
        entry_list.pop(0)                                           # Remove token from entry_list
        parsed_list.append(entry)                                   # Append [1/0.0 2/0.0] to parsed_list

    # CREATE LIST(token) OF LIST(posting) OF LIST(docID, score)
    doc_list = [] 
    for score_list in parsed_list:
        docs = []
        for score in score_list:
            split = stat.split("/")                                 # Split posting by "/" for docID, score
            docs.append(split)
        
        doc_list.append(docs)

    # SORT DOCS THAT ARE PRESENT FOR ALL TOKENS
    answer_list = []
    smallest_list = min(doc_list, key=len)                          # Find smallest list in doc_list to compare with others

    for small_post in smallest_list:
        the_flag = True                                             # Set flag to searh each element

        for postings in doc_list:
            for doc in postings:
                if small_post[0] not in doc:                        # If elem[0] docID not found in other postings, flag is false
                    the_flag = False

        if the_flag:
            doc_answers.append(int(docID))                                   # If true, docID is an answer for query




async def sigint_handler(g_index_dict, signum, frame):
    print("\n\tExiting...\n")
    
    # CLOSE ALL OPEN INDEXES
    for key in g_index_dict.keys():
        g_index_dict[key].close()

    sys.exit(0)



if __name__ == "__main__":
    # OPEN INDEX FILES, save opened files in dict for closing later
    g_index_dict = {}
    index_files = glob.glob("patial-index/*") 
    for file in index_files:
        txt = basename(file)                                                # Retrieve tail of path "a.txt" with basename
        g_index_dict[txt[0]] = open(file, "r", encoding="utf=8")

    signal.signal(signal.SIGINT, partial(sigint_handler, g_index_dict)      # Install signal handler for crtl+C
    
    search_engine()
