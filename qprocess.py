"""Questions preprocessor."""
import re


class Questions(object):
    """docstring for Question."""

    def __init__(self):
        """Constructor."""
        self.what_q = []
        self.who_q = []
        self.when_q = []
        self.affirmation_q = []
        self.unknown_q = []


class QClassifier(Questions):
    """docstring for QClassifier."""

    def __init__(self):
        """Init."""
        Questions.__init__(self)

    def add_to_what_q(self, question):
        """Add to WhoQ."""
        self.what_q.append(question)

    def add_to_who_q(self, question):
        """Add to WhoQ."""
        self.who_q.append(question)

    def add_to_affirmation_q(self, question):
        """Add to WhoQ."""
        self.affirmation_q.append(question)

    def add_to_when_q(self, question):
        """Add to WhoQ."""
        self.when_q.append(question)

    def add_to_unknown_q(self, question):
        """Unknown q."""
        self.unknown_q.append(question)

    def write_to_file(self, file_name, questions):
        """Write to file."""
        f = open(file_name, 'w')
        for element in questions:
            f.write(element)
        f.close


def main():
    """Docstring for main method."""
    quest = QClassifier()
    with open('row_data.txt') as f:
        contents = f.readlines()
        for content in contents:
            if re.search(',,, when', content):
                quest.add_to_when_q(content.split('?', 1)[0].lower().replace("?", "")+"\n")
            elif re.search(',,, what', content):
                quest.add_to_what_q(content.split('?', 1)[0].lower().replace("?", "")+"\n")
            elif re.search(',,, who', content):
                quest.add_to_who_q(content.split('?', 1)[0].lower().replace("?", "")+"\n")
            elif re.search(',,, unknown', content):
                quest.add_to_unknown_q(content.split('?', 1)[0].lower().replace("?", "")+"\n")
            elif re.search(',,, affirmation', content):
                quest.add_to_affirmation_q(content.split('?', 1)[0].lower().replace("?", "")+"\n")
    quest.write_to_file('what_questions.txt', quest.what_q)
    quest.write_to_file('who_questions.txt', quest.who_q)
    quest.write_to_file('when_questions.txt', quest.when_q)
    quest.write_to_file('unknown_questions.txt', quest.unknown_q)
    quest.write_to_file('affirmation_questions.txt', quest.affirmation_q)

if __name__ == '__main__':
    main()
