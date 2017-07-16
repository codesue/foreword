# foreword
A web app that makes reading Swedish more approachable and enjoyable. 

How it works:
1. You select an article for Foreword to prescreen.
2. Foreword automatically sorts the words in the article into lists of known words and unknown words based on the master lists of known words and unknown words you configure.
3. You'll be asked to choose the words you know from the words that could not be automatically sorted. 
4. Foreword parses the article and for keywords and a synopsis, defines the words you don't know, generates lists of your new known words and unknown words from the words you manually sorted, and presents your vocabulary words in a Memrise (bulk add) friendly format. 

Required: <a href="http://flask.pocoo.org/">flask</a>, <a href="http://www.nltk.org/">nltk</a>, <a href="https://newspaper.readthedocs.io/en/latest/">newspaper</a>, <a href="http://pyphen.org/">pyphen</a>

Recommended: <a href="https://www.memrise.com/">Memrise account</a>

Usage:
- Replace words in known_master.txt with your own known words
- Replace words in unknown_master.txt with your own unknown words
- Run <code>python app.py</code>
- (optional but recommended) Save session summary by copy/pasting results to relevant files in /update_wordlists
- (optional but recommended) After every few runs, update known_master.txt and unknown_master.txt by running update_wordlists.py and reconcile_learned_words.py in /update_wordlists. Regularly updating files with update_wordlist.py will increases the automation of the sorting process.

To learn and to do:
- [ ] Center contents on Sort Words page.
- [ ] Don't render template for Sort Words page if all words in the article are automatically are automatically sorted.
- [ ] Make it possible to define words based on possible compounds. (i.e. Fix hyphenator.)
- [ ] Use loader to make wait for results more pleasant. 

Homepage:
<img src="https://github.com/codesue/foreword/blob/master/screenshots/foreword_index.png" alt="screenshot of Foreword homepage" />

Example Sort Words Page:
<img src="https://github.com/codesue/foreword/blob/master/screenshots/foreword_supernova_sortwords.png" alt="screenshot of Foreword Sort Words supernova results" />

Example results pages:
- Foreword Section
<img src="https://github.com/codesue/foreword/blob/master/screenshots/foreword_supernova_results_foreword.png" alt="screenshot of Foreword Foreword Section supernova results" />


- Vocabulary Section
<img src="https://github.com/codesue/foreword/blob/master/screenshots/foreword_supernova_results_vocabulary.png" alt="screenshot of Foreword Vocabulary Section supernova results" />

Website built with <a href="https://getbootstrap.com/">Bootstrap</a> and uses an image and content from the prescreened article. The example results pages are from a <a href ="http://fof.se/tidning/2017/4/artikel/sa-aldras-en-supernova">Forskning & Framsteg article on supernovas</a>.
