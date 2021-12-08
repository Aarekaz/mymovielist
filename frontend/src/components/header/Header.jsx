import React, { useRef } from "react";
import './header.scss';

import { Link, useLocation } from 'react-router-dom';

import logo from '../../assets/tmovie.png';

const headerNav =[
    {
        display: 'Home',
        path: '/'
    },
    {
        display: 'Movies',
        path: '/movie'
    },
    {
        display: 'Shows',
        path: '/shows'
    }
];

const Header =() => {

    const { pathname } = useLocation();
    const headerRef = useRef(null);

    const active = headerNav.findIndex(e => e.path === pathname);



    return (
        <div ref={headerRef} className="header">
            <div className="header__wrap container">
                <div className="logo">
                    <img src={logo} alt="" />
                    <Link to="/">MyMovieList</Link>
                </div>
                <ul className="header__nav">
                    {
                        headerNav.map((e, i) => (
                            <li key= {i} className={`${i === active ? 'active' : ''}`}>
                                <Link to={e.pah}>
                                    {e.display}
                                </Link>
                            </li>
                        ))
                    }
                </ul>
            </div>
                 Header
             </div>
            );
}

export default Header;