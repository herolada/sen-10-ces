import { Outlet, Link } from "react-router-dom";
import '../common.css';

/* function postLanguage(props) {
    useEffect(()=>{
        fetch('http://localhost:5000/language/',{
          'methods':'POST',
          headers : {
            'Content-Type':'application/json'
          },
          body : {
            'language': {props.language}
          },
        })
        .then(response => response.json())  
        .then(response => setRemaining(response['remaining']))
        .catch(error => console.log(error))
    
      },[])
} */


export default function Language() {
  return (
    <div className="center-screen">
        <Link 
            className="btn btn-custom"
            role="button"
            to="/translate_init"
            state={{language:"german"}}
          > 
            German
          </Link>
        
          <Link 
            className="btn btn-custom"
            role="button"
            to="/translate_init"
            state={{language:"czech"}}
          > 
            Czech
          </Link>
    </div>
  );
}
