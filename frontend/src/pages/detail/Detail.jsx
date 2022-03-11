import React, { useState, useEffect } from "react";
import { useParams } from "react-router";

import mmlApi from "../../api/mmlApi";
import apiConfig from "../../api/apiConfig";

import "./detail.scss";
import CastList from "./CastList";
import VideoList from "./VideoList";
import propTypes from "prop-types";
import Button, { OutlineButton } from "../../components/button/Button";

import MovieList from "../../components/movie-list/MovieList";
import SeasonTab from "./SeasonTab";

const Detail = () => {
  const [providers, setProviders] = useState({});
  const [seriesDetail, setSeriesDetail] = useState(null);
  const [item, setItem] = useState(null);

  const { category, id } = useParams();

  const isSeries = category === "tv";

  useEffect(() => {
    const getDetail = async () => {
      const [response, providerRes, showDetail] = await Promise.all([
        mmlApi.detail(category, id, { params: {} }),
        mmlApi.getProviders(id, category),
        (isSeries && mmlApi.getSeriesDetail(id)) || null,
      ]);

      const data = providerRes.results.US;
      setItem(response);
      setProviders(data);

      if (isSeries) setSeriesDetail(showDetail);
      window.scrollTo(0, 0);
    };
    getDetail();
  }, [category, id]);

  return (
    <React.Fragment>
      {item && (
        <React.Fragment>
          <div
            className="banner"
            style={{
              backgroundImage: `url(${apiConfig.originalImage(
                item.backdrop_path || item.poster_path
              )})`,
            }}
          ></div>
          <div className="mb-3 movie-content container">
            <div className="movie-content__poster">
              <div
                className="movie-content__poster__img"
                style={{
                  backgroundImage: `url(${apiConfig.originalImage(
                    item.poster_path || item.backdrop_path
                  )})`,
                }}
              ></div>
            </div>
            <div className="movie-content__info">
              <h1 className="title">{item.title || item.name}</h1>
              <div className="genres">
                {item.genres &&
                  item.genres.slice(0, 5).map((genre, i) => (
                    <span key={i} className="genres__item">
                      {genre.name}
                    </span>
                  ))}
              </div>
              <p className="overview">{item.overview}</p>
              <div className="cast">
                <div className="section__header">
                  <h2>Casts</h2>
                </div>
                <CastList id={item.id} />
              </div>

              <div className="provider">
                <div className="section__header">
                  <h2>Where to watch</h2>
                </div>
                <div className="providers">
                  {providers?.buy?.map((item, i) => (
                    <div key={i} className="casts__item">
                      <div
                        className="casts__item__img"
                        style={{
                          backgroundImage: `url(${apiConfig.originalImage(
                            item.logo_path
                          )})`,
                        }}
                      ></div>
                      <p className="casts__item__name">{item.provider_name}</p>
                    </div>
                  ))}
                </div>

                {/* {providers?.buy?.map((item) => (
                  <div>
                    <img src={apiConfig.originalImage(item.logo_path)} alt="" />
                    {item.provider_name}
                  </div>
                ))} */}
              </div>
              <div className="smallbutton">
                {category === "movie" ? (
                  <Button
                    className="small"
                    onClick={() =>
                      window.open(
                        "https://www.2embed.ru/embed/tmdb/movie?id=" + item.id
                      )
                    }
                  >
                    Stream Unofficiallly
                  </Button>
                ) : (
                  <SeasonTab seasons={seriesDetail?.seasons} id={id} />
                )}
              </div>
              {/* <ul> */}
              {/* {providers?.buy?.map((item) => (
                <div>
                  <img src={apiConfig.originalImage(item.logo_path)} alt="" />
                  {item.provider_name}
                </div>
              ))} */}
              {/* </ul> */}
            </div>
          </div>
          <div className="container">
            <div className="section mb-3">
              <VideoList id={item.id} />
            </div>
            <div className="section mb-3">
              <div className="section__header mb-2">
                <h2>Similar</h2>
              </div>
              <MovieList category={category} type="similar" id={item.id} />
            </div>
          </div>
        </React.Fragment>
      )}
    </React.Fragment>
  );
};

export default Detail;
