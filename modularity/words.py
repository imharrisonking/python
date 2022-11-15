'''
Retrieve and print words from a URL.

Usage:
  python words.py <URL>
'''

import sys
from urllib.request import urlopen


def fetch_words(url):
  """ Fetch a list of words from a URL.

  Args:
    url: The URL of the UTF-8 text document.
  
  Returns:
    A list of strings containing the words from the document.
  """
  story = urlopen(url)
  story_words = []
  for line in story:
    line_words = line.decode('utf-8').split()
    for word in line_words:
      story_words.append(word)
  story.close()
  return story_words

def print_items(story_words):
  '''
  Print items one per line

  Args:
    url: An iterable series of printable items.
  '''
  for item in story_words:
    print(item)

def main(url):
  '''
  Print each word from a text documentt from a URL.

  Args:
    url: The URL of the UTF-8 text document.
  '''
  words = fetch_words(url)
  print_items(words)

# Below we check to see if the module is being executed itself (i.e., a command line run in which __name__ is '__main__' and so fetch_words() will run). Otherwise the module is being imported to another script and __name__ is 'words'. Therefore fetch_words() will not run

if __name__ == '__main__':
  main(sys.argv[1])