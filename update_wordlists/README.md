# Update Wordlists
This directory is a space to update wordlists for use with the Foreword web app without overwriting the files in use by the main program. 

## update_wordlists.py
- adds the words in known.txt to known_master.txt
- adds the words in unknown.txt to unknown_master.txt
- Usage: run <code>python update_wordlists.py</code>

## reconcile_learned_words.py
- removes words in unknown_master.txt that are in master.txt
- Usage: run <code>python reconcile_learned_words.py</code>

## Save Foreword session
After you prescreen an article using the Foreword web app, copy your new known words from the summary section and paste them to known.txt, your new unknown words to unknown.txt, and your vocabulary words to memrise.txt. 

To bulk add vocabulary words to Memrise, just copy them, paste them to your Memrise bulk add form, and choose "Tab" as your word delimiter. Your course fields must be organized as [ Swedish word, Swedish definition, English translation, part of speech, pronunciation ].
