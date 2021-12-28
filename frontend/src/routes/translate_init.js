import { Outlet, Link } from "react-router-dom";
import { useLocation } from 'react-router-dom';
import { useState,useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import '../common.css';
import Loader from "react-loader-spinner";


export default function TranslateInit(props) {
  const location = useLocation();
  let navigate = useNavigate();
  const language = location.state.language;

  const handleUseEffect = async () => {
    const kms = await fetch('http://localhost:5000/languages/',{
      method : 'POST',
      headers : {
        'Content-Type':'application/json'
      },
      body : JSON.stringify({
        language:language
      })
    })
    .then(response => response.json())
    .then(response => console.log(response['done']))
    .catch(error => console.log(error));
    navigate("/translate");
  }

  useEffect(
    handleUseEffect
  ,[]);

  return (
    <div className="center-screen"><Loader
    type="Puff"
    color="#DAFEB7"
    height={200}
    width={200}
    timeout={5000} //3 secs
    /></div>
  );
}
