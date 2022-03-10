import React from "react";
import { GoogleLogout } from "react-google-login";

const clientId =
  "766782824770-ggibhlciuo3gcc39piu75a5kq92ft9jk.apps.googleusercontent.com";

function Logout() {
  const onSuccess = () => {
    alert("Logout made successfully ✌");
  };

  return (
    <div>
      <GoogleLogout
        clientId={clientId}
        buttonText="Logout"
        onLogoutSuccess={onSuccess}
      ></GoogleLogout>
    </div>
  );
}

export default Logout;
