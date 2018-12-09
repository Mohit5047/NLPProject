import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import spacy
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES

nlp = spacy.load('en_core_web_lg')



def task_three():
    tokens = list("")
    POS_tags = list("")
    dependency_tags = list("")
    lemmas = list("")
    for tok in doc:
        tokens.append(tok.text)
        POS_tags.append(tok.tag_)
        dependency_tags.append(tok.dep_)
        print(tok,tok.dep_)

    lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
    for i in range(0,len(tokens)):
        lemmas.append(lemmatizer(tokens[i],POS_tags[i]))

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

    return POS_tags,tokens,dependency_tags,lemmas


def get_verbs(corpus):
    all_word_set = set("")
    for data in corpus:
        doc = nlp(data)
        for tok in doc:
            if tok.tag_ == "VB" or tok.tag_== "VBD" or tok.tag_ == "VBG" or tok.tag_ == "VBN" or tok.tag_ == "VBP" or tok.tag_ == "VBZ":
                if tok not in all_word_set:
                    all_word_set.add(tok)
    return all_word_set


def get_similar(verb_template,all_word_set):
    verb_set = set("")
    for word in all_word_set:
        score = verb_template.similarity(word)
        if score > 0.4:
            if word not in verb_set:
                verb_set.add(word.text)
    print(verb_set)
    return verb_set

file_path = "/Users/mohit/Desktop/a.txt"
file = open(file_path, 'r',encoding="utf-8")
text = file.read()
text1 = text.split(".")
text2 = list("")
for t in text1:
    t = t.replace("\n"," ")
    text2.append(t)

all_verb_set = get_verbs(text2)
print("Enter test Sentence")
doc = nlp(input())

#Dependency Tree
for token in doc:
    print(token.text, token.dep_, token.head.text, token.head.pos_,
          [child for child in token.children])
doc2 = nlp("Jack killed the man in the bar on Thursday at 7 PM near the beach")

#NER tagging
for entity in doc2.ents:
    print(entity.text, entity.label_)

dependency_tags = dict()
entity_tags = dict()
for token in doc:
    dependency_tags[token.dep_] = token

for entity in doc.ents:
    entity_tags[entity.label_] = entity











