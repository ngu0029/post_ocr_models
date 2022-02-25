# -*- coding: utf-8 -*-
"""
@author: NQDUNG @ VLU
"""
from string import punctuation
from collections import Counter
import re, os

data_directory_path = 'Kho ngu lieu 2 trieu am tiet da tach tu'
full_data_directory_paths = [data_directory_path]

def is_not_punctuation(token):
    """ Check if token is not a punctuation string """
    return True if [c for c in token if c not in punctuation] else False
  
def is_not_tag(token):
    """ Check if token is not in tag form """
    return False if re.search(r'<([\w\W]+)>', token) else True

def tokenization(text):
    "List all the syllable tokens (consecutive letters) in a text."
    tokens = text.split()
    syllables = []
    for token in tokens:
      syllables.extend(token.split('_')) # further split tokens that include '_', e.g. Đồng_Nai
    return [syllable for syllable in syllables if is_not_punctuation(syllable) and is_not_tag(syllable)] # get rid of punctuation and tag tokens
  
def tokenization_keep_punc(text):
    "Tokenize but still keep punctuation."
    tokens = text.split()
    syllables = []
    for token in tokens:
      syllables.extend(token.split('_')) # further split tokens that include '_', e.g. Đồng_Nai
    return [syllable for syllable in syllables if is_not_tag(syllable)] # get rid of tag tokens

def build_unigrams():
  """ Build unigrams (single syllables) """
  C = Counter()
  for full_data_directory_path in full_data_directory_paths:
    for root_path, directories, files in os.walk(full_data_directory_path):
      for file in files:        
        file_path = root_path + "/" + file
        txt = open(file_path).read()
        SYLLABLES = tokenization(txt)
        # build unigram
        buf_syllables = Counter(SYLLABLES)
        for s in buf_syllables: 
          C[s] = C.get(s, 0) + buf_syllables[s]
          
        #print("Processing " + file, ": Done...")
        #txt.close()
        del buf_syllables
        del SYLLABLES
        del txt
  
  print("Build unigrams: Done...")
  
  return C

def build_ngrams():
  """ Build bigrams and trigrams """
  C_2w, C_3w = Counter(), Counter()
  for full_data_directory_path in full_data_directory_paths:
    for root_path, directories, files in os.walk(full_data_directory_path):
      for file in files:        
        file_path = root_path + "/" + file
        txt = open(file_path).read()
        SYLLABLES = tokenization_keep_punc(txt) # tokenize but still keep punctuation
        if not SYLLABLES: continue # avoid empty files
          
        # build bigram and trigram. 
        i = 0
        while i < (len(SYLLABLES) - 2):
          w1, w2, w3 = SYLLABLES[i], SYLLABLES[i+1], SYLLABLES[i+2]
          if not is_not_punctuation(w1):
            i += 1
            continue
          else:            
            if not is_not_punctuation(w2):
              i += 2 # jump over the punctuation word
              continue
            else:
              biword = w1 + " " + w2
              C_2w[biword] = C_2w.get(biword, 0) + 1
              if not is_not_punctuation(w3):
                i += 3 # jump over the punctuation word
                continue
              else:
                triword = w1 + " " + w2 + " " + w3
                C_3w[triword] = C_3w.get(triword, 0) + 1
              i += 1 # IMPORTANT! Otherwise, loop forever
        if is_not_punctuation(SYLLABLES[-2]) and is_not_punctuation(SYLLABLES[-1]):
          biword = SYLLABLES[-2] + " " + SYLLABLES[-1] # last biword in file
          C_2w[biword] = C_2w.get(biword, 0) + 1
                 
        #print("Processing " + file, ": Done...")
        #txt.close()
        del SYLLABLES
        del txt
  
  print("Build n-grams: Done...")
  return C_2w, C_3w

# build unigram vocabulary. 
unigram_dict = build_unigrams()

# build bigram and trigram dictionaries. 
bigram_dict, trigram_dict = build_ngrams()
