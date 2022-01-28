import random


class Wrong:
    appeared = 0
    answered = 0
    
    def __init__(self, answer):
        self.answer = answer



class Question:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def ask_and_check(self):
        response = input(f"{self.question}\nWhat is your answer? ")
        if response == self.answer:
            print("Correct!\n")
            return True
        else:
            print(f"Sorry no. Correct answer: {self.answer}\n")
            return False


class MCQuestion(Question):
    SIZE_LIST = 4
    wrong_ans_objs = []
    
    def __init__(self, question, answer, wrong_answers=[]):
        super().__init__(question, answer)
        for answer in wrong_answers:
            wrong_ans_objs.append(Wrong(answer))
        self.wrong_answers = wrong_answers.copy()

    def ask_and_check(self):
        random.shuffle(self.wrong_answers)
        options = self.wrong_answers[:self.SIZE_LIST-1] + [self.answer]
        #options = self.wrong_answers + [self.answer]
        random.shuffle(options)
        print(f"{self.question}")
        for i, option in enumerate(options):
            print(f"{i+1}: {option}")
        response = input("Which is your answer? ")
        if options[int(response)-1] == self.answer:
            print("Correct!\n")
            return True
        else:
            corr = options.index(self.answer)+1
            print(f"Sorry no. Correct answer: {corr}\n")
            return False

    def add_wrong(self, wrong):
        self.wrong_answers.append(wrong)


class Quiz:
    total = 0
    num_correct = 0
    
    def __init__(self, name, questions=[]):
        self.name = name
        self.questions = questions

    def add_question(self, question):
        self.questions.append(question)

    def do(self):
        self.total = len(self.questions)
        self.num_correct = 0
        print(self.name)
        print(f"{'='*len(self.name)}\n")
        for question in self.questions:
            response = question.ask_and_check()
            if response == True:
                self.num_correct += 1

        print(f"You answered {self.num_correct} out of {self.total} correctly.\n")
        return self.total == self.num_correct

    def do_until_right(self):
        perfect = False
        while not perfect:
            perfect = self.do()


def create_quiz_from_file(filename):
    with open(filename, encoding='utf8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            command, data = line.split(' ', 1)
            data = data.strip()
            if command == 'name':
                quiz = Quiz(data)
            elif command == 'q':
                text = data
            elif command == 'a':
                question = Question(text, data)
                quiz.add_question(question)
            elif command == 'mca':
                question = MCQuestion(text, data)
                quiz.add_question(question)
            elif command == 'w':
                question.add_wrong(data)
    return quiz
    
