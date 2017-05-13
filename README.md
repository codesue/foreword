# foreword
A web app that makes reading Swedish more approachable and enjoyable. 

Required: <a href="http://flask.pocoo.org/">flask</a>, <a href="http://www.nltk.org/">nltk</a>, <a href="https://newspaper.readthedocs.io/en/latest/">newspaper</a>, <a href="http://pyphen.org/">pyphen</a>

Recommended: <a href="https://www.memrise.com/">Memrise account</a>

Usage:
- Replace words in known_master.txt with your own known words
- Replace words in unknown_master.txt with your own unknown words
- Run <code>python app.py</code>
- (optional but recommended) Save session summary by copy/pasting results to relevant files in /update_wordlists
- (optional but recommended) After every few runs, update known_master.txt and unknown_master.txt by running update_wordlists.py and reconcile_learned_words.py in /update_wordlists. Regularly updating files with update_wordlist.py will increases the automation of the sorting process.

Homepage:
<img src="https://github.com/codesue/foreword/blob/master/screenshots/foreword_index.png" alt="screenshot of Foreword homepage" />

Example results pages:
- Foreword Section
<img src="https://github.com/codesue/foreword/blob/master/screenshots/foreword_supernova_results_foreword.png" alt="screenshot of Foreword Foreword Section results" />


- Vocabulary Section
<img src="https://github.com/codesue/foreword/blob/master/screenshots/foreword_supernova_results_vocabulary.png" alt="screenshot of Foreword Vocabulary Section results" />

Website built with <a href="https://getbootstrap.com/">Bootstrap</a> and uses an image and content from the prescreened article. The example results pages are from a <a href ="http://fof.se/tidning/2017/4/artikel/sa-aldras-en-supernova">Forskning & Framsteg article on supernovas</a>.
