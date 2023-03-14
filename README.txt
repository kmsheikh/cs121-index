indexer.py


In order to run indexer.py, you must have a stopwords.txt file in the same directory. The stopwords.txt file contains all the stopwords, and is used for document processing. To get web pages from a specific zip file other than developer.zip, the zip file name that is opened at line 61 needs to be changed to the appropriate zip file name. If working with a different zip file 


After running indexer.py, a folder with multiple partial indexes will be created. Additionally, a text file named docID.txt will be created, which is used for storing the urls of documents, and a text file named vocab.txt will be created, which is used for indexing the index.


search.py


In order to run search.py, you must have all the documents generated from indexer.py. After running search.py you will be prompted for a query. After entering your query, you will see the top 5 urls that match with your query. In order to stop the program, press ctrl+C.