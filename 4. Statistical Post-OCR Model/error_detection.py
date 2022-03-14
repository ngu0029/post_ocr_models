# -*- coding: utf-8 -*-
"""
@author: NQDUNG @ VLU
"""
import re, os, json
from build_ngrams import is_not_punctuation
from helpers import COUNTS1, COUNTS2, COUNTS3

delimiters = ".,;\"):?!\n"

def context_words(token, search_text):
  """
    Find 2 words before and after specified token
  """
  if not token: return '', '', '', ''
  
  regex = r"(?:\S+\s){0,2}\S*" + re.escape(token) + r"\S*(?:\s\S+){0,2}"
  contexts = re.findall(regex, search_text, re.IGNORECASE)
  if not contexts: return '', '', '', ''
  
  for context in contexts:
    words = context.split()
    for i, w in enumerate(words):
      if w == token.split()[0]: # token can be one- or two-syllable length
        if len(token.split()) == 1:
          ahead_2w = '' if i-2 < 0 else words[i-2]
          ahead_1w = '' if i-1 < 0 else words[i-1]
          behind_1w = '' if i+1 >= len(words) else words[i+1]
          behind_2w = '' if i+2 >= len(words) else words[i+2]
          break
        elif len(token.split()) == 2:
          ahead_2w = '' if i-2 < 0 else words[i-2]
          ahead_1w = '' if i-1 < 0 else words[i-1]
          behind_1w = '' if i+2 >= len(words) else words[i+2] # increase the index by 1
          behind_2w = '' if i+3 >= len(words) else words[i+3] # increase the index by 1
          break
    if w == token: break

  # This code segment should be put before checking context words ended by delimiters
  # process context words beginning with "\"("
  if ahead_2w and ahead_2w[0] in "\"(": pass # ahead_2w = ahead_2w[1:]
  if ahead_1w and ahead_1w[0] in "\"(": ahead_2w = '' # ahead_2w, ahead_1w = '', ahead_1w[1:]  
  if token and token[0] in "\"(": ahead_2w, ahead_1w = '', ''
  if behind_1w and behind_1w[0] in "\"(": behind_1w, behind_2w = '', ''
  if behind_2w and behind_2w[0] in "\"(": behind_2w = ''    
      
  # process context words ended by delimiters
  # or context words not in COUNTS1 vocabulary (non-word syllables), not taking in consideration
  if (ahead_2w and ahead_2w[-1] in delimiters) or ahead_2w not in COUNTS1: 
    ahead_2w = ''
  if (ahead_1w and ahead_1w[-1] in delimiters) or ahead_1w not in COUNTS1: 
    ahead_2w, ahead_1w = '', ''
  if token and token[-1] in delimiters: behind_1w, behind_2w = '', ''
  if (behind_1w and behind_1w[-1] in delimiters) or behind_1w not in COUNTS1: 
    behind_1w, behind_2w = behind_1w[:-1], ''
  if (behind_2w and behind_2w[-1] in delimiters) or behind_2w not in COUNTS1: 
    behind_2w = behind_2w[:-1]

  return ahead_2w, ahead_1w, behind_1w, behind_2w

def find_context_text(ocr_output, word_begin_index, word_end_index):
  """ Find context text of specified token """  
  if word_end_index != -1:
    token = ocr_output[word_begin_index:word_end_index]
    context_text = ocr_output[((word_begin_index-24) if (word_begin_index-24) >=0 else 0):
                              ((word_end_index+24) if (word_end_index+24) <= len(ocr_output) else len(ocr_output))]
  else: # last token
    token = ocr_output[word_begin_index:]
    context_text = ocr_output[(word_begin_index-24 if word_begin_index-24 >=0 else 0):]
    
  return token, context_text

def is_abbre_word(token):
  # abbreviation, e.g. W.C.
  abbre_regex = r"^([A-Z]\.)+$"
  return re.search(abbre_regex, token)

def is_decimal_num(token):  
  # decimal number, e.g. 7,50; 300.000
  decimal_num = r"^[0-9]+[.,][0-9]+$"
  return re.search(decimal_num, token)

def remove_token_delimiters(token):
  # if token is ended by a delimiter, e.g. "good,", "bye.", remove the delimiter
  if token and token[-1] in delimiters: token = token[:-1]
  if token and token[0] in "\"(": token = token [1:]
  return token

def is_token_erroneous(ocr_output, word_begin_index, word_end_index):
  """ Test if token is erroneous """  
  # context_text is not used in this function
  token, context_text = find_context_text(ocr_output, word_begin_index, word_end_index)
  
  # this check should happen before removing token delimiters
  abbre_word = is_abbre_word(token)
  decimal_num = is_decimal_num(token)
   
  # if token is ended by a delimiter, e.g. "good,", "bye.", remove the delimiter
  token = remove_token_delimiters(token)

  # add case of punctuation, e.g. "/-&" in 904|/|TB|-|UB|ngày|15|-|12|-|2003 and Tài|nguyên|&|môi|trường
  return token and \
         (token not in COUNTS1) and \
         (is_not_punctuation(token)) and \
         (not abbre_word) and \
         (not decimal_num) and \
         (token.upper() not in COUNTS1) and (token.lower() not in COUNTS1) and \
         (not re.search(r'^(£|$)[0-9]+', token)) and \
         (not token.isnumeric())

def is_token_context_erroneous(ocr_output, word_begin_index, word_end_index):
  """ Test if token context is erroneous """
  def is_not_bigram(w1, w2):
    if w1 and w2:
      return (w1 + ' ' + w2) not in COUNTS2
    else:
      return True # bigram does not exist. True means we do not care this case.
  
  def is_not_trigram(w1, w2, w3):
    if w1 and w2 and w3:
      return (w1 + ' ' + w2 + ' ' + w3) not in COUNTS3
    else:
      return True # trigram does not exist. True means we do not care this case.  
  
  token, context_text = find_context_text(ocr_output, word_begin_index, word_end_index)
          
  context_text = ' '.join(context_text.split('|'))
  ahead_2w, ahead_1w, behind_1w, behind_2w = context_words(token, context_text)
      
  # this check should happen before removing token delimiters
  abbre_word = is_abbre_word(token)
  decimal_num = is_decimal_num(token)
    
  # remove the delimiter, e.g. "good,", "bye."
  token = remove_token_delimiters(token)
  
  # Ignore these cases of tokens (return False)
  if token and \
     ((not is_not_punctuation(token)) or \
      abbre_word or \
      decimal_num or \
      re.search(r'^(£|$)[0-9]+', token) or \
      token.isnumeric()):
    return False
  
  if ahead_2w or ahead_1w or behind_1w or behind_2w:
    is_not_context_word = token and \
                          (token in COUNTS1) and \
                          (is_not_bigram(ahead_1w, token)) and \
                          (is_not_bigram(token, behind_1w)) and \
                          (is_not_trigram(ahead_2w, ahead_1w, token)) and \
                          (is_not_trigram(ahead_1w, token, behind_1w)) and \
                          (is_not_trigram(token, behind_1w, behind_2w))
    return is_not_context_word
  else:  
    return False # all context words empty

work_directory_path = os.getcwd()
target_test_file = 'nn_outputs/test_output_gt_sentences_v2.txt'
  
def error_detection(filepath):
  """ Error detection phase """  
  print("Error detection: Start...")
  output_file = open(work_directory_path + "/Results/result_vn_words.json", "w")
  output_file.write("{")
  
  f_sentence = open(filepath, encoding='utf-8').readlines()
  for i in range(len(f_sentence)):
    if f_sentence[i].find('result_VNOnDB_line_offline') != -1:
      output_file.write("\n"+f_sentence[i].strip()+" ")
      #print(f_sentence[i].strip()) ###
      errors = {}
      ocr_output = f_sentence[i+1].strip()
      
      word_begin_index = 0

      for i, character in enumerate(ocr_output):
        if character in "|":
          word_end_index = i
          # check if the token is erroneous
          if is_token_erroneous(ocr_output, word_begin_index, word_end_index):
            errors[str(word_begin_index)+":1"] = {}
          if is_token_context_erroneous(ocr_output, word_begin_index, word_end_index):
            errors[str(word_begin_index)+":2"] = {}

          word_begin_index = word_end_index + 1

      # check if the last token in OCR text is erroneous
      if is_token_erroneous(ocr_output, word_begin_index, -1):
        errors[str(word_begin_index)+":1"] = {}
      if is_token_context_erroneous(ocr_output, word_begin_index, -1):
        errors[str(word_begin_index)+":2"] = {}
      # UTF-8 is as default for json.dumps
      output_file.write(json.dumps(errors, indent=8)+",")

  output_file.seek(0, 2) # uses the end of the file as the reference point
  output_file.truncate(output_file.tell() - 1) # remove last commas mark ','

  output_file = open(work_directory_path + "/Results/result_vn_words.json", "a") # appending
  output_file.write("\n}")
  output_file.close()
  
  print("Error detection: Done!")
  
if __name__ == "__main__":
  # do error detection
  error_detection(target_test_file)