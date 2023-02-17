# 121ass3-index
Deliverables: Submit your code and a report (in PDF format) with a table containing some analytics about your index. The minimum analytics are:  

The number of indexed documents;
The number of unique words;
The total size (in KB) of your index on disk.
No late submissions will be accepted for this milestone.

### Evaluation criteria:

Did your report show up on time?
Are the reported numbers plausible?

# Additional Specifications for Algorithms and Data Structures Developer
Option available to all students. Required for CS and SE students.
Programming skills required: advanced.

### Main challenges

Design efficient data structures, devise efficient file access, balance memory us-
age and response time.

### Corpus

A large collection of ICS web pages (developer.zip).

### Indexer

Your index should be stored in one or more files in the file system (no databases!).

### Search interface

The response to search queries should be ≤300ms. Ideally it would be .100ms,
but you won’t be penalized if it’s higher (as long as it’s kept ≤300ms).

### Operational constraints

Typically, the cloud servers/VMs/containers that run search engines don’t have
a lot of memory. As such, you must design and implement your programs as
if you are dealing with very large amounts of data, so large that you cannot
hold the inverted index all in memory. Your indexer must off load the inverted
index hash map from main memory to a partial index on disk at least 3 times
during index construction; those partial indexes should be merged in the end.
Optionally, after or during merging, they can also be split into separate index
files with term ranges. Similarly, your search component must not load the
entire inverted index in main memory. Instead, it must read the postings from
the index(es) files on disk. The TAs will verify that this is happening.

# Milestone 1
Goal: Build an index

### Building the inverted index

Now that you have been provided the HTML files to index, you may build your
inverted index off of them. The inverted index is simply a map with the token
as a key and a list of its corresponding postings. A posting is the representation
of the token’s occurrence in a document. The posting typically (not limited to)
contains the following info (you are encouraged to think of other attributes that
you could add to the index):
  •The document name/id the token was found in.  
  •Its tf-idf score for that document (for MS1, add only the term frequency).

#### Some tips:
  •When designing your inverted index, you will think about the structure
  of your posting first.  
  •You would normally begin by implementing the code to calculate/fetch
  the elements which will constitute your posting.  
  •Modularize. Use scripts/classes that will perform a function or a set of
  closely related functions. This helps in keeping track of your progress,
  debugging, and also dividing work amongst teammates if you’re in a group.  
  •We recommend you use GitHub as a mechanism to work with your team
  members on this project, but you are not required to do so.  

### Deliverables
Submit your code and a report (in pdf) to with the following content:
  •a table with assorted numbers pertaining to your index. It should have,
  at least the number of documents, the number of [unique] tokens, and the
  total size (in KB) of your index on disk.  

#### Note for the developer option: 
At this time, you do not need to have the
optimized index, but you may save time if you do.

### Evaluation criteria
  •Did your report show up on time?  
  •Are the reported numbers plausible?  
