import React from "react";

import { Route, Switch } from "react-router-dom";

import Home from "../pages/Home";
import Catalog from "../pages/Catalog";
import Detail from "../pages/detail/Detail";

const Routes = () => {
  return (
    <Switch>
      <Route exact path="/search/:keyword" component={Catalog} />
      {/* <Route exact path="/:category/search/:keyword" component={Catalog} /> */}
      <Route exact path="/:category/:id" component={Detail} />
      <Route exact path="/:category" component={Catalog} />
      <Route exact path="/" exact component={Home} />
    </Switch>
  );
};

export default Routes;
