// src/services/api.js

const BASE_URL = 'http://127.0.0.1:8000';

class APIError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

const handleResponse = async (response) => {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new APIError(
      errorData.error || errorData.detail || `HTTP ${response.status}`,
      response.status
    );
  }
  return response.json();
};

export const getBooks = async () => {
  const response = await fetch(`${BASE_URL}/books`);
  return handleResponse(response);
};

export const addBook = async (bookData) => {
  const response = await fetch(`${BASE_URL}/books`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(bookData),
  });
  return handleResponse(response);
};

export const addBookManual = async (bookData) => {
  const response = await fetch(`${BASE_URL}/books/manual`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(bookData),
  });
  return handleResponse(response);
};

export const updateBook = async (isbn, updates) => {
  const response = await fetch(`${BASE_URL}/books/${isbn}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(updates),
  });
  return handleResponse(response);
};

export const getBook = async (isbn) => {
  const response = await fetch(`${BASE_URL}/books/${isbn}`);
  return handleResponse(response);
};

export const deleteBook = async (isbn) => {
  const response = await fetch(`${BASE_URL}/books/${isbn}`, {
    method: 'DELETE',
  });
  return handleResponse(response);
};

export const searchBooks = async (query) => {
  const response = await fetch(`${BASE_URL}/search?q=${encodeURIComponent(query)}`);
  return handleResponse(response);
};

export const getStats = async () => {
  const response = await fetch(`${BASE_URL}/stats`);
  return handleResponse(response);
};

export const getHealth = async () => {
  const response = await fetch(`${BASE_URL}/health`);
  return handleResponse(response);
};