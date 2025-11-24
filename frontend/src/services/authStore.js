// src/services/authStore.js
let currentUser = null;

export const setCurrentUser = (user) => {
  currentUser = user;
};

export const getCurrentUser = () => currentUser;
