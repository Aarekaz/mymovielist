import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";

import "./movie-list.scss";

import { SwiperSlide, Swiper } from "swiper/react";
import { Link } from "react-router-dom";

import Button from "../button/Button";

import mmlApi, { category } from "../../api/mmlApi";
import apiConfig from "../../api/apiConfig";

import MovieCard from "../movie-card/MovieCard";

const MovieList = (props) => {
  const [items, setItems] = useState([]);

  useEffect(() => {
    const getList = async () => {
      let response = null;
      const params = {};

      if (props.type !== "similar") {
        switch (props.category) {
          case category.movie:
            response = await mmlApi.getMoviesList(props.type, { params });
            break;
          default:
            response = await mmlApi.getTvList(props.type, { params });
        }
      } else {
        response = await mmlApi.similar(props.category, props.id);
      }
      setItems(response.results);
    };
    getList();
  }, [props.category, props.id, props.type]);

  return (
    <div className="movie-list">
      <Swiper grabCursor={true} spaceBetween={10} slidesPerView={"auto"}>
        {items.map((item, i) => (
          <SwiperSlide key={i}>
            <MovieCard
              item={item}
              category={props.category || item.media_type}
            />
          </SwiperSlide>
        ))}
      </Swiper>
    </div>
  );
};

MovieList.propTypes = {
  category: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired,
};

export default MovieList;
