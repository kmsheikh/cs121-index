import os
import json
import zipfile
from bs4 import BeautifulSoup
import time
import nltk
from tokenizer import computeWordFrequencies
from collections import defaultdict
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


def indexer():
    # Iterate through the json files found in the zip file
    index = defaultdict(dict)
    
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
                    check_html = page_soup.find_all("html")
                    
                    if check_html:
                        docID += 1
                        text = page_soup.find_all(["p", "pre", "li", "title", "h1"])
                        # TASK: include seprate find_all for title, bold, strong. h1. etc
                        #       to add more weights on the document score

                        for chunk in text:
                            word_list = tokenize_words(chunk.get_text())
                            word_freq = computeWordFrequencies(word_list)       

                            for key in word_freq:
                                if key in index and docID in index[key]:
                                    index[key][docID] += word_freq[key]         # if key and docID exist, add value to dict
                                else:
                                    index[key][docID] = word_freq[key]          # else initialize dict key



    
    index_list = sorted(index.items(), key=lambda x: (x[0]))                
    
    with open("WordIndex.txt", "w") as index_file:
        for elem in index_list:
            index_file.write("{} ->".format(elem[0])),
        
            for doc, count in elem[1].items():
                index_file.write(" {}: ({}) ".format(doc, count)),
            
            index_file.write("\n")


def tokenize_words(text):
    # Uses nltk to tokenize words and returns list of tuples of the words found in the doc and their frequencies in the doc
    stemmer = nltk.stem.PorterStemmer()
    words = nltk.tokenize.word_tokenize(text)
    words = [stemmer.stem(word) for word in words]
    alphanumeric_words = []
    
    for word in words:
        if word.isalnum():
            alphanumeric_words.append(word)

    #return computeWordFrequencies(alphanumeric_words)
    return alphanumeric_words
    
    


if __name__ == "__main__":
    indexer()
