import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import spacy
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES

nlp = spacy.load('en_core_web_lg')
file_path = "/Users/mohit/Desktop/a.txt"
file = open(file_path, 'r')
text = file.read()
text1=text.split(".")
text2 = list("")
for t in text1:
    t = t.replace("\n"," ")
    text2.append(t)
all_word_set = set("")

for data in text2:
    doc = nlp(data)
    for tok in doc:
        if tok.pos_ == "VERB":
            if tok not in all_word_set:
                all_word_set.add(tok)

kidnap_template = nlp("kill")
kidnap_set = set("")
for word in all_word_set:
    score = kidnap_template.similarity(word)
    if score > 0.5:
        if word not in kidnap_set:
            kidnap_set.add(word.text)
print(kidnap_set)