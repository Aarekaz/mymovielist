import React from "react";

import { useParams } from "react-router-dom";

import PageHeader from "../components/page-header/PageHeader";

import { category as cate } from "../api/mmlApi";
import MovieGrid from "../components/movie-grid/MovieGrid";

const Catalog = () => {
  const { category } = useParams();
  console.log("category", category);
  return (
    <React.Fragment>
      <PageHeader>
        {!category
          ? "Search Result"
          : category === cate.movie
          ? "Movies"
          : "Shows"}
      </PageHeader>
      <div className="container">
        <div className="section mb-3">
          <MovieGrid category={category} />
        </div>
      </div>
    </React.Fragment>
  );
};

export default Catalog;
