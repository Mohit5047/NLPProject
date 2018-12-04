import nltk
from nltk.stem import WordNetLemmatizer
import spacy
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES

nlp = spacy.load('en_core_web_sm')
print("Enter test String")
text = input()
doc = nlp(text)

tokens = list("")
POS_tags = list("")
dependency_tags = list("")
for tok in doc:
        tokens.append(tok.text)
        POS_tags.append(tok.pos_)
        dependency_tags.append(tok.dep_)

print(tokens)
print(POS_tags)
print(dependency_tags)
lemmas = list("")

lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
for i in range(0,len(tokens)):
        lemmas.append(lemmatizer(tokens[i],POS_tags[i] ))
print(lemmas)

#Extras
# Find named entities, phrases and concepts
# for entity in doc.ents:
#     print(entity.text, entity.label_)

# Determine semantic similarities
# doc1 = nlp("my fries were super gross")
# doc2 = nlp("such disgusting fries")
# similarity = doc1.similarity(doc2)
# print(doc1.text, doc2.text, similarity)