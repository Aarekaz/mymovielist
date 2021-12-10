import React, { useState, useEffect} from "react";
import propTypes from 'prop-types';

import './movie-list.scss';

import { Swiper, SwiperSlide } from "swiper/react";
import { Link } from "react-router-dom";

import Button from "../button/Button";

import mmlApi, { category } from "../../api/mmlApi";
import apiConfig from "../../api/apiConfig";

const MovieList = props => {

    const [items, setItems] = useState([]);

    useEffect(() => {
        
        const getList = async () => {
            let response = null;
            const params = {};

            if (props.type !== 'similar') {
                switch(props.category) {
                    case category.movie:
                        response = await mmlApi.getMoviesList(props.type, {params});
                        break;
                    default: 
                    response = await mmlApi.getShowsList(props.type, {params});
                }
            } else {
                response = await mmlApi.similar(props.category, props.id);
            }
            setItems(response.results);
        }
        getList();
    }, []);


    return (
        <div className="movie-list">
            <Swiper
                grabCursor={true}
                spaceBetween={10}
                slidesPerView={'auto'}
            >
                {
                    items.map((item, i) => (
                        <SwiperSlide key={i}>
                            <img src={apiConfig.w500Image(items.poster_path)} alt="" />
                        </SwiperSlide>
                    ))
                }
            </Swiper>
        </div>
    );
}

MovieList.propTypes ={
    category: propTypes.string.isRequired,
    type: propTypes.string.isRequired

}

export default MovieList;
