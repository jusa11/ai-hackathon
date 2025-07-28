class UserHistory {
  constructor(userName) {
    this.userName = userName;
    this.context = [];
  }

  addMessage(content, role) {
    this.context.push({
      role: role,
      content: content,
    });

    if (this.context.length > 4) {
      this.context.shift();
    }
  }

  getHistory() {
		return this.context.map((message) => ({
			role: message.role,
			content: message.content,
		}));
  }

  clearHistory() {
    this.context = [];
  }
}

export default UserHistory;
