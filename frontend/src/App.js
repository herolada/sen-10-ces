import './App.css';
import './common.css';
import { useState,useEffect } from 'react';
import { Outlet, Link } from "react-router-dom";

/* export default function App() {
  return (
    <div>
      <h1>Bookkeeper</h1>
      <nav
        style={{
          borderBottom: "solid 1px",
          paddingBottom: "1rem"
        }}
      >
        <Link to="/invoices">Invoices</Link> |{" "}
        <Link to="/expenses">Expenses</Link>
      </nav>
      <Outlet />
    </div>
  );
} */

function App() {
  const [remaining, setRemaining] = useState([]);

  const updateRemaining = () => {
    fetch('http://localhost:5000/remaining/',{
      'methods':'GET',
      headers : {
        'Content-Type':'application/json'
      }
    })
    .then(response => response.json())  
    .then(response => setRemaining(response['remaining']))
    .catch(error => console.log(error))
  }

  useEffect(()=>{
    updateRemaining();
  },[])

  return (
    <div className="App">
      <h1>Sen-</h1><h1 id="remaining">{remaining}</h1><h1>-ces</h1>
    <Outlet context={[setRemaining]}/>
    </div>
  );
}

export default App;
