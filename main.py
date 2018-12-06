import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import spacy
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES

nlp = spacy.load('en_core_web_lg')
print("Enter test String")
text = input()
doc = nlp(text)

tokens = list("")
POS_tags = list("")
dependency_tags = list("")
lemmas = list("")
for tok in doc:
    tokens.append(tok.text)
    POS_tags.append(tok.pos_)
    dependency_tags.append(tok.dep_)

lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
for i in range(0,len(tokens)):
    lemmas.append(lemmatizer(tokens[i],POS_tags[i] ))



print("Tokenize")
print(tokens)
print("Lemmatize")
print(lemmas)
print("POS Tags")
print(POS_tags)
print("Dependency Parse Tree")
print(dependency_tags)

for tok in tokens:
    syn = wn.synsets(tok)
    hypernym = list("")
    hyponym = list("")
    holonym = list("")
    meronym = list("")
    for synset in syn:
        hypernym.append(synset.hypernyms())
        hyponym.append(synset.hyponyms())
        holonym.append(synset.part_holonyms())
        meronym.append(synset.part_meronyms())
    print(tok)
    print("Hypernyms")
    print(hypernym)
    print("Hyponyms")
    print(hyponym)
    print("Holonyms")
    print(holonym)
    print("Meronyms")
    print(meronym)




#Extras
# Find named entities, phrases and concepts
# for entity in doc.ents:
#     print(entity.text, entity.label_)

# Determine semantic similarities
doc1 = nlp("kill")
doc2 = nlp("murdered")
similarity = doc1.similarity(doc2)
print(doc1.text, doc2.text, similarity)