import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import './common.css';
import App from './App';
import Translate from "./routes/translate";
import TranslateInit from "./routes/translate_init";
import Language from "./routes/language";

import reportWebVitals from './reportWebVitals';
import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";  
import { render } from "react-dom";
import { Outlet, Link } from "react-router-dom";

const rootElement = document.getElementById("root");
render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<App />}>
        <Route path="/language" element={<Language />} />
        <Route path="/translate" element={<Translate />} />
        <Route path="/translate_init" element={<TranslateInit/>}/>
        <Route
          path="/"
          element={
            <Link 
              className="btn btn-custom center-screen"
              role="button"
              to="/language"
            > 
              Let's go!
            </Link>

          }
        />  
        <Route
          path="*"
          element={
            <Link 
            className="btn btn-custom center-screen"
            role="button"
            to="/language"
            > 
              Let's go!
            </Link>

          }
        />
      </Route>
    </Routes>
  </BrowserRouter>,
  rootElement
);

reportWebVitals();
