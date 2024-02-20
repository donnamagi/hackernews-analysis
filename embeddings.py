import voyageai
from dotenv import load_dotenv
import os
import json

load_dotenv()
VOYAGE_KEY = os.getenv("VOYAGE_API_KEY")

# some sample data
top_hn = [
  {'comment_count': 3,
  'comment_ids': [39439173, 39439261],
  'content': 'The article discusses a study on an Android runtime (ART) '
             'hijacking mechanism for bytecode injection through a detailed '
             'analysis of the SecNeo packer used to protect the DJI Pilot '
             'Android application. The packer is used to obfuscate the '
             'application code, and the analysis reveals a runtime mechanism '
             'implemented by DJI to protect its code. The study uses a Python '
             'proof-of-concept tool called DxFx to statically unpack the DJI '
             'Pilot application and understand the various mechanisms '
             'implemented by the packer. The analysis shows that the packer '
             'leaves only a bootstrap code in the bytecode to launch the '
             "application's unpacking phase, which is present in a native "
             'library libDexHelper.so. The business logic of the application '
             'is located in the native library, and the first step in the '
             "analysis is to find the bytecode containing the application's "
             'business logic.',
  'date': '2024-02-20T10:06:08.948040',
  'hn_comment': '',
  'hn_id': 39438842,
  'title': 'DJI – The Art of Obfuscation',
  'url': 'https://blog.quarkslab.com/dji-the-art-of-obfuscation.html'},
 {'comment_count': 1,
  'comment_ids': [39439154],
  'content': 'LWN, a popular technology publication, relies on subscribers to '
             'exist. The article discusses the integration of Rust code into '
             'the Linux kernel and how it is influenced by two approaches to '
             'designing abstraction layers for file systems. One approach '
             'favored by most kernel C programmers, involves defining file '
             'system tasks in a single trait called FileSystem, while the '
             'other approach defines file and filesystem-related operations '
             'across multiple object types in the C code. The article '
             'concludes that Rust developers implementing a file system using '
             'the posted abstractions will have to put together an '
             'implementation that follows the FileSystem trait organization.',
  'date': '2024-02-20T10:06:08.948043',
  'hn_comment': '',
  'hn_id': 39438944,
  'title': 'LKML discusses merging Rust access to filesystem APIs',
  'url': 'https://lwn.net/Articles/958072/'}
]

def get_content_embeddings(text):
  vo = voyageai.Client(api_key = VOYAGE_KEY)
  result = vo.embed(text, model="voyage-2")
  return result.embeddings[0]

def main():
  return get_content_embeddings([top_hn[0]['content']])

main()