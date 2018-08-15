from flask import Flask, request, render_template, redirect, url_for, Markup
from newspaper import Article
from xml.etree  import ElementTree
from copy import deepcopy
from nltk.corpus import stopwords
from nltk import FreqDist
from prescreener.prescreen import *
from math import ceil

# Global Variables (Yes, yes, I know.)
article = ""
article_link = ""
html_string = ""
filtered_article_words = []
article_words = []
known_words = []
unknown_words = []
		
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')
	
@app.route('/sort-words/')
def sort_words():
	global article
	global html_string
	global article_link
	global article_words
	global filtered_article_words
	global unknown_words
	
	# Get article URL from user input
	url_to_clean = request.args.get('url_to_clean')
	if not url_to_clean:
		return redirect(url_for('index'))

	# Download and parse article
	article = Article(url_to_clean)
	article.download()
	article.parse()
	
	html_string = ElementTree.tostring(article.clean_top_node)

	article.nlp()
	
	article_link = url_to_clean
	
	article_text = article.text
	
	# Make article wordlist and remove known words
	article_words = create_wordlist(article_text)
	article_words = remove_numbers(article_words)
	unique_article_words = make_unique(article_words)
	# Remove shared words (order important!)
	#  1. Remove known words
	filtered_article_words = remove_shared_words(unique_article_words, master_known_words)
	#  2. Record unknown words
	unknown_words = get_shared_words(filtered_article_words, master_unknown_words)
	#  3. Remove unknown words
	filtered_article_words = remove_shared_words(filtered_article_words, master_unknown_words)
	
	checkboxes_per_column = ceil(len(filtered_article_words) / 4)
	
	return render_template('sort-words/index.html', filtered_article_words=filtered_article_words, checkboxes_per_column=checkboxes_per_column)

	
@app.route('/prescreened-article/show')
def show_article():
	global known_words
	global unknown_words
	global article
	global article_words
	global article_link
	global html_string	
	
	undefined_words = []
	defined_words = []

	# Get known words from user input
	known_words = request.args.getlist("word")
	
	# Filter out new known words
	new_filtered_article_words = remove_shared_words(filtered_article_words, known_words)
	# Record unknown words not in master unknown words
	#  Deep copy for debugging and changing program later
	new_unknown_words = deepcopy(new_filtered_article_words)
	# Update unknown words 
	for word in new_filtered_article_words:
		unknown_words.append(word)
	# Want to define all unknown words, not just new ones
	#  Deep copy for debugging and changing program later	
	undefined_words = deepcopy(unknown_words)
	
	# Define words
	definitions = define(undefined_words, defined_words)
	definitions_stem = define_by_stem(undefined_words, defined_words)
	
	# Find likely Context Words
	stopless_article_words = remove_stopwords(article_words, stops)
	article_context_words = context_words(stopless_article_words, 10)
	article_context_words_str = ", ".join(article_context_words)
	
	# Memrise friendly vocabulary list
	#  Entry must be complete
	#  Must be ordered as word, definition, translation, pos, pronunciation
	#  Each field must be seperated by tab
	#  Each word must have its own line
	vocabulary = []
	for word in definitions:
		if len(word) == 5:
			vocabulary_entry = []
			vocabulary_entry.append(word.get("word"))
			vocabulary_entry.append(word.get("definitions"))
			vocabulary_entry.append(word.get("translations"))
			vocabulary_entry.append(word.get("pos"))
			vocabulary_entry.append(word.get("pronunciation"))
			vocabulary_entry_str = "\t".join(vocabulary_entry)
			vocabulary.append(vocabulary_entry_str)

	a = {
		 "url": article_link,	
		 "title": article.title,
		 "text": str("<br />".join(article.text.splitlines())),
		 "top_image": article.top_image,
		 "keywords": article_context_words_str,
		 "synopsis": article.summary,
		 "definitions": definitions,
		 "definitions_stem": definitions_stem, 
		 "undefined_words": undefined_words,
		 "vocabulary": vocabulary,
		 "known_words": known_words,
		 "new_unknown_words": new_unknown_words
		 }
		 
	return render_template('article/index.html', article=a)
	
@app.errorhandler(404)
def page_not_found(e):
	return render_template("/error-pages/404.html")

if __name__ == "__main__":
	#app.debug = True
	app.run()
