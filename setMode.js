import UserHistory from './UserHistory.js';

export default function getOrCreateUser(users, userId) {
  if (!users.has(userId)) {
    users.set(userId, new UserHistory(userId));
  }
  return users.get(userId);
}
