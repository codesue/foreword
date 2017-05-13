# author: Sue Fylke
# about: Quickie script update master wordlists

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
	
# Add unlisted words to wordlist
def add_unlisted_words(from_wordlist, to_wordlist):
	"""Adds words to list if word not already listed"""
	for word in from_wordlist:
		if word not in to_wordlist:
			to_wordlist.append(word)
	to_wordlist.sort()
	
# Save wordlist to file
def save_wordlist(wordlist, filename):
	"""Saves a list of words to a text file."""
	text_file = open(filename, "w", encoding="utf-8")
	for word in wordlist:
		text_file.write(word + "\n")	
	text_file.close()
	
def update_wordlist(new_wordlist_filename, master_wordlist_filename, updated_wordlist_filename):
	new_wordlist = read_wordlist(new_wordlist_filename)
	master_wordlist = read_wordlist(master_wordlist_filename)
	add_unlisted_words(new_wordlist, master_wordlist)
	save_wordlist(master_wordlist, updated_wordlist_filename)

update_wordlist("known.txt", "known_master.txt", "known_master.txt")	
update_wordlist("unknown.txt", "unknown_master.txt", "unknown_master.txt")
