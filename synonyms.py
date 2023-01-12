import math

def norm(vec):
  '''Return the norm of a vector stored as a dictionary,
  as described in the handout for Project 3.
  '''
  sum_of_squares = 0.0
  for x in vec:
      sum_of_squares += vec[x] * vec[x]

  return math.sqrt(sum_of_squares)

def cosine_similarity(vec1, vec2):
  # Dot product
  num = []
  for word in vec1:
    if word in vec2:
      num.append(vec1[word]*vec2[word])
  num = sum(num)

  # Magnitude
  denom = norm(vec1)*norm(vec2)
  return num/denom

def build_semantic_descriptors(sentences):
# Fix where it is adding multiple times per sentence
  sem_desc = {}
  for sentence in sentences:
    for p_word in range(len(sentence)):
      if sentence[p_word] not in sem_desc: # Parent word
        sem_desc[sentence[p_word]] = {}
      if sentence.index(sentence[p_word]) == p_word:
        for c_word in range(len(sentence)): # Check Child_word in sentence
          if sentence.index(sentence[c_word]) == c_word and sentence[c_word] != sentence[p_word]:
            if sentence[c_word] in sem_desc[sentence[p_word]]:
              sem_desc[sentence[p_word]][sentence[c_word]] += 1
            else:
              sem_desc[sentence[p_word]][sentence[c_word]] = 1
  return sem_desc

def build_semantic_descriptors_from_files(filenames):
  text = []
  punctuations = [",", "--", "-", ":", ";", "\"", "*", "(", ")", "“", "”", "–", "<", ">", "+", "/", "\\", "%", "#", "@", "~", "=", "{", "}", "[", "]", "$"]
  for i in range(len(filenames)):
    file = open(filenames[i], "r", encoding="latin1")
    file_read = (file.read()).lower()
    for punct in punctuations:
      file_read = file_read.replace(punct, " ")
    file_read = file_read.replace("?", ".")
    file_read = file_read.replace("!", ".")
    sentences = file_read.split(".")
    for sentence in sentences:
      text.append(sentence.split())
  return build_semantic_descriptors(text)

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
  '''returns the element of 'choices' which has the largest semantic similarity to word, with the semantic similarity computed using the data in semantic_descriptors and the similarity function similarity_fn.
  '''
  scores = [-1]*len(choices)
  if word in semantic_descriptors:
    word_desc = semantic_descriptors[word]

    for i in range(len(choices)):
      if choices[i] in semantic_descriptors:
        choice_desc = semantic_descriptors[choices[i]]
        scores[i] = similarity_fn(word_desc, choice_desc)
    max_score = max(scores)
  return choices[scores.index(max_score)]

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
  '''returns the percentage (i.e., float between 0.0 and 100.0) of questions on which most_similar_word() guesses the answer correctly using the semantic descriptors stored in semantic_descriptors, using the similarity function similariy_fn'''
  test = open(filename, "r", encoding="latin1")
  test_r = test.read()
  test_q = test_r.splitlines() # Split into questions
  n = len(test_q)
  w = 0
  for questions in test_q:
    question = questions.split() # List representing a question
    answer = most_similar_word(question[0], question[2:], semantic_descriptors, similarity_fn)
    if answer == question[1]:
      w += 1
  return w/n*100
