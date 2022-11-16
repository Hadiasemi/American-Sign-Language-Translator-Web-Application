import math
import itertools
import nltk

nltk.download("punkt", quiet=True) #The Tokenizer

# classifications = [{'a':0.7, 'b':0.1, 'c':0.05, ...}, ...]
def stitch(classificatons):
	classifications = [c.items() for c in classifications]
	possible_strings = list(itertools.product(*classifications))
	possible_strings = [list(zip(*p)) for p in possible_strings]
	possible_strings = [(''.join(letters), sum(map(math.log, probs))) for letters, probs in possible_strings]
	# probability bonus: + between 0.1 and 0.5 for dictionary words based on frequency, + 0.2 for good grammar
	for i, (text, logprob) in enumerate(possible_strings):
		sents = nltk.sent_tokenize(text)
