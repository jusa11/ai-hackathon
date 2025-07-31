class UserHistory {
  constructor(userId) {
    this.userId = userId;
    this.context = [];
  }

  addMessage(content, role, mode) {
    this.context.push({
      role: role,
      content: content,
      mode: mode,
    });

    if (this.context.length > 10) {
      this.context.shift();
    }
  }

  getHistory(mode) {
    return this.context
      .filter((message) => message.mode === mode)
      .map((message) => ({
        role: message.role,
        content: message.content,
      }));
  }

  clearHistory() {
    this.context = [];
  }
}

export default UserHistory;
