class QuizGame:

    def __init__(self, questions):
        self.questions = questions
        self.current_index = 0
        self.score = 0
        self.checkpoint_score = 0

    def get_current_question(self):
        return self.questions[self.current_index]

    def answer(self, answer_index):

        question = self.get_current_question()

        correct = answer_index == question["correct"] #промяна

        if correct:   #промяна
            self.score += question["reward"] #промяна

        self.current_index += 1     #промяна

        return correct           #промяна

    def is_finished(self):
        return self.current_index >= len(self.questions)