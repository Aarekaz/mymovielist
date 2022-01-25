import React, { useRef, useEffect, useState } from "react";
import "./header.scss";

import { Link, useLocation, useHistory } from "react-router-dom";
import Button from "../button/Button";
import Input from "../input/Input";
import logo from "../../assets/tmovie.png";

import "../movie-grid/movie-grid.scss";

const headerNav = [
  {
    display: "Home",
    path: "/",
  },
  {
    display: "Movies",
    path: "/movie",
  },
  {
    display: "Shows",
    path: "/tv",
  },
];

const Header = () => {
  const [keyword, setKeyword] = useState("");
  const { pathname } = useLocation();
  const history = useHistory();
  const headerRef = useRef(null);

  const active = headerNav.findIndex((e) => e.path === pathname);

  useEffect(() => {
    const shrinkHeader = () => {
      if (
        document.body.scrollTop > 100 ||
        document.documentElement.scrollTop > 100
      ) {
        headerRef.current.classList.add("shrink");
      } else {
        headerRef.current.classList.remove("shrink");
      }
    };
    window.addEventListener("scroll", shrinkHeader);
    return () => {
      window.removeEventListener("scroll", shrinkHeader);
    };
  }, []);

  const goToSearch = (event) => {
    event.preventDefault();
    console.log("go to the search called", `/search/${keyword}`);
    if (keyword) history.push(`/search/${keyword}`);
  };

  return (
    <div ref={headerRef} className="header">
      <div className="header__wrap container">
        <div className="logo">
          <img src={logo} alt="" />
          <Link to="/">MyMovieList</Link>
        </div>
        <form onSubmit={goToSearch}>
          <Input
            type="text"
            placeholder="Enter movie/show name"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
          />
          <Button type="submit" className="small">
            Search
          </Button>
        </form>
        <ul className="header__nav">
          {headerNav.map((e, i) => (
            <li key={i} className={`${i === active ? "active" : ""}`}>
              <Link to={e.path}>{e.display}</Link>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Header;
