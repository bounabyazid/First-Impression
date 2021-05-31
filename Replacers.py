'https://github.com/PacktPublishing/Natural-Language-Processing-Python-and-NLTK/blob/master/Module%202/Chapter%202/7853OS_02_codes/replacers.py'
import re
from nltk.corpus import wordnet

replacement_patterns = [
(r'won\'t', 'will not'),
(r'won\’t', 'will not'),
(r'won\´t', 'will not'),

(r'can\'t', 'can not'),
(r'can\’t', 'can not'),
(r'can\´t', 'can not'),

(r'doesn\'t', 'does not'),
(r'doesn\’t', 'does not'),
(r'doesn\´t', 'does not'),

(r'don\'t', 'do not'),
(r'don\’t', 'do not'),
(r'don\´t', 'do not'),

(r'didn\'t', 'did not'),
(r'didn\’t', 'did not'),
(r'didn\´t', 'did not'),

(r'i\'m', 'i am'),
(r'I\'m', 'I am'),

(r'ain\'t', 'is not'),
(r'ain\’t', 'is not'),
(r'ain\´t', 'is not'),

(r'(\w+)\'ll', '\g<1> will'),
(r'(\w+)\’ll', '\g<1> will'),
(r'(\w+)\´ll', '\g<1> will'),

(r'(\w+)n\'t', '\g<1> not'),
(r'(\w+)n\’t', '\g<1> not'),
(r'(\w+)n\´t', '\g<1> not'),

(r'(\w+)\'ve', '\g<1> have'),
(r'(\w+)\’ve', '\g<1> have'),
(r'(\w+)\´ve', '\g<1> have'),

(r'(\w+)\'s', '\g<1> is'),
(r'(\w+)\’s', '\g<1> is'),
(r'(\w+)\´s', '\g<1> is'),

(r'(\w+)\'re', '\g<1> are'),
(r'(\w+)\’re', '\g<1> are'),
(r'(\w+)\´re', '\g<1> are'),

(r'(\w+)\'d', '\g<1> would'),
(r'(\w+)\’d', '\g<1> would'),
(r'(\w+)\´d', '\g<1> would')]
class RegexpReplacer(object):
        def __init__(self, patterns=replacement_patterns):
                self.patterns = [(re.compile(regex), repl) for (regex, repl) in patterns]
        def replace(self, text):
            s = text
            for (pattern, repl) in self.patterns:
                s = re.sub(pattern, repl, s)
            return s
            
class Repeat_Letter_Replacer(object):
	""" Removes repeating characters until a valid word is found.
	>>> replacer = RepeatReplacer()
	>>> replacer.replace('looooove')
	'love'
	>>> replacer.replace('oooooh')
	'ooh'
	>>> replacer.replace('goose')
	'goose'
	"""
	def __init__(self):
		self.repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
		self.repl = r'\1\2\3'

	def replace(self, word):
		if wordnet.synsets(word):
			return word
		
		repl_word = self.repeat_regexp.sub(self.repl, word)
		
		if repl_word != word:
			return self.replace(repl_word)
		else:
			return repl_word
            
class Antonym_Replacer(object):
  def replace(self, word, pos=None):
    antonyms = set()
    for syn in wordnet.synsets(word, pos=pos):
      for lemma in syn.lemmas():
        for antonym in lemma.antonyms():
          antonyms.add(antonym.name())
    if len(antonyms) == 1:
       return antonyms.pop()
    else:
       return None

  def replace_negations(self, sent):
      i, l = 0, len(sent)
      words = []
      while i < l:
            word = sent[i]
            if word == 'not' and i+1 < l:
               ant = self.replace(sent[i+1])
               if ant:
                  words.append(ant)
                  i += 2
                  continue
            words.append(word)
            i += 1
      return words

#negative prefix
#_______________

#de dis in mis non un

#Negtive words
#_____________
    
#no not none no one nobody nothing nowhere never

#Negtive adverbs
#_______________

#Hardly scarcely barly
