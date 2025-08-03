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
    // Возвращает текущий вопрос викторины в отформатированном виде
    if (this.quizState && this.quizState.questionIndex < quizQuestion.length) {
      const questionObj = quizQuestion[this.quizState.questionIndex];
      const questionNumber = this.quizState.questionIndex + 1;

      const options = questionObj.options
        .map((option, index) => `${index + 1}. ${option.text}`)
        .join('\n');

      return `Вопрос ${questionNumber}:\n${questionObj.question}\n\n${options}`;
    }

    return null;
  }

  checkAnswer(userAnswer) {
    // Проверка ответа пользователя
    const currentQuestion = quizQuestion[this.quizState.questionIndex];

    if (currentQuestion.correctAnswer === +userAnswer) {
      this.quizState.correctAnswers++;
      this.quizState.questionIndex++;

      const nextQuestion = this.getQuestion();

      // Победа
      if (this.quizState.questionIndex === quizQuestion.length) {
        this.user.fullAccess = true;
        this.Success = true;
        return `${this.getResult()}. Вы освободили Элис`;
      }

      if (nextQuestion) {
        return 'Правильно! Следующий вопрос: ' + nextQuestion;
      }
    } else {
      const resultMessage = `Неправильно! Попробуйте ещё раз. ${this.getResult()}`;
      this.reset();
      return (
        resultMessage +
        '\n\nВикторина начинается заново:\n' +
        this.getQuestion()
      );
    }
  }

  getResult() {
    return `Вы ответили правильно на ${this.quizState.correctAnswers} из ${quizQuestion.length} вопросов.`;
  }

  reset() {
    this.startQuiz();
  }
}

export default Quiz;
