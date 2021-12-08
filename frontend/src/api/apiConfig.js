const apiConfig ={
    baseUrl: 'https://api.themoviedb.org/3/',
    apiKey: 'bdf8dad8dbd206c22a2ea4685276242c',
    originalImage: (imgPath) => 'https://image.tmdb.org/t/p/original/${imgPath}',
    w500Image: (imgPath) => 'https://image.tmdb.org/t/p/w500/${imgPath}'

}

export default apiConfig;
