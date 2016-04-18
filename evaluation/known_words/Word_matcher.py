#!/usr/bin/env python
# -*- coding: utf-8 -*-

import  urllib2
import codecs
import json
import pylab as pl

#MACROS
_EPOCH_ = "Epoch"
_SEPARATOR_ = "----"
_URL_PREFIX_ = "http://sanskritdictionary.com/?iencoding=iast&q="
_URL_SUFFIX =  "&lang=sans&action=Search"
_HREFS_ = "href='/"
_HREFE_ = "/"

#Globals
learnt_words = {}       #Learnt sanskrit dictionary
not_found_words = {}    #Learnt unknown words
total_words = 0         #Totals words in each Epoch
matched_words = 0       #Matched words in each Epoch
val = 0.0               #Threshold to compute the accuracy
isTimeToCompute = False
accuracy = []           #List of accuracy results for each epoch which is used to plot the graph (Y-Axis)
Epoch = []              #List of Epoch values(X-axis)

#inilialize the dictionary words and the words that are not in the dicitonary (this helps in improving the runtime)
def initializeDictionary():
    global learnt_words, not_found_words
    with codecs.open("learn_dict.txt", "r", "utf-8") as f:
        learnt_words = json.load(f)

    with codecs.open("Learntwords.txt", "r", "utf-8") as f:
        new = json.load(f)

    learnt_words.update(new)

    with codecs.open("Unkownwords.txt", "r", "utf-8") as f:
        not_found_words = json.load(f)

def dumpLearntItems():
    with codecs.open("Learntwords.txt", "w", "utf-8") as op:
        json.dump(learnt_words, op)
    with codecs.open("Unkownwords.txt", "w", "utf-8") as op:
        json.dump(not_found_words, op)

#Function to re-initialize the globals for the next iteration
def initilaizeForNextIteration(epoch_val):
    global val, isTimeToCompute, matched_words, total_words
    val = float(epoch_val)
    isTimeToCompute = True
    matched_words = 0
    total_words = 0

def plotAccuracyGraph(Epoch, accuracy):
    pl.plot(Epoch, accuracy,'r-')
    pl.xlabel('Epoch')
    pl.ylabel('Accuracy')
    pl.show()

def main():
    global learnt_words, not_found_words, matched_words, total_words, isTimeToCompute
    initializeDictionary()
    with codecs.open("log3.txt", "r", "utf-8") as fp:
        for line in fp.readlines():
            if _SEPARATOR_ in line: #Ignore the separator
                continue

            elif _EPOCH_ in line: #Initiliaze for computation only when the last computed Epoch was 0.3 or more away from the currect
                words = line.split()
                if val+0.3 <= float(words[1]):
                    initilaizeForNextIteration(words[1])
                else:
                    isTimeToCompute = False
                    continue

            elif isTimeToCompute:
                for word in line.split():
                    word = word.strip()
                    total_words += 1
                    if word not in learnt_words:
                        if word in not_found_words: #ignore the words already found as unknown
                            continue
                        try:
                            url = _URL_PREFIX_+ unicode(word) +_URL_SUFFIX
                            response = urllib2.urlopen(urllib2.unquote(url).encode("utf-8"))
                            html = response.read()
                            str1 = _HREFS_+unicode(word)+_HREFE_    #Form the string to be searched in HTTP response
                            if str1 in str(html).decode("utf-8"):   #Learn the found word
                                learnt_words[word] = None
                                matched_words += 1
                            else:
                                not_found_words[word] = None        #Learn the unknown word
                        except Exception:                           #Ignore the exceptions generated by bad char URLs
                            pass
                    else:
                        #the word is present in the learnt dictionary, hence, no need to make a http connection
                        matched_words += 1

                a = (float(matched_words)/total_words)*100
                accuracy.append(a)
                Epoch.append(val)

        dumpLearntItems()

    plotAccuracyGraph(Epoch, accuracy)

if __name__ == '__main__':
    main()