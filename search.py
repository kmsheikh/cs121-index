# QUERY PROCESSING
    # Signal hander installed to quit with crtl+c
    # Using vocab.txt for byte positions, 
    # Seek() the lines in index to solve query

# TO DO:
    # Implment ranking, calculate tf-idf with document weights
    # Prompt user, search interface


from tokenizer import *
import glob
from ntpath import basename
import sys
import signal
import time
import glob
import ntpath
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
        stop_list = stop_file.read().split()
    
    lookup_dict = dict()
    with open("docID.txt", "r", encoding="utf-8") as lookup_file:       # lookup_dict stores docID website
        for line in lookup_file:
            (ID, doc) = line.split()
            lookup_dict[int(ID)] = doc
    
    # INTRO TEXT
    print("\tTo quit, enter ctrl+c.\n")


    # GET KEYBOARD INPUT
    while(1):
        query = input("Enter your query:\t")
        start = time.time()                                         # TIME SEARCH RESULTS

        postings_lists = gather_postings(query, vocab_dict, g_index_dict, stop_list)
        if not postings_lists:                                      # empty list, no postings found
            print("\n\tNo results found.")
            print("\tTo quit, enter ctrl+c.\n")
            continue
        
        score_dict = boolean_retrieval(postings_lists)   
        if not score_dict:
            print("\n\tNo results found.")
            print("\tTo quit, enter ctrl+c.\n")
            continue
    
        ranked_list = sorted(score_dict.items(), key=lambda x: (x[1]), reverse=True)
#print(ranked_list)

        if len(ranked_list) < 10:
            num = len(ranked_list)
        else:
            num = 10                                                # Sort and print top 10 or less results

        for x in range(num):
            doc = ranked_list[x][0]
            print("\n\t{}\t{}\n".format(x+1, lookup_dict[doc]))

        end = time.time()
        time_elapsed = end - start

        print("\n\tResults found in {} seconds.".format(time_elapsed))
        print("\tTo quit, enter ctrl+c.\n")



def boolean_retrieval(postings_lists: list)->dict:
    new_dict = {}
    minimum_dict = min(postings_lists, key=len)                     # Use the smallest posting to compare
    for key in minimum_dict.keys():
        the_flag = True
        add_score = 0

        for posting in postings_lists:                              # If key exists in each dict, keep adding score
            if key in posting.keys():
                add_score += posting[key]
            else: 
                the_flag = False                                    # Else, stop looping through postings
                break

        if the_flag:                                                # TRUE = all postings had the document
            new_dict[key] = add_score                               # Add the calculated score to the new dict (docID: score)
      

    return new_dict



def gather_postings(the_query: str, vocab_dict: dict, g_index_dict: dict, stop_list: list)->list:
    query_list = tokenize_words(the_query)
    query_set = set()
    for word in query_list:
        if word not in stop_list:
            query_set.add(word)                                     # Lose duplicates and stop words in query

    # GET WORD and POSTINGS FROM THE INDEX
    found_list = extract_postings(vocab_dict, query_list, g_index_dict)      
    if len(found_list) < len(query_set) or len(found_list) == 0:    # If not all search terms found, return empty list
        return []

    # PARSE POSTING ENTRY, remove tokens
    postings_lists = []                                                
    for found in found_list:    
        entry_list = found.split()                                  # Split entry by whitespace: [word  1/0.0  2/0.0] 
        entry_list.pop(0)                                           # Remove token from parsed entry_list
        
        entry_dict = {}
        for i in range(len(entry_list)):
            entry_list[i] = entry_list[i].split("/")
            entry_dict[int(entry_list[i][0])] = float(entry_list[i][1]) 

        postings_lists.append(entry_dict)                           # Append [1: 0.0, 2: 0.0] to postings_list

    return postings_lists



def extract_postings(vocab_dict: dict, query_set: set, g_index_dict: dict) -> list:
    postings = []
    for word in query_set:
        if word in vocab_dict:
            g_index_dict[word[0]].seek(vocab_dict[word])  
            postings.append(g_index_dict[word[0]].readline())   # Append line found in partial_index

    return postings



def sigint_handler(g_index_dict, signum, frame):
    print("\n\n\tExiting...\n")
    
    # CLOSE ALL OPEN INDEXES
    for key in g_index_dict.keys():
        g_index_dict[key].close()

    sys.exit(0)



if __name__ == "__main__":
    print("\n\tStarting up search engine...")

    # OPEN INDEX FILES, save opened files in dict for closing later
    g_index_dict = {}
    index_files = glob.glob("partial-index/*") 
    for file in index_files:
        txt = ntpath.basename(file)                                         # Retrieve tail of path "a.txt" with basename
        g_index_dict[txt[0]] = open(file, "r", encoding="utf=8")

    signal.signal(signal.SIGINT, partial(sigint_handler, g_index_dict))     # Install signal handler for crtl+C
    
    search_engine()
