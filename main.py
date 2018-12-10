import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import spacy
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
import invoke_verb

nlp = spacy.load('en_core_web_lg')


def task_three(doc1):
    tokens = list("")
    grammar_tags = dict()
    depend_tags = dict()
    lemmas = list("")
    for tok in doc1:
        tokens.append(tok.text)
        grammar_tags[tok] = tok.tag_
        if tok.dep_ in depend_tags.keys():
            value_set = depend_tags[tok.dep_]
            value_set.add(tok)
        else:
            value_set = set()
            value_set.add(tok)
            dependency_tags[tok.dep_] = value_set

    lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
    for i in range(0, len(tokens)):
        lemmas.append(lemmatizer(tokens[i], grammar_tags[i]))

    print("Tokenize")
    print(tokens)
    print("Lemmatize")
    print(lemmas)
    print("POS Tags")
    print(grammar_tags)
    print("Dependency Parse Tree")
    print(depend_tags)

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

    return grammar_tags, tokens, dependency_tags, lemmas


def get_verbs(corpus):
    all_word_set = set("")
    for data in corpus:
        doc = nlp(data)
        for tok in doc:
            if tok.tag_ == "VB" or tok.tag_ == "VBD" or tok.tag_ == "VBG" or tok.tag_ == "VBN" or tok.tag_ == "VBP" or tok.tag_ == "VBZ":
                if tok not in all_word_set:
                    all_word_set.add(tok)
    return all_word_set


def get_similar(verb_template, all_word_set):
    verb_set = set("")
    for word in all_word_set:
        score = verb_template.similarity(word)
        if score > 0.5:
            if word not in verb_set:
                verb_set.add(word.text)
    print(verb_set)
    return verb_set


file_path = "/Users/mohit/Desktop/a.txt"
file = open(file_path, 'r', encoding="utf-8")
text = file.read()
text1 = text.split(".")
text2 = list("")
for t in text1:
    t = t.lower()
    t = t.replace("\n", " ")
    text2.append(t)

all_verb_loose_set = get_verbs(text2)
all_verb_set = set()

print("Bombing")
bombing_set = get_similar(nlp("bomb"), all_verb_set)
print("Shoot")
shoot_set = get_similar(nlp("shoot"), all_verb_set)
print("Arrest")
arrest_set = get_similar(nlp("arrest"), all_verb_set)
print("Smuggle")
smuggle_set = get_similar(nlp("smuggle"), all_verb_set)
print("Seizure")
seizure_set = get_similar(nlp("seize"), all_verb_set)
print("Kidnap")
kidnap_set = get_similar(nlp("kidnap"), all_verb_set)
print("Robbery")
robbery_set = get_similar(nlp("robbery"), all_verb_set)
print("Kill")
kill_set = get_similar(nlp("kill"), all_verb_set)
print("Hijack")
hijack_set = get_similar(nlp("hijack"), all_verb_set)
print("crash")
crash_set = get_similar(nlp("crash"), all_verb_set)

print("Enter test Sentence")
# input_text = input()
doc_input = nlp("John was killed by Jack near Mumbai on Monday")


def get_new_data(doc_input1):
    dependency_tags = dict()
    entity_tags = dict()
    word_children_left = dict()
    word_children_left_count = dict()
    word_children_right = dict()
    word_children_right_count = dict()

    for token in doc_input1:
        word_children_left[token.text] = token.lefts
        word_children_left_count[token.text] = token.n_lefts
        word_children_right[token.text] = token.rights
        word_children_right_count[token.text] = token.n_rights

    for token in doc_input1:
        if token.dep_ in dependency_tags.keys():
            dependency_tags[token.dep_].add(token.text)
        else:
            value_set = set()
            value_set.add(token.text)
            dependency_tags[token.dep_] = value_set

    for entity in doc_input1.ents:
        entity_tags[entity.label_] = entity

    root_word = dependency_tags["ROOT"]
    root_left_child1 = word_children_left[list(root_word)[0]]
    root_right_child1 = word_children_right[list(root_word)[0]]
    return entity_tags, dependency_tags, word_children_left, word_children_left_count, word_children_right, word_children_right_count, root_word, root_left_child1, root_right_child1


input_verb = set()

for tok in doc_input:
    if tok.tag_ == "VB" or tok.tag_ == "VBD" or tok.tag_ == "VBG" or tok.tag_ == "VBN" or tok.tag_ == "VBP" or tok.tag_ == "VBZ":
        if tok not in input_verb:
            input_verb.add(tok.text)


for verb in input_verb:

    if verb.lower() in bombing_set or verb.upper() in bombing_set:
        print("Bombing")
        entity_tags, dependency_tags, word_children_left, word_children_left_count, word_children_right, word_children_right_count, root_word, root_left_child, root_right_child = get_new_data(
            doc_input)
        invoke_verb.bombing(entity_tags, dependency_tags, word_children_left, word_children_left_count,
                            word_children_right, word_children_right_count, root_word, root_left_child,
                            root_right_child)

    if verb.lower() in shoot_set or verb.upper() in shoot_set:
        print("Shoot")
        entity_tags, dependency_tags, word_children_left, word_children_left_count, word_children_right, word_children_right_count, root_word, root_left_child, root_right_child = get_new_data(
            doc_input)
        invoke_verb.shoot(entity_tags, dependency_tags, word_children_left,
                          word_children_left_count, word_children_right, word_children_right_count, root_word,
                          root_left_child, root_right_child)
    if verb.lower() in arrest_set or verb.upper() in arrest_set:
        print("Arrest")
        entity_tags, dependency_tags, word_children_left, word_children_left_count, word_children_right, word_children_right_count, root_word, root_left_child, root_right_child = get_new_data(
            doc_input)
        invoke_verb.arrest(entity_tags, dependency_tags, word_children_left,
                           word_children_left_count, word_children_right, word_children_right_count, root_word,
                           root_left_child, root_right_child)
    if verb.lower() in smuggle_set or verb.upper() in smuggle_set:
        print("Smuggle")
        entity_tags, dependency_tags, word_children_left, word_children_left_count, word_children_right, word_children_right_count, root_word, root_left_child, root_right_child = get_new_data(
            doc_input)
        invoke_verb.smuggle(entity_tags, dependency_tags, word_children_left, word_children_left_count,
                            word_children_right, word_children_right_count, root_word, root_left_child,
                            root_right_child)
    if verb.lower() in seizure_set or verb.upper() in seizure_set:
        print("Seizure")
        entity_tags, dependency_tags, word_children_left, word_children_left_count, word_children_right, word_children_right_count, root_word, root_left_child, root_right_child = get_new_data(
            doc_input)
        invoke_verb.seizure(entity_tags, dependency_tags, word_children_left, word_children_left_count,
                            word_children_right, word_children_right_count, root_word, root_left_child,
                            root_right_child)
    if verb.lower() in kidnap_set or verb.upper() in kidnap_set:
        print("Kidnap")
        entity_tags, dependency_tags, word_children_left, word_children_left_count, word_children_right, word_children_right_count, root_word, root_left_child, root_right_child = get_new_data(
            doc_input)
        invoke_verb.kidnap(entity_tags, dependency_tags, word_children_left,
                           word_children_left_count, word_children_right, word_children_right_count, root_word,
                           root_left_child, root_right_child)
    if verb.lower() in robbery_set or verb.upper() in robbery_set:
        print("Robbery")
        entity_tags, dependency_tags, word_children_left, word_children_left_count, word_children_right, word_children_right_count, root_word, root_left_child, root_right_child = get_new_data(
            doc_input)
        invoke_verb.robbery(entity_tags, dependency_tags, word_children_left,
                            word_children_left_count, word_children_right, word_children_right_count, root_word,
                            root_left_child, root_right_child)
    if verb.lower() in kill_set or verb.upper() in kill_set:
        print("Kill")
        entity_tags, dependency_tags, word_children_left, word_children_left_count, word_children_right, word_children_right_count, root_word, root_left_child, root_right_child = get_new_data(
            doc_input)
        invoke_verb.kill(entity_tags, dependency_tags, word_children_left,
                         word_children_left_count, word_children_right, word_children_right_count, root_word,
                         root_left_child, root_right_child)
    if verb.lower() in hijack_set or verb.upper() in hijack_set:
        print("Hijack")
        entity_tags, dependency_tags, word_children_left, word_children_left_count, word_children_right, word_children_right_count, root_word, root_left_child, root_right_child = get_new_data(
            doc_input)
        invoke_verb.hijack(entity_tags, dependency_tags, word_children_left,
                           word_children_left_count, word_children_right, word_children_right_count, root_word,
                           root_left_child, root_right_child)
    if verb.lower() in crash_set or verb.upper() in crash_set:
        print("Crash")
        invoke_verb.crash(doc_input)

invoke_verb.recognize_person(doc_input)
