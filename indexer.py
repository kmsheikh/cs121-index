import os
import json
import zipfile
from bs4 import BeautifulSoup
import time
from tokenizer import *
from collections import defaultdict
import psutil
import sys
import string

# create an inverted index for the corpus
# tokens = alphanumeric sequences in the dataset
# stemming = better textual matches
# important text = bolded and heading text should be more important!!
# all words will be indexed, no stop words

# load inverted index hash map from main memory into partial index 3+ times during index construction
# partial indexes will be merged in the end

# inverted index maps token -> postings
# posting = representation of token's occurrence in document (doc id/name + tf-idf score)

# m1 -- use token frequency instead of tf-idf score

# partial index + merge
    # open all text files, organized alphabetically (a.txt b.txt... 9.txt)
    # for each token in LOOP, immediately write to corresponding file
    # after all documents searched, iterate through list of files:
        # load a.txt into memory
        # sort
        # write to index.txt (complete index)
        # close a.txt


ZIP_DOC_NUM = 2000                  # Number of documents in Zip File

def indexer():

    # create partial-index directory
    try:
        os.mkdir("partial-index")
    except FileExistsError as error:
        print(error)
        print("Delete partial-index and try again.")
        return

    # OPEN ALL FILES IN partial-index directory
    index_range = string.ascii_lowercase + string.digits + "!"
    partial_dict = {}                                           # Dictionary to track open index files

    for i in index_range:
        path = "partial-index/" + i + ".txt"
        partial_file = open(path, "x", encoding="utf-8") 
        partial_dict[i] = partial_file                          # Match file to letter/digit 

    # Iterate through the json files found in the zip file
    index = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    lookup_file = open("docID.txt", "a", encoding="utf-8")
    offload_dict = True

    with zipfile.ZipFile("analyst.zip", "r") as zipped:
        files = zipped.namelist()
        docID = 0

        for name in files:
            extension = os.path.splitext(name)[-1]  

            if extension == ".json":
                with zipped.open(name) as json_file:
                    json_content = json_file.read()
                    json_dict = json.loads(json_content)
                    
                    page_soup = BeautifulSoup(json_dict['content'], "html.parser")
                    
                    text = page_soup.find_all(["title", "h1", "h2", "h3", "b", "strong"])       # Get "important" words from html
                    important_text_size = len(text)     
                    for chunk in text:
                        word_list = tokenize_words(chunk.get_text())
                        word_freq = computeWordFrequencies(word_list)       
                        for key in word_freq:
                            index[key][docID][1] += word_freq[key] 


                    unwanted_tags = ["title", "h1", "h2", "h3", "b", "strong"]
                    for tag in unwanted_tags:
                        [s.extract() for s in page_soup(tag)]

                    text = page_soup.find_all()                                                 # Get "non-important" words from html
                    text_size = len(text)
                    for chunk in text:
                        word_list = tokenize_words(chunk.get_text())
                        word_freq = computeWordFrequencies(word_list)       
                        for key in word_freq:
                            index[key][docID][0] += word_freq[key]

                    if text_size + important_text_size > 0:                                     # Check if indexer extracted text from tags
                        docID += 1                                                              # If not, ignore
                        lookup_file.write("{} {}\n".format(docID, json_dict["url"]))            # Append to docID lookup table

                    
                    # Offload the dictionary index in each of these branches
                    if offload_dict == True:
                        if docID > (ZIP_DOC_NUM / 5) * 4:
                            index = offload(index, partial_dict)
                            offload_dict = False
                        elif docID > (ZIP_DOC_NUM / 5) * 3:
                            index = offload(index, partial_dict) 
                        elif docID > (ZIP_DOC_NUM / 5) * 2:
                            index = offload(index, partial_dict)
                        elif docID > ZIP_DOC_NUM / 5:
                            index = offload(index, partial_dict)

    
    lookup_file.close()
    offload(index, partial_dict)                    # Last offload

    #index_list = sorted(index.items(), key=lambda x: (x[0]))                    # Sort the index (ENTIRELY IN MEMORY)
    #vocab_file = open("vocab.txt", "a", encoding="utf-8")                       # INDEX THE INDEX
    
    #with open("index.txt", "w", encoding="utf-8") as index_file:
    #   for elem in index_list:
    #      vocab_file.write("{} {}\n".format(elem[0], index_file.tell()))      # INDEX THE INDEX write byte position before writing to original index
    #      index_file.write("{} ".format(elem[0])),
     
    #      for doc, count in elem[1].items():
    #         index_file.write("{}.{}.{} ".format(doc, count[0], count[1])),
        
    #       index_file.write("\n")
    
    #vocab_file.close()

    # Close all open partial indexes
    for key in partial_dict.keys():
        partial_dict[key].close()



# Separate function for offloading dict + writing to partial files
# arg1 = current index, arg2 = partial dict files

def offload(my_dict, p_dict)->defaultdict:
    index_list = sorted(my_dict.items(), key=lambda x: (x[0]))          # Sort the current in-memory index
                                            
    for elem in index_list:
        try:
            partial_file = p_dict[elem[0][0]]                           # Use first letter to retrieve file   
        except KeyError:
            partial_file = p_dict["!"]                                  # Non-english go in *.txt

        partial_file.write("{} ".format(elem[0])),
        
        for doc, count in elem[1].items():
            partial_file.write("{}.{}.{} ".format(doc, count[0], count[1])),
            
        partial_file.write("\n")

    return defaultdict(lambda: defaultdict(lambda: [0, 0]))
    


if __name__ == "__main__":
    indexer()
