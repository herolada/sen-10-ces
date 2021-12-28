import { Outlet, Link } from "react-router-dom";
import { useLocation, useOutletContext } from 'react-router-dom';
import { useEffect, useReducer, useRef  } from 'react';
import ReactDOM from 'react-dom';
import useState from 'react-usestateref';
import '../common.css';




export default function Translate(props) {
  //const location = useLocation()
  //const language = location.state.language
  const [refresh, setRefresh] = useState(0);
  const [sentence, setSentence, currentSentence] = useState({text:"", id:0});
  const [correctTranslation, setCorrectTranslation] = useState("");
  const [score, setScore] = useState(0.0);
  const [showButtons, setShowButtons] = useState(false);
  const [showGoAgain, setShowGoAgain] = useState(false);
  const [showGlitter, setShowGlitter] = useState(false);
  const [setParentRemaining] = useOutletContext();
  const [remaining, setRemaining, counterRef] = useState([]);
  const textRef = useRef(null);

  function submitOnEnter(event){
    if(event.which === 13){
        postTranslation(event);
        event.preventDefault(); // Prevents the addition of a new line in the text field (not needed in a lot of cases)
    }
  }

  let nextSentence = () => {
    fetch('http://localhost:5000/next_sentence/',{
      method: 'GET',
      headers : {
        'Content-Type':'application/json'
      }
    })
    .then(response => response.json())
    .then(response => setSentence({text: response['sentence'], id: response['id']}))
    .then(() => currentSentence.current['id'] > 10 ? setShowGoAgain(true) : {} )
    .catch(error => console.log(error));
    setShowGlitter(false);
    setShowButtons(false);
  }


  const handleChange = accept => async e => {
    const resp = await fetch(`http://localhost:5000/confirm/${sentence['id']}/${accept}`,{
      method : 'POST',
      headers : {
        'Content-Type':'application/json'
      }
    });

    const resp2 = await fetch('http://localhost:5000/remaining/',{
      'methods':'GET',
      headers : {
        'Content-Type':'application/json'
      }
    })
    .then(response => response.json())  
    .then(response => setRemaining(response['remaining']))
    .then(() => setParentRemaining(counterRef.current))
    .catch(error => console.log(error));
    textRef.current.value = '';
    nextSentence();
  };

  const handleGoAgain = setter => e => {
    setShowGoAgain(setter);
  };

  const buttons = <div>
                    <button type="button" className="btn btn-yes" onClick={handleChange(true)} >✓</button>
                    <button type="button" className="btn btn-no" onClick={handleChange(false)} >✕</button>
                  </div>;
  
  const goAgain = <div>
                    <Link className="btn btn-dark" role="button" to="/language" onClick={handleGoAgain(false)}>Let's go again!</Link>
                  </div>;

  async function postTranslation(e) {
    e.preventDefault();
    
    var translation = ""
    try {
      translation = e.target.translation.value;
    } catch(error) {
      translation = e.target.value;
    }

    console.log(translation);
  
    const resp1 = await fetch(`http://localhost:5000/translations/${sentence['id']}`,{
      method : 'POST',
      headers : {
        'Content-Type':'application/json'
      },
      body : JSON.stringify({
        translation:translation
      })
    });

    const resp2 = await fetch(`http://localhost:5000/correct_translations/${sentence['id']}`,{
      method : 'GET',
      headers : {
        'Content-Type':'application/json'
      },
    })
    .then(response => response.json())
    .then(response => setCorrectTranslation(response['correct_translation']));
    
    const resp3 = await fetch(`http://localhost:5000/text_comparison/${sentence['id']}`,{
      method : 'GET',
      headers : {
        'Content-Type':'application/json'
      },
    })
    .then(response => response.json())
    .then(response => setScore(response['score']))
    .then(() => setShowGlitter(true))
    .then(() => setShowButtons(true));    
  }

  useEffect(
    nextSentence
    ,[]);

  return (
    <div className = "center-screen side-borders">
      <div>
        <p className="sentence">{sentence['text']}</p>
      </div>
      <div>
        <form onSubmit={postTranslation}>
            <textarea className="text-area" onKeyPress={submitOnEnter} id="translation" name="translation" ref={textRef}/>
          {/* <input type="submit" value="Submit" /> */}
        </form>
      </div>
      <div>
        <p className="sentence">{showGlitter ? correctTranslation : null}</p>
      </div>
      <div>
        <p className="small-sentence">{showGlitter ? score : null}</p>
      </div>
      <div>
        {showButtons ? buttons : null}
      </div>
      <div>
        {showGoAgain ? goAgain : null}
      </div>
    </div>
  );
}
