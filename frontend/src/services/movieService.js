const baseUrl = "http://127.0.0.1:5000/json";

export const fetchMovies = async () => {
  const response = await fetch(baseUrl);
  const data = await response.json();
  return data ||[];
};
