# author: Sue Fylke
# about: Quickie script to reconcile master wordlists for learned words

from nltk.tokenize import RegexpTokenizer as rt
tokenizer = rt(r'\w+')

# Read wordlist from file
def read_wordlist(filename):
	"""Reads wordlist from file and returns wordlist as a list"""
	wordlist_file = open(filename, "rU", encoding="utf-8")
	wordlist = wordlist_file.read()
	wordlist_file.close()
	wordlist = tokenizer.tokenize(wordlist)
	return wordlist
	
# Remove shared from wordlist
def remove_shared_words(operand_wordlist, reference_wordlist):
	"""Returns copy of wordlist with only those words that aren't in list of known words"""
	filtered_list = []
	for word in operand_wordlist:
		if word not in reference_wordlist:
			filtered_list.append(word)
	return filtered_list	
	
# Save wordlist to file
def save_wordlist(wordlist, filename):
	"""Saves a list of words to a text file."""
	text_file = open(filename, "w", encoding="utf-8")
	for word in wordlist:
		text_file.write(word + "\n")	
	text_file.close()
	
def reconcile_learned_words(master_known_filename, master_unknown_filename, updated_master_unknown_filename):
	known_words = read_wordlist(master_known_filename)
	unknown_words = read_wordlist(master_unknown_filename)
	updated_unknown_words = remove_shared_words(unknown_words, known_words)
	save_wordlist(updated_unknown_words, updated_master_unknown_filename)

reconcile_learned_words("known_master.txt", "unknown_master.txt", "unknown_master.txt")	
