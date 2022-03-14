# -*- coding: utf-8 -*-
"""
@author: NQDUNG @ VLU
"""
from helpers import prepareData

# Sentence pairs are taken from AED train dataset
_, _, pairs = prepareData('ocr', 'gt', False, 'aed')
# Input and target vocabularies are built based on the OCR texts and GT texts respectively
# and enriched with VietTreeBank dictionary
input_lang, output_lang, _ = prepareData('ocr', 'gt', False, 'vtb_aed')

print(len(pairs))
print(input_lang.n_words, len(input_lang.word2index), len(input_lang.index2word))
print(output_lang.n_words, len(output_lang.word2index), len(output_lang.index2word))