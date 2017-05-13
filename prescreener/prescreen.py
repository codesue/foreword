#
# author: Sue Fylke
# file: prescreen.py
# date: 12 May 2017
# about: module for prescreener web app
# usage: strictly a module, do not run
#

import os
import os.path
import re
import pyphen
from nltk.stem import SnowballStemmer
from nltk.tokenize import RegexpTokenizer as rt
from nltk.corpus import stopwords
from nltk import FreqDist
import xml.etree.ElementTree as ET

# Tool Settings
tokenizer = rt(r'\w+')
stemmer = SnowballStemmer("swedish")
hyphenator = pyphen.Pyphen(lang="sv")
stops = stopwords.words("swedish")

# Known Words File
master_known_words_filename = os.path.join(os.getcwd(), "prescreener", "known_master_updated.txt")
	
# FUNCTIONS	
# Create wordlist from file (cleans data)
def create_wordlist(text):
	"""Creates a list of words from a text file"""
	wordlist = tokenizer.tokenize(text)
	wordlist = [word.lower() for word in wordlist]
	return wordlist

	
# Read wordlist from file (data already clean)
def read_wordlist(filename):
	"""Reads wordlist from file and returns wordlist as a list"""
	wordlist_file = open(filename, "rU", encoding="utf-8")
	wordlist = wordlist_file.read()
	wordlist_file.close()
	wordlist = tokenizer.tokenize(wordlist)
	return wordlist

	
# Remove numeric "words" from a wordlist
def remove_numbers(wordlist):
	"""Returns copy of wordlist with numeric strings removed"""
	no_numbers = []
	for word in wordlist:
		if not word.isnumeric():
			no_numbers.append(word)
	return no_numbers

	
# Make words in wordlist unique
def make_unique(wordlist):
	"""Returns a copy of wordlist with each distinct word listed only once"""
	unique_words = []
	for word in wordlist:
		if word not in unique_words:
			unique_words.append(word)
	return unique_words	
	

# Remove stopwords
def remove_stopwords(wordlist, stops):
	"""Returns copy of wordlist with stopwords removed"""
	no_stops = []
	for word in wordlist:
		if word not in stops:
			no_stops.append(word)
	return no_stops

	
# Remove known words from wordlist (shared words)
def remove_known_words(wordlist, known_words):
	"""Returns copy of wordlist with only those words that aren't in list of known words"""
	filtered_list = []
	for word in wordlist:
		if word not in known_words:
			filtered_list.append(word)
	return filtered_list
	
# Find likely context words, pref. of tokenized text with no stopwords
def context_words(tokenized_text, number):
	"""Returns list of the likely context words in a text based on frequency"""
	context_words = []
	fdist = FreqDist(tokenized_text)
	context_word_pairs = fdist.most_common(number)
	for pair in context_word_pairs:
		context_words.append(pair[0])
	return context_words
	
	
# Define words
def define(undefined_words, defined_words):
	tree = ET.parse("folkets_sv_en_public.xml")
	root = tree.getroot()
	vocabulary = []
	for child in root:
		for word in undefined_words:
			if word == child.get("value"):
				word_entry = {}
				word_entry["word"] = child.get("value")
				if child.get("class") != None:
					word_entry["pos"] = child.get("class")
				definitions = ""
				definitions_list = []
				for definition in child.findall("definition"):
					if child.findall("definition") != None:
						if child.findall("definition") == 1:
							definitions = definition.get("value")
						else:
							definitions_list.append(definition.get("value"))
				if len(definitions_list) > 0:			
					definitions = ", ".join(definitions_list)
				if definitions != "":
					word_entry["definitions"] = definitions
				translations = ""
				translations_list = []
				for translation in child.findall("translation"):
					if child.findall("translation") != None:
						if child.findall("translation") == 1:	
							translations = translation.get("value")
						else:
							translations_list.append(translation.get("value"))
				if len(translations_list) > 0:
					translations = ", ".join(translations_list)
				if translations != "":
					word_entry["translations"] = translations	
				if child.find("phonetic") != None:
					phonetic = child.find("phonetic")
					word_entry["pronunciation"] = phonetic.get("value")
				vocabulary.append(word_entry)
				defined_words.append(word)
				undefined_words.remove(word)
	return vocabulary


# Define words by stem				
def define_by_stem(undefined_words, defined_words):
	"""Stems words then define them"""
	tree = ET.parse("folkets_sv_en_public.xml")
	root = tree.getroot()
	vocabulary = []
	for child in root:
		for word in undefined_words:
			# save original word, rename stemmed word for ease and consistency
			original_word = word
			word = stemmer.stem(word)
			if word == child.get("value"):
				word_entry = {}
				word_entry["word"] = child.get("value")  + " (" + original_word + ")"
				if child.get("class") != None:
					word_entry["pos"] = child.get("class")
				definitions = ""
				definitions_list = []
				for definition in child.findall("definition"):
					if child.findall("definition") != None:
						if child.findall("definition") == 1:
							definitions = definition.get("value")
						else:
							definitions_list.append(definition.get("value"))
				if len(definitions_list) > 0:			
					definitions = ", ".join(definitions_list)
				if definitions != "":
					word_entry["definitions"] = definitions
				translations = ""
				translations_list = []
				for translation in child.findall("translation"):
					if child.findall("translation") != None:
						if child.findall("translation") == 1:	
							translations = translation.get("value")
						else:
							translations_list.append(translation.get("value"))
				if len(translations_list) > 0:
					translations = ", ".join(translations_list)
				if translations != "":
					word_entry["translations"] = translations	
				if child.find("phonetic") != None:
					phonetic = child.find("phonetic")
					word_entry["pronunciation"] = phonetic.get("value")
				vocabulary.append(word_entry)
				defined_words.append(original_word)
				undefined_words.remove(original_word)
	return vocabulary	
		
# Define words by parts		
def define_by_parts(undefined_words):
	"""Decompose words then defines them piecemeal"""
	tree = ET.parse("folkets_sv_en_public.xml")
	root = tree.getroot()
	vocabulary = []
	hyphens = {}
	for child in root:
		for word in undefined_words:
			# save original word
			original_word = word
			hyphens.setdefault(word, [])
			if len(hyphens.keys()) != 0:
				for key in hyphens.keys():
					for pair in hyphenator.iterate(key):
						for item in pair:
								# rename hyphen for ease and consistency
								word = item
								if word == child.get("value"):
									word_entry = {}
									word_entry["word"] = child.get("value")  + " (" + original_word + ")"
									if child.get("class") != None:
										word_entry["pos"] = child.get("class")
									definitions = ""
									definitions_list = []
									for definition in child.findall("definition"):
										if child.findall("definition") != None:
											if child.findall("definition") == 1:
												definitions = definition.get("value")
											else:
												definitions_list.append(definition.get("value"))
									if len(definitions_list) > 0:			
										definitions = ", ".join(definitions_list)											
									if definitions != "":
										word_entry["definitions"] = definitions
									translations = ""	
									translations_list = []
									for translation in child.findall("translation"):
										if child.findall("translation") != None:
											if child.findall("translation") == 1:	
												translations = translation.get("value")
											else:
												translations_list.append(translation.get("value"))
									if len(translations_list) > 0:
										translations = ", ".join(translations_list)
									if translations != "":
										word_entry["translations"] = translations	
									if child.find("phonetic") != None:
										phonetic = child.find("phonetic")
										word_entry["pronunciation"] = phonetic.get("value")
									vocabulary.append(word_entry)
									undefined_words.remove(original_word)
		return vocabulary	
	
# Read master list of known words
master_known_words = read_wordlist(master_known_words_filename)
	
