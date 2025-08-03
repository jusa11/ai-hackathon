class UserHistory {
  constructor(userId) {
    this.userId = userId;
    this.contexts = new Map(); // ключ — mode, значение — массив сообщений
    this.quiz = null;
    this.fullAccess = false;
  }

  addMessage(content, role, mode) {
    if (!this.contexts.has(mode)) {
      this.contexts.set(mode, []);
    }

    const history = this.contexts.get(mode);
    history.push({ role, content });

    if (history.length > 10) {
      history.shift();
    }
  }

  getHistory(mode) {
    return this.contexts.get(mode) || [];
  }

  clearHistory() {
    this.contexts.clear();
  }

  setQuiz(quiz) {
    this.quiz = quiz;
  }

  getQuiz() {
    return this.quiz;
  }
}

export default UserHistory