# -*- coding: utf-8 -*-
"""
@author: NQDUNG @ VLU
"""
import re, os, operator

data_directory_path = 'InkData_paragraph'
full_data_directory_paths = [data_directory_path]

def generate_char_vocab():
  """ Generate Vietnamese character vocabulary """
  vnchars = []
  
  for full_data_directory_path in full_data_directory_paths:
    for root_path, directories, files in os.walk(full_data_directory_path):
      for file in files:        
        file_path = root_path + "/" + file
        txt = open(file_path).read()
        paragraphs = re.compile(r'<Tg_Truth>(.*?)</Tg_Truth>', re.DOTALL).findall(txt)
        # Enrich with more syllables
        for s in paragraphs:
          for c in s:
            if c not in vnchars:
              vnchars.extend(c)
        
  #print("Generating Vietnamese character vocabulary: Done...")
  return vnchars
  
def generate_char_types():
  """ Generate character types like digits, uppers, lowers, special symbols """
  vnchars = generate_char_vocab()
  vndigits, vnuppers, vnlowers, vnsymbols = [], [], [], []

  for c in vnchars:
    if c.isdigit():
      if c not in vndigits:
        vndigits.extend(c)
    elif c.isupper():
      if c not in vnuppers:
        vnuppers.extend(c)
    elif c.islower():
      if c not in vnlowers:
        vnlowers.extend(c)
    else:
      if c not in vnsymbols:
        vnsymbols.extend(c)
    
  return vndigits, vnuppers, vnlowers, vnsymbols

def is_not_aligned_correctly(ocr_aligned, gs_aligned):
  """ Check if OCR text and GS text are aligned """  
  return len(ocr_aligned) != len(gs_aligned) # aligned at word level

def find_edit_patterns(filepath, edit_patterns):
  """ Find edit patterns in the OCR-GS texts """  
  vndigits, vnuppers, vnlowers, _ = generate_char_types()
  alphabet_allCase = ''.join(vndigits + vnuppers + vnlowers + [" ", ".", ",", "(", ")", "/"])
  
  f_sentence = open(filepath, encoding='utf-8').readlines()
  for i in range(len(f_sentence)):
    if f_sentence[i].find('result_VNOnDB_line_offline') != -1:
      #print(f_sentence[i].strip()) ###

      ocr_syllables_aligned = f_sentence[i+1].strip().split('|') # ocr syllables aligned
      gs_syllables_aligned = f_sentence[i+2].strip().split('|') # gs syllables aligned
      
      if is_not_aligned_correctly(ocr_syllables_aligned, gs_syllables_aligned):
        print("!!! File \"" + f_sentence[i] + "\" OCR_aligned and GS_aligned are not aligned properly\n")
        continue
      
      # A more arbitrary mapping
      for s_th in range(len(ocr_syllables_aligned)):
        ocr_aligned = ocr_syllables_aligned[s_th] # ocr syllable @ s_th position
        gs_aligned = gs_syllables_aligned[s_th] # gs syllable @ s_th position
        if ("#" in gs_aligned) or ("#" in ocr_aligned): continue
        if len(ocr_aligned) != len(gs_aligned):
          print(ocr_aligned, gs_aligned)
          continue
        for i in range(len(ocr_aligned)):
          if (gs_aligned[i] != ocr_aligned[i]) and (gs_aligned[i] != "@") and (ocr_aligned[i] != "@"):
            key = gs_aligned[i] + "|" + ocr_aligned[i]
            edit_patterns[key] = edit_patterns.get(key, 0) + 1

          if i < (len(ocr_aligned)-1):
            if (gs_aligned[i] != ocr_aligned[i]) and (gs_aligned[i+1] != ocr_aligned[i+1]) \
            and ((gs_aligned[i:i+2]) != "@@") and ((ocr_aligned[i:i+2]) != "@@"):
              key = (gs_aligned[i:i+2]).replace("@", "") + "|" + (ocr_aligned[i:i+2]).replace("@", "")
              edit_patterns[key] = edit_patterns.get(key, 0) + 1

            # Add cases of deletion and insertion
            if (gs_aligned[i] in alphabet_allCase) and (gs_aligned[i+1] in alphabet_allCase) \
            and (ocr_aligned[i] == "@") and (ocr_aligned[i+1] == gs_aligned[i+1]): # insert before
              key = (gs_aligned[i:i+2]) + "|" + (ocr_aligned[i+1])
              edit_patterns[key] = edit_patterns.get(key, 0) + 1

            if (gs_aligned[i] in alphabet_allCase) and (gs_aligned[i+1] in alphabet_allCase) \
            and (ocr_aligned[i+1] == "@") and (ocr_aligned[i] == gs_aligned[i]): # insert after
              key = (gs_aligned[i:i+2]) + "|" + (ocr_aligned[i])
              edit_patterns[key] = edit_patterns.get(key, 0) + 1

            if (ocr_aligned[i] in alphabet_allCase) and (ocr_aligned[i+1] in alphabet_allCase) \
            and (gs_aligned[i] == "@") and (gs_aligned[i+1] == ocr_aligned[i+1]): # delete before
              key = (gs_aligned[i+1]) + "|" + (ocr_aligned[i:i+2])
              edit_patterns[key] = edit_patterns.get(key, 0) + 1

            if (ocr_aligned[i] in alphabet_allCase) and (ocr_aligned[i+1] in alphabet_allCase) \
            and (gs_aligned[i+1] == "@") and (gs_aligned[i] == ocr_aligned[i]): # delete after
              key = (gs_aligned[i]) + "|" + (ocr_aligned[i:i+2])
              edit_patterns[key] = edit_patterns.get(key, 0) + 1
                           
  return edit_patterns
      
def write_edit_patterns_to_file(edit_patterns):
  """ Write edit patterns into file """  
  output_file = open("edit_patterns.txt", "w", encoding='utf-8')

  for edit_pattern in sorted(edit_patterns.items(), key=operator.itemgetter(1), reverse=True): # or key=lambda x: x[1] 
    output_file.write(edit_pattern[0] + "|" + str(edit_pattern[1]) + "\n")
  output_file.close()
  
def build_char_edit_tabs(train_fp='train_output_gt_sentences_v2_aligned.txt', \
                         val_fp = 'val_output_gt_sentences_v2_aligned.txt'):
  """ Build the character edit tables from training data """
  print("Build character edit patterns: Start...")
  # Variable to contain the error-correction pattern pairs
  edit_patterns = {}
    
  # Generate the edit patterns using training/validation datasets
  edit_patterns = find_edit_patterns(train_fp, edit_patterns) # construct edit patterns from train set
  edit_patterns = find_edit_patterns(val_fp, edit_patterns) # construct edit patterns from val set
  write_edit_patterns_to_file(edit_patterns)
  
  print("Build character edit patterns: Done!")  
  return edit_patterns  

if __name__ == "__main__":
  # Build the character edit tables
  edit_patterns = build_char_edit_tabs()
