import math
import itertools

import nltk
from wordfreq import word_frequency

nltk.download("punkt", quiet=True) #The Tokenizer

MAX_FREQ = word_frequency('the', 'en')
FREQ_WEIGHT = 0.2 # What is the maximum percent of the bonus given to the probability rating of a given parse based on it containing frequent words.
CLUMPINESS_CONSTANT = 1.15 # How much should the algorithm try to favor parses that have fewer letters.

# From itertools documentation
def powerset(iterable):
  "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
  s = list(iterable)
  return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))

# Use the power set to get all possible ways of partitioning a list into sublists
def partition(seq):
  possible = []
  ids = {id(obj):obj for obj in seq}
  for delimiters in powerset(ids.keys()):
    possible.append(''.join([str(number)+';.' if number in delimiters else str(number)+';' for number in ids.keys()]))
  new_possible = []
  for id_chain in possible:
    chunks = id_chain.split('.')
    chunks = [[ids[int(id)] for id in chunk.split(';') if len(id) != 0] for chunk in chunks]
    if chunks[-1] == []:
      continue
    new_possible.append(chunks)
  return new_possible

# classifications = [{'a':0.7, 'b':0.1, 'c':0.05, ..., 'z':0}, ...]
def chunk_letters(classifications):
  possible_chunkings = partition(classifications)
  merged_chunkings = []
  for chunking in possible_chunkings:
    merged_chunking = []
    for chunk in chunking:
      letters = chunk[0].keys()
      probabilities = {letter:-sum([math.log(1-probs[letter]) for probs in chunk]) for letter in letters}
      merged_chunking.append(probabilities)
    merged_chunkings.append(merged_chunking)
  max_prob = 0
  best_chunking = []
  for chunking in merged_chunkings:
    probability = [max(probs.values()) for probs in chunking]
    probability = sum([p**CLUMPINESS_CONSTANT for p in probability])
    if probability > max_prob:
      max_prob = probability
      best_chunking = chunking
  return best_chunking

def print_most_likely(chunking):
  for letter in chunking:
    print(max(letter, key=letter.get),)

def stitch(classifications):
  classifications = [c.items() for c in classifications]
  possible_strings = list(itertools.product(*classifications))
  possible_strings = [list(zip(*p)) for p in possible_strings]
  possible_strings = [(''.join(letters), sum(map(math.log, probs))) for letters, probs in possible_strings]
  max_freq_bonus = 1000000
  best = None
  for i, (text, logprob) in enumerate(possible_strings):
    sents = nltk.sent_tokenize(text)
    freqs = []
    for sent in sents:
      words = nltk.word_tokenize(sent)
      for word in words:
        freqs.append(word_frequency(word, 'en'))
    freq_bonus = math.log(sum(freqs) / (len(freqs)*MAX_FREQ))
    logprob = - logprob - (freq_bonus*FREQ_WEIGHT)
    if logprob < max_freq_bonus:
      max_freq_bonus = logprob
      best = text
  return best