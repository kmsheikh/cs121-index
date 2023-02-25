# QUERY PROCESSING

# Using vocab.txt for byte positions, 
# seek the lines in index to solve query
def create_vocab_dict():
    vocab_dict = dict()

    with open("vocab.txt", "r", encoding="utf-8") as vocab_file:        # Write vocab index to memory
        for line in vocab_file:
            (word, byte) = line.split()
            vocab_dict[word] = int(byte)

def get_postings(keys, vocab_dict):
    postings = []
    with open("index.txt", "r", encoding="utf-8") as index_file:        # Find line in index
        for key in keys:
            if key in vocab_dict:
                index_file.seek(vocab_dict[key])
                postings.append(index_file.readline().split()[1:])
            else:
                print(f"{key} was not found")
        
def get_matches(postings):
    min_index = postings.index(min(postings))
    #max_index = postig
    return_postings = []
    
    for posting in postings[min_index]:
        doc_postings = []
        matches_found = 0
        split_posting = [int(x) for x in posting.split(".")]
        doc_postings.append(split_posting)

        for others in range(len(postings)):
            if others != min_index:
                for other_posting in postings[others]:
                    other_split_posting = [int(x) for x in other_posting.split(".")]
                    if other_split_posting[0] == split_posting[0]:
                        doc_postings.append(other_split_posting)
                        matches_found += 1

        if matches_found == len(postings) - 1:
            combined_posting = [split_posting[0], 0, 0]
            for doc_posting in doc_postings:
                combined_posting[1] += doc_posting[1]
                combined_posting[2] += doc_posting[2]

            return_postings.append(combined_posting)

    

    return sorted(return_postings, key = lambda x: -(x[1] + x[2] * 2))

        # i = 0
        # while True:    
        #     for others in range(len(postings)):
        #         if others != min_index:
        #             if i < postings[others][-1]:
        #                 other_split_posting = postings[others][i].split(".")
        #                 if other_split_posting[0] == split_posting[0]:
        #                     matches_found += 1
        #                     doc_postings.append(other_split_posting)

        #     if matches_found == len(postings) - 1 or matches_found == -1: 
        #         break

        #     i += 1

        


def search_engine(keys):
    
    # HARDCODE TEST
    # Search for "professor"

    vocab_dict = create_vocab_dict()
    postings = get_postings(keys, vocab_dict)
    get_matches(postings)
    



if __name__ == "__main__":
    query = input("Please enter your search query:\n")
    query_list = tokenize_words(query)
    search_engine(query_list)
