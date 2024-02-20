import spacy
import re
import pprint

# Load the English model
nlp = spacy.load("en_core_web_sm")

contents = []  # Sample data from the Hacker News API  
chunks = []
for content in contents:
  # Process the text
  doc = nlp(content)

  # Analyze syntax
  noun_phrases = [chunk.text for chunk in doc.noun_chunks]
  verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
  named_entities = [(entity.text, entity.label_) for entity in doc.ents]

  # Combine the arrays of strings into one string
  phrases = ' '.join(noun_phrases)
  phrases = re.sub(r'[()[\]{}<>/!@#$%^&*]', '', phrases)
  verbs = ' '.join(verbs)
  entities = ' '.join(entity[0] for entity in named_entities)

  chunk_dict = {
    'noun_phrases': phrases,
    'verbs': verbs,
    'named_entities': entities
  }
  chunks.append(chunk_dict)

pprint.pprint(chunks)