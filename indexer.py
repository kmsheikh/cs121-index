import os
import json
import zipfile
from bs4 import BeautifulSoup
import time
import nltk

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
    with zipfile.ZipFile("analyst.zip", "r") as zipped:
        files = zipped.namelist()
        for name in files:
            extension = os.path.splitext(name)[-1]
            if extension == ".json":
                with zipped.open(name) as json_file:
                    json_content = json_file.read()
                    json_dict = json.loads(json_content)
                    page_soup = BeautifulSoup(json_dict['content'], "html.parser")
                    text = page_soup.find_all(["p", "pre", "li", "title", "h1"])
                    if len(text) > 0:
                        current_text = ""
                        for chunk in text:
                            current_text += chunk.get_text()
                    
                    
                    
                time.sleep(1)

 def tokenize_words(text):
     # Uses nltk to tokenize words and returns list of tuples of the words found in the doc and their frequencies in the doc
                


if __name__ == "__main__":
    indexer()
