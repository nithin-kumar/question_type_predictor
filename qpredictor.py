"""Training Classifier + Prediction."""
import sys


class DocumentCollection(object):
    """docstring for DocumentCollection."""

    def __init__(self, file_name, catogory):
        """Constructor."""
        super(DocumentCollection, self).__init__()
        f = open(file_name)
        self.documents = f.readlines()
        self.catogory = catogory

    def get_word_frequency_table(self):
        """Frequency of words in each docs collection."""
        word_frequency_table = {}
        total_word_count = 0
        for document in self.documents:
            words = document.split()
            for word in words:
                total_word_count += 1
                if word not in word_frequency_table:
                    word_frequency_table[word] = 1
                else:
                    word_frequency_table[word] += 1
        word_frequency_table['total_word_count'] = total_word_count
        word_frequency_table['unique_word_count'] = len(word_frequency_table.keys())
        return word_frequency_table


class MultinomialNaiveBayesClassifier(DocumentCollection):
    """docstring for Classifier."""

    def __init__(self, training_data):
        """Classifier constructor."""
        self.number_of_classes = len(training_data.keys())
        self.classes = training_data.keys()
        self.training_data = training_data
        self.training_information = {}
        self.probabilty_information = {}
        self.vocabulary_size = 0

    def compute_training_information(self):
        """Training Data information."""
        information = {'total_documents': 0}
        for item in self.training_data:
            information[item] = {}
            doc_collection = DocumentCollection(self.training_data[item], item)
            # information[item] = {'documents': doc_collection}
            information[item]['document_length'] = len(doc_collection.documents)
            information[item]['word_frequency_table'] = doc_collection.get_word_frequency_table()
            information['total_documents'] += len(doc_collection.documents)
        self.training_information = information
        # print information['what']['word_frequency_table']
        # return information

    def compute_prior_probability(self):
        """Compute Prior Probability."""
        prior_probability_table = {}
        self.compute_training_information()
        for catogory in self.classes:
            prior_probability_table[catogory] = self.training_information[catogory]['document_length'] / float(self.training_information['total_documents'])
        self.probabilty_information['prior_probability'] = prior_probability_table

    def compute_likelyhood(self):
        """Likelyhood computation."""
        vocabulary_size = 0
        for catogory in self.classes:
            vocabulary_size += self.training_information[catogory]['word_frequency_table']['unique_word_count']
        self.vocabulary_size = vocabulary_size

    def train(self):
        """Train the classifier."""
        self.compute_prior_probability()
        self.compute_likelyhood()

    def classify(self, document):
        """Classify the document."""
        words = document.split()
        alpha = 1  # Add 1 Laplace smoothing
        rank = {}
        for catogory in self.classes:
            argmax = self.probabilty_information['prior_probability'][catogory]
            for word in words:
                if word in self.training_information[catogory]['word_frequency_table']:
                    word_frequency = self.training_information[catogory]['word_frequency_table'][word]
                else:
                    word_frequency = 0
                argmax *= (word_frequency + alpha) / float(self.training_information[catogory]['word_frequency_table']['total_word_count'] + self.vocabulary_size)
            rank[argmax] = catogory
        return rank[max(rank.keys())].upper()

    def validate(self, validation_set):
        """Validate the classifier."""


class UserInterface(object):
    """docstring for UserInterface."""

    @staticmethod
    def read_from_file(filename, classifier):
        """Read input from file."""
        input_file = open(filename)
        data = input_file.readlines()
        for question in data:
            print (question + "::" + classifier.classify(question.lower().replace("?", "")))

    @staticmethod
    def read_from_commandline(classifier):
        """Read input form commandline."""
        while True:
            print "\nQuestion?:"
            question = raw_input()
            print classifier.classify(question.lower().replace("?", ""))


def main():
    """Main Method."""
    print "Initializing classifier...."
    classifier = MultinomialNaiveBayesClassifier({'who': 'who_questions.txt', 'what': 'what_questions.txt', 'when': 'when_questions.txt', 'unknown': 'unknown_questions.txt', 'affirmarion': 'affirmation_questions.txt'})
    print "Training classifier...."
    classifier.train()
    if len(sys.argv) > 1:
        UserInterface.read_from_file(sys.argv[1], classifier)
    else:
        UserInterface.read_from_commandline(classifier)
if __name__ == '__main__':
    main()
