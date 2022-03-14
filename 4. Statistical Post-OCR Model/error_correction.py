# -*- coding: utf-8 -*-
"""
@author: NQDUNG @ VLU
"""
import os, json
from error_detection import find_context_text, context_words, target_test_file
from candidate_gen import hw_cand_generation

def find_top5_candidates(ocr_output, word_begin_index, word_end_index):
  """ Find top-5 scored candidates """
  token, context_text = find_context_text(ocr_output, word_begin_index, word_end_index)
  token = ' '.join(token.split('|'))
  context_text = ' '.join(context_text.split('|'))
  
  if len(token.split()) == 1:
    ahead_2w, ahead_1w, behind_1w, behind_2w = context_words(token, context_text)
    return token, [ahead_2w, ahead_1w, behind_1w, behind_2w], hw_cand_generation(token, [ahead_2w, ahead_1w, behind_1w, behind_2w])
  elif len(token.split()) > 1:
    ahead_2w, ahead_1w, behind_1w, behind_2w = context_words(token, context_text)
    return token, ['', ahead_1w, behind_1w, ''], hw_cand_generation(token, ['', ahead_1w, behind_1w, ''])
  else:
    print("This should not happen. Token", token, "contains at least one syllable!")
    return token, ['', '', '', ''], {token: 1.}

work_directory_path = os.getcwd()

erroneous_tokens_pos_file = open(work_directory_path + "/Results/result_vn_words.json")
erroneous_tokens_pos = json.load(erroneous_tokens_pos_file) # a dict with keys as file names
erroneous_tokens_pos_file.close()

def move_begin_index_ahead(error_begin_index, reversed_ocr_output):
  """ move error_begin_index one syllable ahead """
  for k, c in enumerate(reversed_ocr_output):
    if c == '|': # second '|' looking backward from the end of line
      break
  if k == len(reversed_ocr_output) - 1: # not finding out '|'
    return 0 # begin index becomes start of line
  else:
    return (error_begin_index - 1) - k # begin_index of previous syllable
  
def error_correction(filepath):
  """ Error correction phase """
  print("Error correction: Start...")
  output_file = open(work_directory_path + "/Results/corrected_vn_words.json", "w", encoding='utf-8')
  output_file.write("{")
  corrected_output_gt_file = open(work_directory_path + "/Results/test_output_gt_sentences_v2_corrected.txt", "w", encoding='utf-8')
  
  f_sentence = open(filepath, encoding='utf-8').readlines()
  for i in range(len(f_sentence)):
    if f_sentence[i].find('result_VNOnDB_line_offline') != -1:
      file = f_sentence[i].split("\"")[1] # file is also a key in the dict erroneous_tokens_pos {}
      output_file.write("\n"+file+" ")
      #print(file) ###
      ocr_output = f_sentence[i+1].strip()
      corrected_ocr_output = ocr_output.split('|')
      errors_to_output = {}
      
      for error in erroneous_tokens_pos[file]: # iterate over key as {error pos:no. of tokens} in dict (value as empty dict)
        results = {}
        
        number_of_tokens = int(error[error.find(":")+1:]) # no. of tokens
        if number_of_tokens != 1:
          error_begin_index = int(error[:error.find(":")]) # error pos

          error_end_index = error_begin_index
          for j in range(number_of_tokens):
            error_end_index = ocr_output.find("|", error_end_index + 1)
            if error_end_index == -1: break
        else:
          error_begin_index = int(error[:error.find(":")])
          error_end_index = ocr_output.find("|", error_begin_index)
        
        # improve context error which is placed at the end of line.
        # move error_begin_index one syllable ahead to create meaningful bigram
        if error_end_index == -1 and number_of_tokens > 1:
          if ocr_output[error_begin_index:] == ocr_output.split('|')[-1]: # check if it is the last syllable
            reversed_ocr_output = ''.join(reversed(ocr_output[:error_begin_index-1])) # not involve last '|' since (error_begin_index-1) is the index of last '|'
            error_begin_index = move_begin_index_ahead(error_begin_index, reversed_ocr_output) # move begin_index one syllable ahead
            
        # improve context error whose syllable is ended by '.,)'.
        # move error_begin_index one syllable ahead to create meaningful bigram
        if error_end_index != -1 and number_of_tokens > 1:
          current_token = ocr_output[error_begin_index:error_end_index]
          if current_token.split('|')[0][-1] in '.,)': # check last character of error syllable
            error_end_index -= (len(current_token.split('|')[1]) + 1) # move end_index one syllable ahead
            reversed_ocr_output = ''.join(reversed(ocr_output[:error_begin_index-1])) # not involve last '|' since (error_begin_index-1) is the index of last '|'
            error_begin_index = move_begin_index_ahead(error_begin_index, reversed_ocr_output) # move begin_index one syllable ahead                      
         
        # process the correction
        token, contexts, results = find_top5_candidates(ocr_output, error_begin_index, error_end_index) 
        if not results:
          print('The results should not be empty. Maybe no candidate is suggested!') ###
          results = {token: 1.}
        errors_to_output[error + " " + token + " " + str(contexts)] = results
        
        # find the error syllable location with syllable count#
        syllable_count = 0
        for c in ocr_output[:error_begin_index]:
          if c == '|': syllable_count += 1
        
        # replace corrected token into corrected ocr output
        highest_ranked_cor_token = (list(results.keys())[0]).split()
        corrected_ocr_output = corrected_ocr_output[:syllable_count] + highest_ranked_cor_token + \
                               corrected_ocr_output[syllable_count+len(token.split()):]
        
      # UTF-8 is as default for json.dumps
      output_file.write(json.dumps(errors_to_output, indent=8, ensure_ascii=False)+",")
    
      # write corrected output and gt sentences for evaluation later
      corrected_ocr_output = '|'.join(corrected_ocr_output)
      corrected_output_gt_file.write(f_sentence[i]) # including '\n' at the end
      corrected_output_gt_file.write(corrected_ocr_output)
      corrected_output_gt_file.write('\n')
      corrected_output_gt_file.write(f_sentence[i+2]) # including '\n' at the end

  output_file.seek(0, 2) # uses the end of the file as the reference point
  output_file.truncate(output_file.tell() - 1) # remove last commas mark ','

  output_file = open(work_directory_path + "/Results/corrected_vn_words.json", "a") # appending
  output_file.write("\n}")
  output_file.close()
  
  corrected_output_gt_file.close()
  
  print("Error correction: Done!")
  
if __name__ == "__main__":
  # do error correction
  error_correction(target_test_file)
