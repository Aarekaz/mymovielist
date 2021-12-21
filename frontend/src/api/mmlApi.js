import axiosClient from "./axiosClient";

export const category={
    movie: 'movie',
    shows: 'tv'
}

export const movieType ={
    upcoming: 'upcoming',
    top_rated: 'top_rated',
    popular: 'popular'
}

export const tvType ={
    top_rated: 'top_rated',
    popular: 'popular',
    on_air: 'on_air'
}

const mmlApi = {
    getMoviesList: (type, params) =>{
        const url = 'movie/' + movieType[type];
        return axiosClient.get(url, params);
    },
    getTvList: (type, params) =>{
        const url = 'tv/' + tvType[type];
        return axiosClient.get(url, params);
    },
    //getMoviesList: (type, params) =>{
      //  const url = 'movie/' + movieType[type];
        //return axiosClient.get(url, params);
    //},
    getVideos: (cate, id) =>{
        const url = category[cate] + '/' + id + '/videos';
        return axiosClient.get(url, {params: {}});
    },
    search: (cate, params) =>{
        const url = 'search/'+ category[cate];
        return axiosClient.get(url, params);
    },
    detail: (cate, id, params) =>{
        const url = category[cate] + '/' + id;
        return axiosClient.get(url, params);
    },
    credits: (cate, id) =>{
        const url = category[cate] + '/' + id + '/credits';
        return axiosClient.get(url, {params: {}});
    },
    similar: (cate, id) =>{
        const url = category[cate] + '/' + id + '/similar';
        return axiosClient.get(url, {params: {}});
    },
}

export default mmlApi;
