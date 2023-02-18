import os
import json
import zipfile
import time

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
    # Iterate through zip file folders by turning it into a directory and walking through it
    with zipfile.ZipFile("analyst.zip", "r") as zipped:
        files = zipped.namelist()
        for name in files:
            extension = os.path.splitext(name)[-1]
            if extension == ".json":
                print(name)
                time.sleep(1)

            


if __name__ == "__main__":
    indexer()
