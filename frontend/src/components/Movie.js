import React from "react";
import { fetchMovies } from "../services/movieService";

const Movie = () => {
  const [movies, setMovies] = React.useState([]);

  React.useEffect(() => {
    (async function () {
      const data = await fetchMovies();
      setMovies(data);
    })();
  }, []);

  return (
    <div>
      {movies.map((movie) => (
        <ul id={movie.Distance}>
          <li>{movie.Title} </li>
          <li>{movie.Genre} </li>
          <li>{movie.Distance} </li>
        </ul>
      ))}
    </div>
  );
};

export default Movie;
