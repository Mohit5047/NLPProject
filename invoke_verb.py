import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import spacy
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES

nlp = spacy.load('en_core_web_lg')


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


def bombing(entity_tags1, depend_tag, word_child_left, word_child_left_count, word_child_right, word_child_right_count, root1_word, root1_left_child, root1_right_child):
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

        print("Bomber/Perpetrator: ",subject_string)
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
        print("Target: ",object_string[index])
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

        print("Target: ", subject_string)
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
        print("Bomber/Perpetrator: ",final_string )
        if "DATE" in entity_tags1.keys():
            print("Date: ", entity_tags1["DATE"])
        elif "TIME" in entity_tags1.keys():
            print("Time: ", entity_tags1["TIME"])
        if "GPE" in entity_tags1.keys():
            print("Location: ", entity_tags1["GPE"])
        elif "LOC" in entity_tags1.keys():
            print("Location: ", entity_tags1["LOC"])


def shoot(entity_tags1, depend_tag, word_child_left, word_child_left_count, word_child_right, word_child_right_count, root1_word, root1_left_child, root1_right_child):
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

        print("Shooter/Perpetrator: ",subject_string)
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
        print("Target/Victim: ",object_string[index])
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

        print("Target/Victim: ", subject_string)
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
        print("Shooter/Perpetrator: ",final_string )
        if "DATE" in entity_tags1.keys():
            print("Date: ", entity_tags1["DATE"])
        elif "TIME" in entity_tags1.keys():
            print("Time: ", entity_tags1["TIME"])
        if "GPE" in entity_tags1.keys():
            print("Location: ", entity_tags1["GPE"])
        elif "LOC" in entity_tags1.keys():
            print("Location: ", entity_tags1["LOC"])


def arrest(entity_tags1, depend_tag, word_child_left, word_child_left_count, word_child_right, word_child_right_count, root1_word, root1_left_child, root1_right_child):
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

        print("Arrester: ",subject_string)
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
        max1 = 0
        for i in range(0,len(object_string)):
            score = doc1.similarity(nlp(object_string[i]))
            print(score)
            if max1<score:
                max1 = score
                index = i
        print("Criminal: ",object_string[index])
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

        print("Criminal: ", subject_string)
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
        print("Arrester: ",final_string )
        if "DATE" in entity_tags1.keys():
            print("Date: ", entity_tags1["DATE"])
        elif "TIME" in entity_tags1.keys():
            print("Time: ", entity_tags1["TIME"])
        if "GPE" in entity_tags1.keys():
            print("Location: ", entity_tags1["GPE"])
        elif "LOC" in entity_tags1.keys():
            print("Location: ", entity_tags1["LOC"])


def smuggle(entity_tags1, depend_tag, word_child_left, word_child_left_count, word_child_right, word_child_right_count, root1_word, root1_left_child, root1_right_child):
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

        if "CARDINAL" in entity_tags1.keys():
            print("Quantity: ",entity_tags1["CARDINAL"])
        elif "QUANTITY"  in  entity_tags1.keys():
            print("Quantity: ",entity_tags1["QUANTITY"])

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
        index1 = -1
        max1 = 0
        doc11 = nlp("item")
        for i in range(0, len(object_string)):
            if max1 < doc11.similarity(nlp(object_string[i])):
                max1 = doc11.similarity(nlp(object_string[i]))
                index1 = i
        print("Item: ", object_string[index1])

        if "CARDINAL" in entity_tags1.keys():
            print("Quantity: ", entity_tags1["CARDINAL"])
        elif "QUANTITY" in entity_tags1.keys():
            print("Quantity: ", entity_tags1["QUANTITY"])


def seizure(entity_tags1, depend_tag, word_child_left, word_child_left_count, word_child_right, word_child_right_count, root1_word, root1_left_child, root1_right_child):
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

        print("Authority: ",subject_string)
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

        index1 = -1
        max1 = 0
        doc11 = nlp("item")
        for i in range(0, len(object_string)):
            if max1 < doc11.similarity(nlp(object_string[i])):
                max1 = doc11.similarity(nlp(object_string[i]))
                index1 = i
        print("Item: ", object_string[index1])

        if "CARDINAL" in entity_tags1.keys():
            print("Quantity: ",entity_tags1["CARDINAL"])
        elif "QUANTITY"  in  entity_tags1.keys():
            print("Quantity: ",entity_tags1["QUANTITY"])
        if "GPE" in entity_tags1.keys():
            print("Location: ", entity_tags1["GPE"])
        elif "LOC" in entity_tags1.keys():
            print("Location: ", entity_tags1["LOC"])

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

        index1 = -1
        max1 = 0
        doc11 = nlp("authority")
        for i in range(0, len(object_string)):
            if max1 < doc11.similarity(nlp(object_string[i])):
                max1 = doc11.similarity(nlp(object_string[i]))
                index1 = i
        print("Authority: ", object_string[index1])

        if "CARDINAL" in entity_tags1.keys():
            print("Quantity: ", entity_tags1["CARDINAL"])
        elif "QUANTITY" in entity_tags1.keys():
            print("Quantity: ", entity_tags1["QUANTITY"])
        if "GPE" in entity_tags1.keys():
            print("Location: ", entity_tags1["GPE"])
        elif "LOC" in entity_tags1.keys():
            print("Location: ", entity_tags1["LOC"])


def kidnap(entity_tags1, depend_tag, word_child_left, word_child_left_count, word_child_right, word_child_right_count, root1_word, root1_left_child, root1_right_child):
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

        print("Kidnapper/Perpetrator: ",subject_string)
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
        print("Target/Victim: ",object_string[index])
        if "DATE" in entity_tags1.keys():
            print("Date: ", entity_tags1["DATE"])
        elif "TIME" in entity_tags1.keys():
            print("Time: ", entity_tags1["TIME"])

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

        print("Target/Victim: ", subject_string)
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
        print("Kidnapper/Perpetrator: ",final_string )
        if "DATE" in entity_tags1.keys():
            print("Date: ", entity_tags1["DATE"])
        elif "TIME" in entity_tags1.keys():
            print("Time: ", entity_tags1["TIME"])


def robbery(entity_tags1, depend_tag, word_child_left, word_child_left_count, word_child_right, word_child_right_count, root1_word, root1_left_child, root1_right_child):
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

        print("Robber/Perpetrator: ",subject_string)
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

        doc1 = nlp("target")
        index = -1
        max1 = 0
        for i in range(0,len(object_string)):
            score = doc1.similarity(nlp(object_string[i]))
            print(score)
            if max1<score:
                max1 = score
                index = i
        print("Victim: ",object_string[index])
        object_string.remove(object_string[index])
        doc2 = nlp("item")
        index1 = -1
        max2 = 0
        for i in range(0, len(object_string)):
            score = doc2.similarity(nlp(object_string[i]))
            print(score)
            if max2 < score:
                max2 = score
                index1 = i
        if index1 != -1:
            print("Item: ", object_string[index1])
            object_string.remove(object_string[index1])
        if "DATE" in entity_tags1.keys():
            print("Date: ", entity_tags1["DATE"])
        elif "TIME" in entity_tags1.keys():
            print("Time: ", entity_tags1["TIME"])


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

        print("Target: ", subject_string)
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

        final_string = ""
        for s in object_string:
            if "by" in s:
                final_string = s
                break
            else:
                final_string = "NULL"
        print("Robber/Perpetrator: ",final_string )
        object_string.remove(final_string)
        doc2 = nlp("item")
        index1 = -1
        max2 = 0
        for i in range(0, len(object_string)):
            score = doc2.similarity(nlp(object_string[i]))
            print(score)
            if max2 < score:
                max2 = score
                index1 = i
        if index1 != -1:
            print("Item: ", object_string[index1])
            object_string.remove(object_string[index1])
        if "DATE" in entity_tags1.keys():
            print("Date: ", entity_tags1["DATE"])
        elif "TIME" in entity_tags1.keys():
            print("Time: ", entity_tags1["TIME"])


def kill(entity_tags1, depend_tag, word_child_left, word_child_left_count, word_child_right, word_child_right_count, root1_word, root1_left_child, root1_right_child):
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

        print("Killer/Perpetrator: ",subject_string)
        object_string = list()
        if word_child_right_count[list(root1_word)[0]] != 0 :
            for tok in root1_right_child:
                token_right_child = word_child_right[tok.text]
                token_right_count = word_child_right_count[tok.text]
                string = tok.text
                if "obj" not in tok.dep_:
                    string += " "+get_string(token_right_child,token_right_count,"",word_child_right,word_child_right_count,word_child_left,word_child_left_count)
                    string = get_compound(tok.lefts, "") + " " + string
                    object_string.append(string)
                else:
                    string = get_compound(tok.lefts, "") + " " + string
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
        print("Target/Victim: ",object_string[index])
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
            for tok in root1_left_child:
                if tok.dep_ == "nsubjpass":
                    token_right_child = word_child_right[tok.text]
                    token_right_count = word_child_right_count[tok.text]
                    subject_string += tok.text
                    subject_string += get_string(token_right_child, token_right_count, "", word_child_right,
                                                 word_child_right_count,word_child_left,word_child_left_count)
                    subject_string = get_compound(tok.lefts, "") + " " + subject_string

        print("Target/Victim: ", subject_string)
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

        print(object_string)
        final_string = ""
        for s in object_string:
            if "by" in s:
                final_string = s
                break
            else:
                final_string = "NULL"
        print("Killer/Perpetrator: ",final_string )
        if "DATE" in entity_tags1.keys():
            print("Date: ", entity_tags1["DATE"])
        elif "TIME" in entity_tags1.keys():
            print("Time: ", entity_tags1["TIME"])
        if "GPE" in entity_tags1.keys():
            print("Location: ", entity_tags1["GPE"])
        elif "LOC" in entity_tags1.keys():
            print("Location: ", entity_tags1["LOC"])


def hijack(entity_tags1, depend_tag, word_child_left, word_child_left_count, word_child_right, word_child_right_count, root1_word, root1_left_child, root1_right_child):
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

        print("Hijacker/Perpetrator: ",subject_string)
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
        doc1 = nlp("target")
        index = -1
        max1 = 0
        for i in range(0,len(object_string)):
            score = doc1.similarity(nlp(object_string[i]))
            print(score)
            if max1<score:
                max1 = score
                index = i
        print("Target: ",object_string[index])
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

        print("Target: ", subject_string)
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
        print("Hijacker/Perpetrator: ",final_string )
        if "DATE" in entity_tags1.keys():
            print("Date: ", entity_tags1["DATE"])
        elif "TIME" in entity_tags1.keys():
            print("Time: ", entity_tags1["TIME"])
        if "GPE" in entity_tags1.keys():
            print("Location: ", entity_tags1["GPE"])
        elif "LOC" in entity_tags1.keys():
            print("Location: ", entity_tags1["LOC"])


def crash(document):
    doc_sim = nlp("vehicle")
    word_set = list()
    for tok in document:
        word_set.append(tok.text)
    max1 = 0
    index1 = -1
    for i in range(0,len(word_set)):
        score = doc_sim.similarity(nlp(word_set[i]))
        if max1 < score:
            index1 = i
            max1 = score
    print("Vehicle: ",word_set[index1])

    for entity1 in document.ents:
        if entity1.label_ == "LOCATION" or entity1.label_ == "GPE":
            print("Location: ",entity1)


def recognize_person(document):
    entity_labels = dict()
    for entity1 in document.ents:
        entity_labels[entity1.label_] = entity1
    if "PERSON" in  entity_labels.keys():
        print("Person: ",entity_labels["PERSON"])
    if "ORG" in  entity_labels.keys():
        print("Orgranization: ",entity_labels["ORG"])







