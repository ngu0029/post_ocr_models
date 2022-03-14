# -*- coding: utf-8 -*-
"""
@author: NQDUNG @ VLU

Note: Many modifications have been made based on the original code published by Pytorch @
https://pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html
"""

SOS_token = 0
EOS_token = 1
UNK_token = 2

class Lang:
    """ Lang class includes
            -- word → index (word2index) dictionary 
            -- index → word (index2word) dictionary
            -- a count of each word (word2count)
    """
    def __init__(self, name):
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {0: "SOS", 1: "EOS", 2: "UNK"}
        self.n_words = 3

    def addSentence(self, sentence):
        for word in sentence.split('|'):
            self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1
            
def readLangs(lang1, lang2, reverse=False, enrich='aed'):
    """ 
        The readLangs function includes:
        -- read the data file 
        -- split the file into lines
        -- split lines into pairs
    """
    print("Reading lines...")
    # Read the file and split into lines
    if enrich == 'aed':
        lines = open('train_%s-%s.txt' % (lang1, lang2), encoding='utf-8').\
            read().strip().split('\n')
    elif enrich == 'vtb':
        lines = open('train_%s-%s_vtb.txt' % (lang1, lang2), encoding='utf-8').\
            read().strip().split('\n')
    else: # vtb + aed
        lines = open('train_%s-%s_enriched.txt' % (lang1, lang2), encoding='utf-8').\
            read().strip().split('\n')

    # Split every line into pairs
    pairs = [[s for s in l.split('\t')] for l in lines]

    # Reverse pairs, make Lang instances
    if reverse:
        pairs = [list(reversed(p)) for p in pairs]
        input_lang = Lang(lang2)
        output_lang = Lang(lang1)
    else:
        input_lang = Lang(lang1)
        output_lang = Lang(lang2)

    return input_lang, output_lang, pairs

MAX_LENGTH = 147 # based on AED train sentences

def filterPair(p):
    """ Trim the data set to MAX_LENGTH sentences """
    return len(p[0].split('|')) < MAX_LENGTH and \
        len(p[1].split('|')) < MAX_LENGTH    

def filterPairs(pairs):
    return [pair for pair in pairs if filterPair(pair)]

def prepareData(lang1, lang2, reverse=False, enrich='aed'):
    """
        The full process for preparing the data is:
            -- Read text file and split into lines, split lines into pairs
            -- Filter by length
            -- Make word lists from sentences in pairs
    """
    input_lang, output_lang, pairs = readLangs(lang1, lang2, reverse, enrich)
    print("Read %s sentence pairs" % len(pairs))
    pairs = filterPairs(pairs)
    print("Trimmed to %s sentence pairs" % len(pairs))
    print("Counting words...")
    for pair in pairs:
        input_lang.addSentence(pair[0])
        output_lang.addSentence(pair[1])
    print("Counted words:")
    print(input_lang.name, input_lang.n_words)
    print(output_lang.name, output_lang.n_words)
    return input_lang, output_lang, pairs