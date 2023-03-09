import os
import json
import zipfile
from bs4 import BeautifulSoup
import math
from tokenizer import tokenize_words
from tokenizer import computeWordFrequencies
from collections import defaultdict
import sys
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
ZIP_DOC_NUM = 2000  # Get the amount of documents that are assumed to be in the Zip File

def indexer():
    # Iterate through the json files found in the zip file
    index = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    lookup_file = open("docID.txt", "a", encoding="utf-8")
    
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
                    lookup_file.write("{} {}\n".format(docID, json_dict["url"]))              # Append to docID lookup table

                    text = page_soup.find_all(["title", "h1", "h2", "h3", "b", "strong"])     # Get "important" words from html (replaces text for memory conservation)
                    important_text_size = len(text) # Get size of prior find_all call
                    for chunk in text:
                        word_list = tokenize_words(chunk.get_text())
                        word_freq = computeWordFrequencies(word_list)  
                        for key in word_freq:
                            index[key][docID][1] += word_freq[key] 

                    unwanted_tags = ["title", "h1", "h2", "h3", "b", "strong"]
                    for tag in unwanted_tags:
                        [s.extract() for s in page_soup(tag)]

                    text = page_soup.find_all()           # Get non-important words from html
                    text_size = len(text)       # Get size of prior find_all call
                    for chunk in text:
                        word_list = tokenize_words(chunk.get_text())
                        word_freq = computeWordFrequencies(word_list)       
                        for key in word_freq:
                            index[key][docID][0] += word_freq[key] 
                    
                    if text_size + important_text_size > 0: # Check if indexer extracted some text from the tags we require. If not it is essentially ignored.
                        docID += 1

                    if docID > (ZIP_DOC_NUM / 5) * 4:  # Offload the dictionary index in each of these branches.
                        pass
                    elif docID > (ZIP_DOC_NUM / 5) * 3:
                        pass 
                    elif docID > (ZIP_DOC_NUM / 5) * 2:
                        pass
                    elif docID > ZIP_DOC_NUM / 5:
                        pass

    lookup_file.close()
    
    index_list = sorted(index.items(), key=lambda x: (x[0]))                
#    print(f"{psutil.virtual_memory()[2]} percent of RAM used at END")

    vocab_file = open("vocab.txt", "a", encoding="utf-8")                       # INDEX THE INDEX

    with open("index.txt", "w", encoding="utf-8") as index_file:
        for elem in index_list:

            vocab_file.write("{} {}\n".format(elem[0], index_file.tell()))      # INDEX THE INDEX write byte position before writing to original index

            index_file.write("{} ".format(elem[0])),
        
            for doc, count in elem[1].items():
                index_file.write("{}.{}.{} ".format(doc, count[0], count[1])),
            
            index_file.write("\n")
    
    vocab_file.close()

def update_indexes(files, doc_nums):
    for letter in sorted(files.keys()):
        partial_index = defaultdict(lambda: defaultdict())
        files[letter].seek(0)
        for line in files[letter]:
            split_line = line.split()
            for posting in split_line[1:]:
                split_posting = posting.split(".")
                tf = 1 + int(split_posting[1]) + (int(split_posting[2]) * 2)
                df = len(split_line[1:])
                tf_idf = (1 + math.log10(tf)) * math.log(doc_nums / df)
                partial_index[split_line[0]][int(split_posting[0])] = tf_idf
        
        files[letter].seek(0)
        files[letter].truncate(0)
        for key, value in sorted(partial_index.items(), key = lambda x: x[0]):
            files[letter].write(f"{key} ")
            for doc, score in sorted(value.items(), key = lambda x: x[0]):
                files[letter].write(f"{doc}/{score} ")
            files[letter].write("\n")


if __name__ == "__main__":
    #indexer()
    partial = open("partial_test.txt", "r+")

    update_indexes({"a": partial}, 20)