import React, {useState, useEffect} from 'react';
import './home.css';
import ThreeSegmentLayout from '../homepage';
import PopupWindow from '../popup';
import LoadingScreen from '../loadingscreen';

function HomePage() {
    const [loading, setLoading] = useState(true);
    const [popupVisible, setPopupVisible] = useState(false);
    const [popupShow, setPopupShow] = useState(false);
  
    useEffect(() => {
      const timer = setTimeout(() => {
        setLoading(false);
        setPopupShow(true);
        setTimeout(() => {
          setPopupVisible(true);
        }, 300);
      }, 6000);
  
      return () => clearTimeout(timer);
    }, []);
  
    const togglePopup = () => {
      setPopupVisible(!popupVisible);
    };
  
    if (loading) {
      return <LoadingScreen />;
    }
  
    return (
      <div className="App">
        <ThreeSegmentLayout leftRatio={1} midRatio={2.5} rightRatio={0.8} />
        <PopupWindow show={popupVisible} onClose={togglePopup}></PopupWindow>
        {/* <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.tsx</code> and save to reload.
          </p>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
        </header> */}
      </div>
    );
  };
  
  export default HomePage;
  