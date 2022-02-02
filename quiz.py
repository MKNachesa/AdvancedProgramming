import random


class Wrong:
    ans_selected = 0
    ans_offered = 0
    score = 0

    def __init__(self, answer):
        self.answer = answer

    def selected(self, wrong_ans_objs):
        self.wrong_ans_objs = wrong_ans_objs
        for answer in wrong_ans_objs:
            if answer in self.ans_selected:
                self.ans_selected[answer] += 1
            else:
                self.ans_selected[answer] = 1

    def offered(self, wrong_ans_objs):
        self.wrong_ans_objs = wrong_ans_objs
        for answer in self.wrong_ans_objs:
            if answer in self.ans_offered:
                self.ans_offered[answer] += 1
            else:
                self.ans_offered[answer] = 1

    def calculate_score(self):
        self.score = (2 * self.ans_selected + 1) / (self.ans_offered + 1)


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
    ans_to_offer = []

    def __init__(self, question, answer, wrong_answers_mc=[]):
        super().__init__(question, answer)
        self.wrong_answers_mc = wrong_answers_mc.copy()
        self.wrong_ans_objs = self.wrong_ans_objs.copy()
        for answer in self.wrong_answers_mc:
            self.wrong_ans_objs.append(Wrong(answer))

    def displays_wrong(self):
        for w in self.wrong_ans_objs:
            w.calculate_score()

        self.ans_to_offer = [ans for ans in sorted(self.wrong_ans_objs,
                                                   key=lambda item: item.score,
                                                   reverse=True)
                             ][:self.SIZE_LIST-1]
        for ans in self.ans_to_offer:
            ans.ans_offered += 1

        self.ans_to_offer = [ans.answer for ans in self.ans_to_offer] + [self.answer]
        random.shuffle(self.ans_to_offer)

    def ask_and_check(self):
        self.displays_wrong()
        print(f"{self.question}")
        for i, option in enumerate(self.ans_to_offer):
            print(f"{i + 1}: {option}")
        response = input("Which is your answer? ")
        if self.ans_to_offer[int(response) - 1] == self.answer:
            print("Correct!\n")
            return True
        else:
            wrong = self.ans_to_offer[int(response)-1]
            for wrong_ans in self.wrong_ans_objs:
                if wrong_ans.answer == wrong:
                    wrong_ans.ans_selected += 1
                    break
            print(f"Sorry no. Correct answer: {self.answer}\n")
            return False

    def add_wrong(self, wrong):
        self.wrong_ans_objs.append(Wrong(wrong))


class Quiz:
    total = 0
    num_correct = 0

    def __init__(self, name, questions=[]):
        self.name = name
        self.questions = questions.copy()

    def add_question(self, question):
        self.questions.append(question)

    def do(self):
        self.total = len(self.questions)
        self.num_correct = 0
        print(self.name)
        print(f"{'=' * len(self.name)}\n")
        for question in self.questions:
            response = question.ask_and_check()
            if response is True:
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
