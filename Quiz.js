import quizQuestion from './utils/quizQuestion.js';

class Quiz {
  constructor(user) {
    this.user = user;
    this.quizState = null;
    this.Success = false;
  }

  startQuiz() {
    // Инициализация викторины
    this.quizState = {
      correctAnswers: 0,
      questionIndex: 0,
    };
  }

  getQuestion() {
    if (this.quizState && this.quizState.questionIndex < quizQuestion.length) {
      const questionObj = quizQuestion[this.quizState.questionIndex];
      const questionNumber = this.quizState.questionIndex + 1;

      const options = questionObj.options.map((option, index) => {
        return [
          { text: option.text, callback_data: `quiz_answer_${index + 1}` },
        ];
      });

      const text = `Вопрос ${questionNumber}:\n${questionObj.question}`;

      return {
        text,
        options,
      };
    }

    return null;
  }

  checkAnswer(userAnswer) {
    const currentQuestion = quizQuestion[this.quizState.questionIndex];

    if (currentQuestion.correctAnswer === +userAnswer - 1) {
      this.quizState.correctAnswers++;
      this.quizState.questionIndex++;

      // Победа
      if (this.quizState.questionIndex === quizQuestion.length) {
        this.user.fullAccess = true;
        this.Success = true;

        return {
          text: `${this.getResult()} Вы освободили Элис!`,
          options: [[{ text: '🏠 Вернуться в меню', callback_data: 'menu' }]],
        };
      }

      const nextQuestion = this.getQuestion();

      if (nextQuestion) {
        return {
          text: 'Правильно! Следующий вопрос:\n\n' + nextQuestion.text,
          options: nextQuestion.options,
        };
      }
    } else {
      const resultMessage = `Неправильно! Попробуйте ещё раз. ${this.getResult()}`;
      this.reset();

      const newQuestion = this.getQuestion();

      return {
        text:
          resultMessage +
          '\n\nВикторина начинается заново:\n\n' +
          newQuestion.text,
        options: newQuestion.options,
      };
    }

    return null;
  }

  getResult() {
    return `Вы ответили правильно на ${this.quizState.correctAnswers} из ${quizQuestion.length} вопросов.`;
  }

  reset() {
    this.startQuiz();
  }
}

export default Quiz;
