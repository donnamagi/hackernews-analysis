import spacy
import voyageai
import re
from dotenv import load_dotenv
import os

load_dotenv()
VOYAGE_KEY = os.getenv("VOYAGE_API_KEY")

# some sample data
top_hn = [{'comment_count': 672,
  'comment_ids': [39305993,
                  39308595,
                  39305810,
                  39305639,
                  39305677,
                  39305651,
                  39309555,
                  39306049,
                  39308837,
                  39305565],
  'content': 
             'The Federal Communications Commission (FCC) has adopted a ruling '
             'that defines calls made with AI-generated voices as "artificial" '
             'under the Telephone Consumer Protection Act (TCPA). This means '
             "that such calls are subject to the act's restrictions on "
             'telemarketing and automated calls.',
  'hn_comment': '',
  'hn_id': 39304736,
  'title': 'FCC rules AI-generated voices in robocalls illegal',
  'url': 'https://www.fcc.gov/document/fcc-makes-ai-generated-voices-robocalls-illegal'},
 {'comment_count': 584,
  'comment_ids': [39322275,
                  39323462,
                  39325074,
                  39324479,
                  39323028,
                  39322378,
                  39323065],
  'content': 'The author has experience leading infrastructure at a technology '
             'startup for four years, during which they made some decisions '
             'regarding the use of cloud services (GCP and AWS). They provide '
             'recommendations for startups, endorsing the use of EKS for '
             'Kubernetes clusters and helm charts for managed add-ons, as well '
             'as offering regret for using EKS managed add-ons. The author '
             'emphasizes the importance of support and stability when choosing '
             'cloud services, with AWS providing better customer focus and '
             'stability, while Google Cloud has improved in recent years due '
             'to additional Kubernetes integrations.',
  'hn_comment': '',
  'hn_id': 39313623,
  'title': 'Almost every infrastructure decision I endorse or regret',
  'url': 'https://cep.dev/posts/every-infrastructure-decision-i-endorse-or-regret-after-4-years-running-infrastructure-at-a-startup/'},
 {'comment_count': 214,
  'comment_ids': [39301497,
                  39298688,
                  39306583,
                  39298598],
  'content': 'John Walker passed away on February 2, 2024, after being born to '
             'William and Bertha Walker in Maryland, USA. He is survived by '
             'his wife Roxie, a brother Bill from West Virginia, and numerous '
             'other relatives. John pursued a career in astronomy at Case '
             'Western Reserve University before switching to computer science '
             'and earning an electrical engineering degree. He worked at '
             'various companies in California before designing his own circuit '
             'board based on the Texas Instruments TMS9900 microprocessor, '
             'which led to the creation of Marinchip Systems and eventually '
             'Autodesk. John was a regular caller on audio meet-ups (AMUs) on '
             'Ricochet.com for over ten years and was known by many in the '
             "community. This announcement has been posted on behalf of John's "
             'family, with the Scanalyst web site serving as a tribute to his '
             'life and legacy.',
  'hn_comment': '',
  'hn_id': 39297185,
  'title': 'John Walker, founder of Autodesk, has died',
  'url': 'https://scanalyst.fourmilab.ch/t/john-walker-1949-2024/4305'}]

contents = []
for story in top_hn:
  contents.append(story['content'])

# Load the English model
nlp = spacy.load("en_core_web_sm")

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

print(chunks)

vo = voyageai.Client(api_key = VOYAGE_KEY)

# pass all strings through the embed now
text = [chunks[0]['noun_phrases']]
result = vo.embed(text, model="voyage-2")

print(result.embeddings)
