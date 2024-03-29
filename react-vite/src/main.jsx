import React from "react";
import ReactDOM from "react-dom/client";
import { Provider as ReduxProvider } from "react-redux";
// import App from './router/index'
import { RouterProvider } from "react-router-dom";
import { CartProvider } from "./context/CartContext";
import configureStore from "./redux/store";
import { router } from "./router";
import * as sessionActions from "./redux/session";
import "./index.css";

const store = configureStore();

if (import.meta.env.MODE !== "production") {
  window.store = store;
  window.sessionActions = sessionActions;
}

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ReduxProvider store={store}>
    <CartProvider>
      <RouterProvider router={router} />
    </CartProvider>
    </ReduxProvider>
  </React.StrictMode>
);
