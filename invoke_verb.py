import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import spacy
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES

nlp = spacy.load('en_core_web_lg')


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


def get_string(token_child_set,number_of_children,string,word_children1_right,word_children1_right_count,word_children1_left,word_children1_left_count):
    while number_of_children>0:
        for child_token in token_child_set:
            string += " "+child_token.text
            string = get_compound(child_token.lefts,"") + " "+ string
            if "obj" in child_token.dep_:
                number_of_children = 0
                break
            else:
                number_of_children = number_of_children - 1
                string += " " + get_string(word_children1_right[child_token.text],
                                           word_children1_right_count[child_token.text], "", word_children1_right,
                                           word_children1_right_count,word_children1_left,word_children1_left_count)
    return string


def get_compound(token_left_child,string):
    for tok in token_left_child:
        if tok.dep_ == "compound":
            string = tok.text + " " + string
    return string


def fill_template1(entity_tags1, depend_tag, word_child_left, word_child_left_count, word_child_right, word_child_right_count, root1_word, root1_left_child, root1_right_child):
    if "nsubjpass" not in depend_tag.keys():
        subject_string = ""
        if word_child_left_count[list(root1_word)[0]] != 0:
            for token in root1_left_child:
                if token.dep_ == "nsubj":
                    token_right_child = word_child_right[token.text]
                    token_right_count = word_child_right_count[token.text]
                    subject_string += token.text
                    subject_string += get_string(token_right_child,token_right_count,"",word_child_right,word_child_right_count,word_child_left,word_child_left_count)
                    subject_string = get_compound(token.lefts, "") + " " + subject_string

        print("Killer: ",subject_string)
        object_string = list()
        if word_child_right_count[list(root1_word)[0]] != 0 :
            for token in root1_right_child:
                token_right_child = word_child_right[token.text]
                token_right_count = word_child_right_count[token.text]
                string = token.text
                if "obj" not in token.dep_:
                    string += " "+get_string(token_right_child,token_right_count,"",word_child_right,word_child_right_count,word_child_left,word_child_left_count)
                    string = get_compound(token.lefts, "") + " " + string
                    object_string.append(string)
                else:
                    string = get_compound(token.lefts, "") + " " + string
                    object_string.append(string)

        print(object_string)
        doc1 = nlp("victim")
        index = -1
        max = 0
        for i in range(0,len(object_string)):
            score = doc1.similarity(nlp(object_string[i]))
            print(score)
            if max<score:
                max = score
                index = i
        print("Victim: ",object_string[index])
        if "DATE" in entity_tags1.keys():
            print("Date: ", entity_tags1["DATE"])
        elif "TIME" in entity_tags1.keys():
            print("Time: ", entity_tags1["TIME"])
        if "GPE" in entity_tags1.keys():
            print("Location: ", entity_tags1["GPE"])
        elif "LOC" in entity_tags1.keys():
            print("Location: ", entity_tags1["LOC"])

    else:
        subject_string = ""
        if word_child_left_count[list(root1_word)[0]] != 0:
            for token in root1_left_child:
                if token.dep_ == "nsubjpass":
                    token_right_child = word_child_right[token.text]
                    token_right_count = word_child_right_count[token.text]
                    subject_string += token.text
                    subject_string += get_string(token_right_child, token_right_count, "", word_child_right,
                                                 word_child_right_count,word_child_left,word_child_left_count)
                    subject_string = get_compound(token.lefts,"") + " " + subject_string

        print("Victim: ", subject_string)
        object_string = list()
        if word_child_right_count[list(root1_word)[0]] != 0:
            for token in root1_right_child:
                token_right_child = word_child_right[token.text]
                token_right_count = word_child_right_count[token.text]
                string = token.text
                string += " " + get_string(token_right_child, token_right_count, "", word_child_right,
                                           word_child_right_count,word_child_left,word_child_left_count)
                string = get_compound(token.lefts,"")  + " " + string
                object_string.append(string)

        print(object_string)
        final_string = ""
        for s in object_string:
            if "by" in s:
                final_string = s
                break
            else:
                final_string = "NULL"
        print("Killer: ",final_string )
        if "DATE" in entity_tags1.keys():
            print("Date: ", entity_tags1["DATE"])
        elif "TIME" in entity_tags1.keys():
            print("Time: ", entity_tags1["TIME"])
        if "GPE" in entity_tags1.keys():
            print("Location: ", entity_tags1["GPE"])
        elif "LOC" in entity_tags1.keys():
            print("Location: ", entity_tags1["LOC"])


def fill_template2(entity_tags1, depend_tag, word_child_left, word_child_left_count, word_child_right, word_child_right_count, root1_word, root1_left_child, root1_right_child):
    if "nsubjpass" not in depend_tag.keys():
        subject_string = ""
        if word_child_left_count[list(root1_word)[0]] != 0:
            for tok in root1_left_child:
                if tok.dep_ == "nsubj":
                    token_right_child = word_child_right[tok.text]
                    token_right_count = word_child_right_count[tok.text]
                    subject_string += tok.text
                    subject_string += get_string(token_right_child,token_right_count,"",word_child_right,word_child_right_count,word_child_left,word_child_left_count)
                    subject_string = get_compound(tok.lefts, "") + " " + subject_string

        print("Perpetrator: ",subject_string)
        object_string = list()
        if word_child_right_count[list(root1_word)[0]] != 0:
            for tok in root1_right_child:
                token_right_child = word_child_right[tok.text]
                token_right_count = word_child_right_count[tok.text]
                string = tok.text
                string += " " + get_string(token_right_child, token_right_count, "", word_child_right,
                                           word_child_right_count, word_child_left, word_child_left_count)
                string = get_compound(tok.lefts, "") + " " + string
                object_string.append(string)


        print(object_string)
        from_string = "NULL"
        to_string = "NULL"
        for s in object_string:
            if "from" in s:
                from_string = s
            if "towards" in s:
                to_string = s

        if from_string != "NULL":
            object_string.remove(from_string)
        if to_string != "NULL":
            object_string.remove(to_string)

        print("From: ",from_string)
        print("To: ",to_string)


        index1 = -1
        max1 = 0
        doc11 = nlp("item")
        for i in range(0, len(object_string)):
            if max1 < doc11.similarity(nlp(object_string[i])):
                max1 = doc11.similarity(nlp(object_string[i]))
                index1 = i
        print("Item: ", object_string[index1])

        if "CARDINAL" in entity_tags.keys():
            print("Quantity: ",entity_tags["CARDINAL"])
        elif "QUANTITY"  in  entity_tags.keys():
            print("Quantity: ",entity_tags["QUANTITY"])

    else:
        subject_string = ""
        if word_child_left_count[list(root1_word)[0]] != 0:
            for tok in root1_left_child:
                if tok.dep_ == "nsubjpass":
                    token_right_child = word_child_right[tok.text]
                    token_right_count = word_child_right_count[tok.text]
                    subject_string += tok.text
                    subject_string += get_string(token_right_child, token_right_count, "", word_child_right,
                                                 word_child_right_count,word_child_left,word_child_left_count)
                    subject_string = get_compound(tok.lefts, "") + " " + subject_string

        print("Item : ", subject_string)
        object_string = list()
        if word_child_right_count[list(root1_word)[0]] != 0:
            for tok in root1_right_child:
                token_right_child = word_child_right[tok.text]
                token_right_count = word_child_right_count[tok.text]
                string = tok.text
                string += " " + get_string(token_right_child, token_right_count, "", word_child_right,
                                           word_child_right_count,word_child_left,word_child_left_count)
                string = get_compound(tok.lefts, "") + " " + string
                object_string.append(string)

        final_string = ""
        for s in object_string:
            if "by" in s:
                final_string = s
                break
            else:
                final_string = "NULL"
        print("Perpetrator: ", final_string)
        print(object_string)
        from_string = "NULL"
        to_string = "NULL"
        for s in object_string:
            if "from" in s:
                from_string = s
            if "towards" in s:
                to_string = s

        if from_string != "NULL":
            object_string.remove(from_string)
        if to_string != "NULL":
            object_string.remove(to_string)

        print("From: ", from_string)
        print("To: ", to_string)


def fill_template3(document):
    doc_sim = nlp("vehicle")
    word_set = list()
    for tok in document:
        word_set.append(tok.text)
    max1 = 0
    index = -1
    for i in range(0,len(word_set)):
        score = doc_sim.similarity(nlp(word_set[i]))
        if max1 < score:
            index1 = i
            max1 = score
    print("Vehicle: ",word_set[i])


    for entity1 in  document.ents:
        if entity1.label_ == "LOCATION" or entity1.label_ == "GPE":
            print("Location: ",entity)


# file_path = "/Users/mohit/Desktop/a.txt"
# file = open(file_path, 'r',encoding="utf-8")
# text = file.read()
# text1 = text.split(".")
# text2 = list("")
# for t in text1:
#     t = t.replace("\n"," ")
#     text2.append(t)

# all_verb_set = get_verbs(text2)
# shot_set = get_similar(nlp("shot"),all_verb_set)
# kidnap_set = get_similar(nlp("kidnap"),all_verb_set)


print("Enter Test Sentence")
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

fill_template2(entity_tags,dependency_tags,word_children_left,word_children_left_count,word_children_right,word_children_right_count,root_word,root_left_child,root_right_child)




