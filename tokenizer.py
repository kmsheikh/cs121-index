from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

def tokenize_words(text: str) -> list:
    # Uses nltk to tokenize words and returns list of tuples of the words found in the doc and their frequencies in the doc
    port = PorterStemmer()
    alnum_list = []
    word_list = word_tokenize(text)

    for word in word_list:
        word = port.stem(word)

        if word.isalnum():
            alnum_list.append(word)

    return alnum_list


def computeWordFrequencies(tokenList : list[str]) -> dict[str, int]:
    # take list of tokens and count # of frequencies as map
    # should run in linear time to text file size
    
    freqMap = dict()

    for t in tokenList:             # iterate thru list and count
        if t in freqMap.keys():     # count +1 if already in map
            freqMap[t] += 1
        else:
            freqMap[t] = 1          # start count if not in map
    return freqMap


def printFreq(freqMap : dict[str,int]):
    # display tokens high to low, any ties are displayed in alphanumeric order
    # should run in linear time to text file size

    for f in sorted(list(set(freqMap.values())), reverse=True):     # use set to isolate frequencies then sort as list high to low

        for w in sorted([i for i in freqMap if freqMap[i] == f]):   # iterate through sorted list of tokens with frequency f
            print(f, "=>", w)                                       # print token => frequency
