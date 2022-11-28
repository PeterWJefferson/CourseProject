import numpy as np
import math
import heapq
import random


def normalize(input_matrix):
    """
    Normalizes the rows of a 2d input_matrix so they sum to 1
    """

    row_sums = input_matrix.sum(axis=1)
    try:
        assert (np.count_nonzero(row_sums)==np.shape(row_sums)[0]) # no row should sum to zero
    except Exception:
        raise Exception("Error while normalizing. Row(s) sum to zero")
    new_matrix = input_matrix / row_sums[:, np.newaxis]
    return new_matrix

       
class Corpus(object):

    """
    A collection of documents.
    """

    def __init__(self, documents_path):
        """
        Initialize empty document list.
        """
        self.documents = []
        self.vocabulary = []
        self.likelihoods = []
        self.documents_path = documents_path
        self.term_doc_matrix = None 
        self.document_topic_prob = None  # P(z | d)
        self.topic_word_prob = None  # P(w | z)
        self.topic_prob = None  # P(z | d, w)

        self.number_of_documents = 0
        self.vocabulary_size = 0

    def build_corpus(self):
        """
        Read document, fill in self.documents, a list of list of word
        self.documents = [["the", "day", "is", "nice", "the", ...], [], []...]
        
        Update self.number_of_documents
        """
        

        with open(self.documents_path, 'r') as file:
            for line in file.readlines():
                doc = list()
                doc.extend(line.split())
                self.documents.append(doc)
                self.number_of_documents += 1


    def build_vocabulary(self):
        """
        Construct a list of unique words in the whole corpus. Put it in self.vocabulary
        for example: ["rain", "the", ...]

        Update self.vocabulary_size
        """
        _set = set()
        for document in self.documents:
            _set.update(document)
        self.vocabulary = _set
        self.vocabulary_size = len(self.vocabulary)

    def build_term_doc_matrix(self):
        """
        Construct the term-document matrix where each row represents a document, 
        and each column represents a vocabulary term.

        self.term_doc_matrix[i][j] is the count of term j in document i
        """
        
        self.term_doc_matrix = np.zeros(shape=(self.number_of_documents, self.vocabulary_size))
        vocab_dist = {j: i for i, j in enumerate(self.vocabulary)}
        for i, document in enumerate(self.documents):
            for t in document:
                self.term_doc_matrix[i][vocab_dist[t]] += 1


    def initialize_randomly(self, number_of_topics):
        """
        Randomly initialize the matrices: document_topic_prob and topic_word_prob
        which hold the probability distributions for P(z | d) and P(w | z): self.document_topic_prob, and self.topic_word_prob

        Don't forget to normalize! 
        HINT: you will find numpy's random matrix useful [https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.random.random.html]
        """

        self.document_topic_prob = normalize(np.random.random(size=(self.number_of_documents, number_of_topics)))
        self.topic_word_prob = normalize(np.random.random(size=(number_of_topics, len(self.vocabulary))))

    def initialize_uniformly(self, number_of_topics):
        """
        Initializes the matrices: self.document_topic_prob and self.topic_word_prob with a uniform 
        probability distribution. This is used for testing purposes.

        DO NOT CHANGE THIS FUNCTION
        """
        self.document_topic_prob = np.ones((self.number_of_documents, number_of_topics))
        self.document_topic_prob = normalize(self.document_topic_prob)

        self.topic_word_prob = np.ones((number_of_topics, len(self.vocabulary)))
        self.topic_word_prob = normalize(self.topic_word_prob)

    def initialize(self, number_of_topics, random=False):
        """ Call the functions to initialize the matrices document_topic_prob and topic_word_prob
        """
        print("Initializing PLSA...")

        if random:
            self.initialize_randomly(number_of_topics)
        else:
            self.initialize_uniformly(number_of_topics)

    def expectation_step(self):
        """ The E-step updates P(z | w, d)
        """
        # print("E step:")
        
        self.topic_word_prob = np.nan_to_num(self.topic_word_prob)
        for document in range(self.topic_prob.shape[0]):
            for voc in range(self.topic_prob.shape[2]):
                self.topic_prob[document, :, voc] = self.document_topic_prob[document, :] * self.topic_word_prob[:, voc]
                self.topic_prob[document, :, voc] /= self.topic_prob[document, :, voc].sum()
        self.topic_word_prob = np.nan_to_num(self.topic_word_prob)
            
    def maximization_step(self, number_of_topics):
        """ The M-step updates P(w | z)
        """
        # print("M step:")
        
        # update P(w | z)
        
        for t in range(self.topic_prob.shape[1]):
            for voc in range(self.topic_prob.shape[2]):
                self.topic_word_prob[t, voc] = self.term_doc_matrix[:, voc].dot(self.topic_prob[:, t, voc])
            self.topic_word_prob[t, :] /= self.topic_word_prob[t, :].sum()
        self.topic_word_prob = np.nan_to_num(self.topic_word_prob)
        
        # update P(z | d)

        for document in range(self.topic_prob.shape[0]):
            for topic in range(self.topic_prob.shape[1]):
                self.document_topic_prob[document, topic] = self.term_doc_matrix[document, :].dot(self.topic_prob[document, topic, :])
            self.document_topic_prob[document, :] /= self.document_topic_prob[document, :].sum()
        self.document_topic_prob = np.nan_to_num(self.document_topic_prob)


    def calculate_likelihood(self, number_of_topics):
        """ Calculate the current log-likelihood of the model using
        the model's updated probability matrices
        
        Append the calculated log-likelihood to self.likelihoods

        """
        self.likelihoods.append(np.sum(np.log(np.matmul(self.document_topic_prob, self.topic_word_prob)) * self.term_doc_matrix))
        return self.likelihoods[-1]

    def plsa(self, number_of_topics, max_iter, epsilon):

        """
        Model topics.
        """
        # print ("EM iteration begins...")
        
        # build term-doc matrix
        self.build_term_doc_matrix()
        
        # Create the counter arrays.
        
        # P(z | d, w)
        self.topic_prob = np.zeros([self.number_of_documents, number_of_topics, self.vocabulary_size], dtype=np.float)

        # P(z | d) P(w | z)
        self.initialize(number_of_topics, random=False)

        # Run the EM algorithm
        current_likelihood = 0.0

        prev_prob = self.topic_prob.copy()

        for iteration in range(max_iter):
            # print("Iteration #" + str(iteration + 1) + "...")
            self.expectation_step()
            prev_prob = self.topic_prob.copy()
            self.maximization_step(number_of_topics)
            self.calculate_likelihood(number_of_topics)
            tmp_likelihood = self.calculate_likelihood(number_of_topics)
            if iteration > 100 and abs(current_likelihood - tmp_likelihood) < epsilon/10:
                return tmp_likelihood
            current_likelihood = tmp_likelihood
            # print(max(self.likelihoods))



def get_topics(file_path = 'data/DBLP.txt', top_N = 5, depth = 10):
    documents_path = file_path
    corpus = Corpus(documents_path)  # instantiate corpus
    lines = open(file_path).readlines()
    random.shuffle(lines)
    open(file_path, 'w').writelines(lines)
    corpus.build_corpus()
    corpus.build_vocabulary()
    number_of_topics = 2
    max_iterations = depth
    epsilon = 0.001
    corpus.plsa(number_of_topics, max_iterations, epsilon)
    prob_sums = corpus.topic_word_prob.sum(axis=0)
    top_indices = heapq.nlargest(5, range(len(prob_sums)), key=list(prob_sums).__getitem__)
    top_N_topics = []
    for index in top_indices:
        top_N_topics.append(list(corpus.vocabulary)[index])
    return top_N_topics
