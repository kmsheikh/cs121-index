# QUERY PROCESSING

# Using vocab.txt for byte positions, 
# seek the lines in index to solve query


def search_engine():
    
    # HARDCODE TEST
    # Search for "professor"

    vocab_dict = dict()

    with open("vocab.txt", "r", encoding="utf-8") as vocab_file:        # Write vocab index to memory
        for line in vocab_file:
            (word, byte) = line.split()
            vocab_dict[word] = int(byte)
    
    
    with open("index.txt", "r", encoding="utf-8") as index_file:        # Find line in index
        key = "professor"
        
        if key in vocab_dict:
            index_file.seek(vocab_dict[key])
            print(index_file.readline())
        else:
            print("Professor was not found")



if __name__ == "__main__":
    search_engine()
