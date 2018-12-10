import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import spacy
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES

nlp = spacy.load('en_core_web_lg')


def task_three():
    tokens = list("")
    grammar_tags = dict()
    dependency_tags = dict()
    lemmas = list("")
    for tok in doc:
        tokens.append(tok.text)
        grammar_tags[tok] = tok.tag_
        if tok.dep_ in dependency_tags.keys():
            value_set = dependency_tags[tok.dep_]
            value_set.add(tok)
        else:
            value_set = set()
            value_set.add(tok)
            dependency_tags[tok.dep_] = value_set

    lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
    for i in range(0,len(tokens)):
        lemmas.append(lemmatizer(tokens[i],grammar_tags[i]))

    print("Tokenize")
    print(tokens)
    print("Lemmatize")
    print(lemmas)
    print("POS Tags")
    print(grammar_tags)
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

    return grammar_tags,tokens,dependency_tags,lemmas


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
dependency_tags = dict()
entity_tags = dict()
word_children_left = dict()
word_children_left_count = dict()
word_children_right = dict()
word_children_right_count = dict()

for token in doc:
    word_children_left[token.text] = token.lefts
    word_children_left_count[token.text] = token.n_lefts
    word_children_right[token.text] = token.rights
    word_children_right_count[token.text] = token.n_rights

for token in doc:
    if token.dep_ in dependency_tags.keys():
        dependency_tags[token.dep_].add(token.text)
    else:
        value_set = set()
        value_set.add(token.text)
        dependency_tags[token.dep_] = value_set

for entity in doc.ents:
    entity_tags[entity.label_] = entity

root_word = dependency_tags["ROOT"]
root_left_child = word_children_left[list(root_word)[0]]
root_right_child = word_children_right[list(root_word)[0]]










