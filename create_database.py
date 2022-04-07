import nltk 
from nltk.corpus import floresta
import re 
#nltk.download("floresta")

with open("database.txt","w") as f:
    dataset = ""
    for word,tag in floresta.tagged_words()[:1000]:
        if tag.endswith("n")  and len(word) > 3 and not re.search(".[^a-zA-Z]+",word):
            dataset +=  word + " "
        f.writelines(dataset)
