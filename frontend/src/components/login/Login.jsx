import React, { useState } from "react";
import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import Tooltip from "@mui/material/Tooltip";

import { GoogleLogin, GoogleLogout, useGoogleLogout } from "react-google-login";
import { useHistory } from "react-router-dom";

// refresh token
import { refreshTokenSetup } from "./refreshToken";
import Logout from "./Logout";
import { __RouterContext } from "react-router";

const clientId =
  "766782824770-ggibhlciuo3gcc39piu75a5kq92ft9jk.apps.googleusercontent.com";

function Login() {
  const history = useHistory();

  const [isLoggedIn, setLoggedIn] = useState(false);
  const [userDetail, setUserDetail] = useState({});

  const onLogoutSuccess = () => {
    setUserDetail({});
    setLoggedIn(false);
  };

  const { signOut } = useGoogleLogout({
    clientId,
    onLogoutSuccess,
  });

  const onSuccess = (res) => {
    refreshTokenSetup(res);
    setLoggedIn(true);
    setUserDetail(res?.profileObj);
  };

  const onFailure = (res) => {
    console.log("Login failed: res:", res);
    alert(`Failed to login. 😢 `);
  };

  const handleLogout = () => {
    signOut();
  };
  const handleRedirect = () => {
    window.open("https://www.google.com/","_blank");

  };
  return (
    <div>
      {isLoggedIn ? (
        <Tooltip
          title={
            <div>
              <Button
                style={{
                  color: "white",
                  textTransform: "none",
                  width: "100px",
                }}
                onClick={handleRedirect}
              >
                Dashboard
              </Button>
              <br />
              <Button
                onClick={handleLogout}
                style={{
                  color: "white",
                  textTransform: "none",
                  paddingLeft: "0px !important",
                  width: "100px",
                }}
              >
                Logout
              </Button>
            </div>
          }
          arrow
        >
          <Avatar alt={userDetail?.name} src={userDetail?.imageUrl} />
        </Tooltip>
      ) : (
        <GoogleLogin
          clientId={clientId}
          buttonText="Login"
          onSuccess={onSuccess}
          onFailure={onFailure}
          cookiePolicy={"single_host_origin"}
          style={{ marginTop: "100px" }}
          isSignedIn={true}
        />
      )}
    </div>
  );
}

export default Login;
