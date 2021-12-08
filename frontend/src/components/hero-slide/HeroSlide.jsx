import React, { useEffect, useState } from "react";

import SwiperCore, { Autoplay } from 'swiper';
import { Swiper, SwiperSlide } from 'swiper/react';

import mmlApi, { category, movieType } from "../../api/mmlApi";

import apiConfig from "../../api/apiConfig";
//import axiosClient from "../../api/axiosClient";

import './hero-slide.scss';

const HeroSlide = () => {

    SwiperCore.use([Autoplay]);

    const [movieItems, setMovieItems] = useState([]);

    useEffect(() => {
        const getMovies = async () => {
            const params = {page: 1}
            try {
                const response = await mmlApi.getMoviesList(movieType.popular, {params});
                setMovieItems(response.results.slice(0, 5));
                console.log(response);
            } catch {
                console.log('error');
            }
        }
        getMovies();
    }, []);



    return (
        <div className="hero-slide">
            <Swiper 
                modules={[Autoplay]}
                grabCursor={true}
                spaceBetween={0}
                slidesPerView={1}
            >
                {
                    movieItems.map((item, i) => (
                        <SwiperSlide key={i}>
                            {({ isActive}) => (
                                <img src={apiConfig.originalImage(item.backdrop_path)} />
                            )}

                        </SwiperSlide>
                    ))
                }

            </Swiper>
        </div>
    );
}

export default HeroSlide;

export function use(arg0: any[]) {
    throw new Error("Function not implemented.");
}

