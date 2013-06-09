rephrase
========

Interactive Machine Translation: Paraphrasing Experiments 


## Active Ideas

### Using Search Graph

* store hypotheses from Moses text output in a local sqlite database
* find span in the graph that generated phrases user wants to paraphrase 
* find alternative phrases in the search graph that have similar coverage  
* use *forward* and *fscore* to merge these phrases into paraphrasing options 
* rank resulting options according to the scores of their constituent phrase scores 

### Monolingual Paraphrasing


## Project Structure

* __converter.py__ - converts textual representation of the search graph into an sqlite database
* __rephraser.py__ - produces paraphrasing options from an MT output sentence and an input string that contains user's selection for paraphrasing 