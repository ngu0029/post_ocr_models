# -*- coding: utf-8 -*-
"""
@author: NQDUNG @ VLU

Note: Many modifications have been made based on the original code published by Pytorch @
https://pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html
"""
import re, torch
from helpers import MAX_LENGTH, SOS_token
from biLSTM_NMT_model import tensorFromSentence, encoder1, attn_decoder1
from build_trainData_and_Vocab import input_lang, output_lang

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def evaluate(encoder, decoder, sentence, max_length=MAX_LENGTH):
    with torch.no_grad():
        input_tensor = tensorFromSentence(input_lang, sentence)
        input_length = input_tensor.size()[0]
        encoder_hidden = encoder.initHidden()

        encoder_outputs = torch.zeros(max_length, encoder.hidden_size * 2, device=device)

        for ei in range(input_length):
            encoder_output, encoder_hidden = encoder(input_tensor[ei],
                                                     encoder_hidden)
            encoder_outputs[ei] += encoder_output[0, 0]

        decoder_input = torch.tensor([[SOS_token]], device=device)
        decoder_hidden = encoder_hidden

        decoded_words = []
        decoder_attentions = torch.zeros(max_length, max_length)

        for di in range(input_length - 1):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs)
            decoder_attentions[di] = decoder_attention.data
            topv, topi = decoder_output.data.topk(1)
            
            word_in_both_input_and_target = sentence.split('|')[di]
            if word_in_both_input_and_target in output_lang.word2index:
                decoded_words.append(word_in_both_input_and_target)
            else:
                decoded_words.append(output_lang.index2word[topi.item()])                

            if di < input_length:
                word_in_both_input_and_target = input_lang.index2word[input_tensor[di].item()] # current syllable
                if word_in_both_input_and_target in output_lang.word2index:
                    decoder_input = torch.tensor([[output_lang.word2index[word_in_both_input_and_target]]], device=device)
                else:
                    decoder_input = topi.squeeze().detach()        
            else:
                decoder_input = topi.squeeze().detach()
            
        return decoded_words, decoder_attentions[:di + 1]

def split_sentences(txt):
  sentences = []
  res = re.search(r'[^A-Z]\|[.,!?:;]\|[^0-9.,]', txt)
  while res:
    sentences.append(txt[: res.start()+3])
    txt = txt[res.start()+4:]
    res = re.search(r'[^A-Z]\|[.,!?:;]\|[^0-9.,]', txt)
  if (not sentences) or (not res):
    sentences.append(txt)
  return sentences

def ocr_correction(encoder, decoder, line):
  sentences = split_sentences(line)
  corrected_line = ''
  for i in range(len(sentences)):
      output_words, attentions = evaluate(
          encoder, decoder, sentences[i])
      if i == 0:
          corrected_line = '|'.join(output_words)
      else:
          corrected_line += '|' + '|'.join(output_words)
  return corrected_line
    
encoder1.eval()
attn_decoder1.eval()
