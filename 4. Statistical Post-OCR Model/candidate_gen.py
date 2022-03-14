# -*- coding: utf-8 -*-
"""
@author: NQDUNG @ VLU
"""
from helpers import Pedit_efp, efp_multi_edits
from candidate_score import f_weights, total_score_efp_improved

class Individual:
    """Individual of the population. It holds parameters of the solution as well as the score of the solution."""
    def __init__(self, candidate, score):
        self.candidate = candidate
        self.score = score

    def __repr__(self):
        return '{} score: {}'.format(self.candidate, self.score)
  
class Population:
    """Population of individuals. It holds common info among individuals
    """
    def __init__(self, e, ct_words):
        """
        e: erroneous word
        cands: candidates of the erroneous word e
        cands_edits: dict of candidates and corresponding edits
        ct_words: context words of the erroneous word e
        """
        self.e = e
        self.ct_words = ct_words
        self.cands_edits = efp_multi_edits(e)
        self.cands = list(self.cands_edits.keys())
        # recored edit prob for each candidate for improving computational cost, see total_score_efp_improved()
        self.edit_probs = {c: self.compute_edit_prob(c) for c in self.cands}
        self.individuals = self.generate_first_pop()
        
    def generate_first_pop(self):
        """Generate population @ initialization"""
        return [Individual(c, self.evaluate_indvl(c)) for c in self.cands]
                  
    def compute_edit_prob(self, c):
        """Compute edit/substitution probability for a candidate"""
        return Pedit_efp(self.cands_edits[c])
      
    def evaluate_indvl(self, c, ws=f_weights):
        """Returns total score of the candidate individual"""
        return total_score_efp_improved(self.e, c, self.edit_probs, self.cands, \
                         self.ct_words[0], self.ct_words[1], self.ct_words[2], self.ct_words[3], ws)
    
    def get_top5(self):
        """Finds top 5 of the population by their score (the higher the better)."""
        sort_inds = sorted(self.individuals, key = lambda individual: individual.score, reverse=True)
        return {ind.candidate: ind.score for ind in sort_inds[:5]}
        
    def __repr__(self):
        return '{} population: {}'.format(self.e, self.individuals)

def hw_cand_generation(e, ct_words):
  population = Population(e, ct_words)
  return population.get_top5()
  