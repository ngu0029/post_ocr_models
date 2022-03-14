# -*- coding: utf-8 -*-
"""
@author: NQDUNG @ VLU
"""
from helpers import lcs, MCLCS1, MCLCSany, MCLCSz, COUNTS1, COUNTS2, COUNTS3

def similarity(r, s):
  NLCS = 2*len(lcs(r, s))/(len(r) + len(s))
  NMCLCS1 = 2*len(MCLCS1(r, s))/(len(r) + len(s))
  NMCLCSany = 2*len(MCLCSany(r, s))/(len(r) + len(s))
  NMCLCSz = 2*len(MCLCSz(r, s))/(len(r) + len(s))
  return .25*NLCS + .25*NMCLCS1 + .25*NMCLCSany + .25*NMCLCSz

def similarity_score(e, c):
  """
    Return similarity score for each correction candidate. The higher score, the better candidate.
    e: erroneous token
    c: correction candidate
  """
  return similarity(e, c)

def syllable_frequency(c, cands):
  """
    Return the normalized frequency of the correction candidate c regarding all the correction candidates
  """
  dict_c = {c: COUNTS1[c] for c in cands}
  max_c = max(cands, key=lambda c: dict_c[c])
  return dict_c[c]/dict_c[max_c] if dict_c[max_c] else 0

def syllable_freq_score(c, cands):
  """
    Return syllable frequency score for each correction candidate. The higher score, the better candidate.
    c: correction candidate
    cands: list of correction candidates including c
  """
  return syllable_frequency(c, cands)

def bi_score(c, cands, ahead_w, behind_w):
  """
    Return the bigram score for each condidate in context
    c: candidate in check
    cands: correction candidates
    ahead_w, behind_w: words ahead and behind the erroneous word
  """
  def bi_counts(c, ahead_w, behind_w):
    if ahead_w or behind_w:
      return COUNTS2[ahead_w + ' ' + c] + \
             COUNTS2[c + ' ' + behind_w] + .001 # smoothing
    else:
      return COUNTS2[c] + .001

  dict_c = {c: bi_counts(c, ahead_w, behind_w) for c in cands}
  max_c =  max(cands, key=lambda c: dict_c[c])
  return dict_c[c] / dict_c[max_c] if dict_c[max_c] else 0

def tri_score(c, cands, ahead_2w, ahead_1w, behind_1w, behind_2w):
  """
    Return the bigram score for each condidate in context
    c: candidate in check
    cands: correction candidates
    ahead_w, behind_w: words ahead and behind the erroneous word
  """
  def tri_counts(c, ahead_2w, ahead_1w, behind_1w, behind_2w):
    if len(c.split()) == 2 and (ahead_1w or behind_1w):
      return COUNTS3[ahead_1w + ' ' + c] + \
             COUNTS3[c + ' ' + behind_1w] + .001 # smoothing
    
    if ahead_2w or ahead_1w or behind_1w or behind_2w:
      return COUNTS3[ahead_2w + ' ' + ahead_1w + ' ' + c] + \
             COUNTS3[ahead_1w + ' ' + c + ' ' + behind_1w] + \
             COUNTS3[c + ' ' + behind_1w + ' ' + behind_2w] + .001
    else:
      return COUNTS3[c] + .001

  dict_c = {c: tri_counts(c, ahead_2w, ahead_1w, behind_1w, behind_2w) for c in cands}
  max_c =  max(cands, key=lambda c: dict_c[c])
  return dict_c[c] / dict_c[max_c] if dict_c[max_c] else 0

def edit_score_efp_improved(c, dict_edit_probs):
  """
    Return edit score based on Error Freq Patterns
    c: a correction candidate
    dict_edit_probs: a dictionary of correction candidates and their edit probabilities
  """
  if not dict_edit_probs[c]: return 1.

  max_c = max(dict_edit_probs.keys(), key=dict_edit_probs.get)
  return dict_edit_probs[c] / dict_edit_probs[max_c] if dict_edit_probs[max_c] else 0

f_weights = (.25, .0, .25, .25, .25)

def total_score_efp_improved(e, c, edit_probs, cands, ahead_2w, ahead_1w, behind_1w, behind_2w, ws=f_weights):
  """
    Compute the EFP score
    ws: weights (heuristically chosen)
  """
  return ws[0]*similarity_score(e, c) + \
         ws[1]*0 + \
         ws[2]*bi_score(c, cands, ahead_1w, behind_1w) + \
         ws[3]*tri_score(c, cands, ahead_2w, ahead_1w, behind_1w, behind_2w) + \
         ws[4]*edit_score_efp_improved(c, edit_probs)