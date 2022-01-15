import 'swiper/swiper.min.css';
import './assets/boxicons-2.0.7/css/boxicons.min.css';
import './App.scss';

import { BrowserRouter, Route } from 'react-router-dom';

import Header from './components/header/Header';
import Footer from './components/footer/Footer';

import Routes from './config/Routes';
import React from 'react';

function App() {
  return(
    <BrowserRouter>
        <Route render={props => (
        <React.Fragment>
              <Header {...props} />
              <Routes/>
              <Footer/>
        </React.Fragment>
        )}/>
    </BrowserRouter>
  );
}
  

export default App;
