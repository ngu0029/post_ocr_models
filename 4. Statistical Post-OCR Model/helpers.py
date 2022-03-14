# -*- coding: utf-8 -*-
"""
@author: NQDUNG @ VLU
"""
from build_ngrams import build_unigrams, build_ngrams
from functools import reduce
import collections, operator

# build unigram vocabulary. 
COUNTS1 = build_unigrams()
# build bigram and trigram dictionaries. 
COUNTS2, COUNTS3 = build_ngrams()

def load_err_patterns(filename, sep='|'):
    """Return a Counter initialized from key-value pairs, 
    one on each line of filename."""
    C, C1 = collections.Counter(), collections.Counter()
    for line in open(filename, encoding='utf-8'):
        gs, ocr, count = line.split(sep)
        C[ocr+'|'+gs] = int(count)
        C1[ocr] = C1.get(ocr, []) + [gs]
    return C, C1
  
err_gs_patterns, err_patterns = load_err_patterns('edit_patterns.txt') # case-sensitive

def levenshtein(s1, s2):
  """
    Compute Levenshtein's edit distance between s1 and s2
    under Copyright 2015, James TurkJames Turk, Sunlight Foundation
    with LICENSE BSD 2: https://github.com/jamesturk/jellyfish/blob/master/LICENSE
  """
  if s1==s2:
      return 0

  len1 = len(s1)
  len2 = len(s2)
  infinite = len1 + len2

  # character array
  da = collections.defaultdict(int)

  # distance matrix
  score = [[0] * (len2 + 2) for x in range(len1 + 2)]

  score[0][0] = infinite
  for i in range(0, len1 + 1):
      score[i + 1][0] = infinite
      score[i + 1][1] = i
  for i in range(0, len2 + 1):
      score[0][i + 1] = infinite
      score[1][i + 1] = i

  for i in range(1, len1 + 1):
      db = 0
      for j in range(1, len2 + 1):
          i1 = da[s2[j - 1]]
          j1 = db
          cost = 1
          if s1[i - 1] == s2[j - 1]:
              cost = 0
              db = j

          score[i + 1][j + 1] = min(score[i][j] + cost,
                                    score[i + 1][j] + 1,
                                    score[i][j + 1] + 1,
                                    score[i1][j1] + (i - i1 - 1) + 1 + (j - j1 - 1))
      da[s1[i - 1]] = i

  return score[len1 + 1][len2 + 1]

def lcs(a, b):
  """
    Compute longest common distance between a and b
    Reference: http://rosettacode.org/wiki/Longest_common_subsequence#Python
  """  
  lengths = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
  # row 0 and column 0 are initialized to 0 already
  for i, x in enumerate(a):
      for j, y in enumerate(b):
          if x == y:
              lengths[i+1][j+1] = lengths[i][j] + 1
          else:
              lengths[i+1][j+1] = max(lengths[i+1][j], lengths[i][j+1])
  # read the substring out from the matrix
  result = ""
  x, y = len(a), len(b)
  while x != 0 and y != 0:
      if lengths[x][y] == lengths[x-1][y]:
          x -= 1
      elif lengths[x][y] == lengths[x][y-1]:
          y -= 1
      else:
          assert a[x-1] == b[y-1]
          result = a[x-1] + result
          x -= 1
          y -= 1
  return result
  
def MCLCS1(r, s):
  """
    Compute Maximal Consecutive LCS starting at character 1
  """
  if len(r) > len(s):
    r, s = s, r
  n = len(r)
  while n > 0:
    if r[:n] == s[:n]:
      return r[:n]
    else:
      n -= 1
  return ""

def all_ngrams(s):
  if len(s) == 0: return [""]
  if len(s) == 1: return [s]
  res = []
  for i in range(len(s)):
    j = i + 1
    while j <= len(s):
       res.append(s[i:j])
       j += 1
  return res

def MCLCSany(r, s):
  """
    Compute Maximal consecutive LCS starting at any character n
  """
  if len(r) > len(s):
    r, s = s, r
  ngrams = all_ngrams(r)
  ngrams = sorted(ngrams, key=lambda g: len(g), reverse=True)
  for ngram in ngrams:
    if s.find(ngram) != -1:
      return ngram
  return ""

def MCLCSz(r, s):
  """
    Compute Maximal consecutive LCS ending at the last character
  """
  if len(r) > len(s):
    r, s = s, r
  n = 0
  while n < len(r):
    if r[n:] == s[len(s)-len(r)+n:]:
      return r[n:]
    else:
      n += 1
  return ""
       
def product(nums):
    "Return the product of a sequence of numbers."
    return reduce(operator.mul, nums, 1)

class Pdist(dict):
    "A probability distribution estimated from counts in datafile."
    def __init__(self, data=[], N=None, missingfn=None):
        for key,count in data:
            self[key] = self.get(key, 0) + int(count)
        self.N = float(N or sum(self.values()))
        self.missingfn = missingfn or (lambda k, N: 1./N)
    def __call__(self, key): 
        if key in self: return self[key]/self.N
        else: return self.missingfn(key, self.N)
        
def datafile_efp(filename, sep="|"):
  "Read key,value pairs from file."
  for line in open(filename, encoding='utf-8'):
      gs, ocr, count = line.split(sep)
      yield ocr+'|'+gs, count
      
Pdist_efp = Pdist(datafile_efp('edit_patterns.txt'))

def Pedit_efp(edits): # P(w | c) is computed by Pedit
    """
    Compute probability of P(w|c) including multiple edits.
    The argument edits can be '' or 'a|b' or 'a|b+c|d'.
    See def of product(nums): return reduce(operator.mul, nums, 1)
    """
    if edits == '': return 1.
    return product(Pdist_efp(e) for e in edits.split('+'))
  
def neighboring_patterns(s):
    """
      Return correction patterns
    """
    if s not in err_patterns: return []
    for p in err_patterns[s]:
      yield p
  
def efp_multi_edits(word, d=2): 
    "Return a dict of {correct: edit} pairs within d edits of word." 
    results = {}
    def editsR(hd, tl, d, edits):
        def ed(L,R): return edits+[L+'|'+R]
        C = hd+tl 
        if C in COUNTS1 or C in COUNTS2 or C in COUNTS3:
          e = '+'.join(edits) 
          if C not in results: results[C] = e 
          else: results[C] = max(results[C], e, key=Pedit_efp)               
        if d <= 0: return
        if not tl: return
        ## No replacement
        editsR(hd+tl[0], tl[1:], d, edits)
        ## Replacement
        if len(tl) == 1:
          for p in neighboring_patterns(tl):
            editsR(hd+p, '', d-1, ed(tl, p))
        elif len(tl) >= 2:
          for p in neighboring_patterns(tl[0]):
            editsR(hd+p, tl[1:], d-1, ed(tl[0], p))   
          for p in neighboring_patterns(tl[0:2]):
            editsR(hd+p, tl[2:], d-1, ed(tl[0:2], p))
          
    ## Body of edits: 
    editsR('', word, d, [])
    return results