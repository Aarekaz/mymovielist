import axiosClient from "./axiosClient";

export const category = {
  movie: "movie",
  shows: "tv",
};

export const movieType = {
  upcoming: "upcoming",
  top_rated: "top_rated",
  popular: "popular",
};

export const tvType = {
  top_rated: "top_rated",
  popular: "popular",
  on_air: "on_air",
};

const mmlApi = {
  getMoviesList: (type, params) => {
    const url = "movie/" + movieType[type];
    return axiosClient.get(url, params);
  },
  getTvList: (type, params) => {
    const url = "tv/" + tvType[type];
    return axiosClient.get(url, params);
  },

  getVideos: (cate, id) => {
    const url = cate + "/" + id + "/videos";
    return axiosClient.get(url, { params: {} });
  },
  search: (cate, params) => {
    const url = `search${cate ? `${cate}` : "/multi"}`;
    return axiosClient.get(url, params);
  },
  detail: (cate, id, params) => {
    const url = cate + "/" + id;
    return axiosClient.get(url, params);
  },
  credits: (cate, id) => {
    const url = cate + "/" + id + "/credits";
    return axiosClient.get(url, { params: {} });
  },
  similar: (cate, id) => {
    const url = cate + "/" + id + "/similar";
    return axiosClient.get(url, { params: {} });
  },

  getProviders: (id) => {
    const url = `movie/${id}/watch/providers`;
    return axiosClient.get(url, { params: {} });
  },
};

export default mmlApi;
