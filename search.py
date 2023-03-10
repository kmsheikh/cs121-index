# QUERY PROCESSING

# Using vocab.txt for byte positions, 
# seek the lines in index to solve query


# TO DO:
#       Implment ranking, calculate tf-idf with document weights
#       Offer continuous input for user?


from tokenizer import *
import glob
import sys
import signal
import time
import glob
import ntpath
import sys
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
            lookup_dict[int(ID) - 1] = doc

    # INTRO TEXT
    # explain what to search
    # how to quit (after every timestamp?)


    # GET KEYBOARD INPUT
    while(1):
        query = input("Enter your query:\n\t")
        start = time.time()                                         # TIME SEARCH RESULTS        
        postings_lists = gather_postings(query, vocab_dict, g_index_dict, stop_list)
        if not postings_lists:                                      # empty list, no postings found
            print("\n\tNo results found.\n")
            continue

        ranked_postings = get_matches(postings_lists)
        if not ranked_postings:
            print("\n\tNo results found.\n")
            continue

        if len(ranked_postings) < 10:
            num = len(ranked_postings)
        else:
            num = 10                                                # Sort and print top 10 or less results

        for x in range(num):
            doc = int(ranked_postings[x][0])
            print("\n\t{}\t{}\n".format(x+1, lookup_dict[doc]))

        end = time.time()
        time_elapsed = end - start

        print("\n\tResults found in {} seconds.\n".format(time_elapsed))

def gather_postings(the_query: str, vocab_dict: dict, index_dict: dict, stop_list: list)->list:
    query_list = tokenize_words(the_query)
    query_set = set()
    for word in query_list:
        if word not in stop_list:
            query_set.add(word)                                     # Lose duplicates and stop words in query

    # GET WORD and POSTINGS FROM THE INDEX
    found_list = extract_postings(vocab_dict, query_list, index_dict)      
    if len(found_list) < len(query_set) or len(found_list) == 0:    # If not all search terms found, return empty list
        return []

    # PARSE POSTING ENTRY, remove tokens
    postings_lists = []                                                
    for found in found_list:    
        entry_list = found.split()                                  # Split entry by whitespace: [word  1/0.0  2/0.0] 
        entry_list.pop(0)                                           # Remove token from parsed entry_list
        for i in range(len(entry_list)):
            entry_list[i] = entry_list[i].split("/")                # Split each posting to index proper elements
        postings_lists.append(entry_list)                                      # Append [1/0.0 2/0.0] to postings_list

    return postings_lists

def extract_postings(vocab_dict: dict, query_set: set, index_dict: dict) -> list:
    postings = []
    for word in query_set:
        if word in vocab_dict:
            index_dict[word[0]].seek(vocab_dict[word])  
            postings.append(index_dict[word[0]].readline())   # Append line found in partial_index

    return postings

def get_matches(posting_lists: list) -> list:
    """
    Recursively finds postings with common docIds in a list of lists of postings
    """
    if len(posting_lists) == 1:  # If the posting_lists only has one list of postings, the only matches would be itself
        print(posting_lists)
        return sorted(posting_lists[0], key = lambda x: -float(x[1])) # return a ranked version of the list of postings
    else:
        posting_lists = sorted(posting_lists, key = len) # sort posting list in increasing order of length to gather the first two smallest amount of postings
        min1 = posting_lists.pop(0)
        if (len(min1) == 0):        # if length of the first minimum posting list is 0, then that means two lists didnt have a common docID posting, so reject it (since we're using AND retrieval)
            return []

        min2 = posting_lists.pop(0)
        and_merged = and_merge(min1, min2)
        posting_lists.append(and_merged)
        return get_matches(posting_lists)
        

def and_merge(posting1: list, posting2: list) -> list:
    """
    "Merges" two postings together by returning postings with common docIDs
    """
    pointer1 = 0
    pointer2 = 0
    new_posting_list = []
    while pointer1 != len(posting1) and pointer2 != len(posting2):  # Simultaneously iterates through postings by having pointers for each list
        if int(posting1[pointer1][0]) > int(posting2[pointer2][0]):     # If posting in posting1 is greater than posting in  posting2, iterate through posting2.
            pointer2 += 1                                                    # Since postings are ordered by increasing docId nums, iterating through posting2 may eventually reach docId
                                                                                    # from posting in posting1 or a higher docId num
        
        elif int(posting1[pointer1][0]) < int(posting2[pointer2][0]):   # Prior logic applies vice versa if posting in posting2 greater than posting in posting1
            pointer1 += 1

        else:
            docID = int(posting1[pointer1][0])      # If equal, add tf-idf scores together, add new posting to posting list, and iterate both lists
            score = float(posting1[pointer1][1]) + float(posting2[pointer2][1])
            new_posting_list.append([docID, score])
            pointer1 += 1
            pointer2 += 1
    
    return new_posting_list

def sigint_handler(g_index_dict, signum, frame):
    print("\n\tExiting...\n")
    
    # CLOSE ALL OPEN INDEXES
    for key in g_index_dict.keys():
        g_index_dict[key].close()

    sys.exit(0)



if __name__ == "__main__":
    g_index_dict = {}
    index_files = glob.glob("partial-index/*") 
    for file in index_files:
        txt = ntpath.basename(file)                                         # Retrieve tail of path "a.txt" with basename
        g_index_dict[txt[0]] = open(file, "r", encoding="utf=8")

    signal.signal(signal.SIGINT, partial(sigint_handler, g_index_dict))     # Install signal handler for crtl+C
    
    search_engine()