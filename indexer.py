import os
import json
import zipfile
import time
from bs4 import BeautifulSoup

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
    # Create count and map
    count = 0;
    docID_map = dict();

    # Iterate through zip file folders by turning it into a directory and walking through it
    with zipfile.ZipFile("analyst.zip", "r") as zipped:
        files = zipped.namelist()
        for name in files:
            extension = os.path.splitext(name)[-1]
            if extension == ".json":
                                
                with open(name, "r") as json_file:
                    json_data = json_file.read()

                doc = json.loads(json_data)
            
                
                the_soup = BeautifulSoup(doc["content"], "html.parser")
                # print(the_soup)                             # PRINT CHECK creates bs object
                 
                text = the_soup.find_all("p", "pre", "li", "title", "h1") 
                text.extend(the_soup.find_all("h2", "h3", "h4", "h5", "h6"))
                
                if len(text) == 0:
                    print("NON HTML FOUND")
                    print("\n")
                    continue
                

                docID_map[name] = count                             # doc name is key, ID is value    
                # print(docID_map[name], name)              # PRINT CHECK print docID dict
                count += 1;


                print(text)
                print("\n")



                # print(str(doc["content"]))                # PRINT CHECK prints html file
                # print("\n")

                time.sleep(1)

            


if __name__ == "__main__":
    indexer()
