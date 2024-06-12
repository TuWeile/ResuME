import React, { useState, useEffect } from 'react';
import './App.css';
import ThreeSegmentLayout from './frontend/homepage';
import PopupWindow from './frontend/popup';
import LoadingScreen from './frontend/loadingscreen';

interface AppProps {
  prod: boolean;
}

const App: React.FC<AppProps> = ({ prod }) => {
  const [loading, setLoading] = useState(true);
  const [popupVisible, setPopupVisible] = useState(false);
  const [popupShow, setPopupShow] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(false);
      setPopupShow(prod);
      setTimeout(() => {
        setPopupVisible(prod);
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
        {prod && <PopupWindow show={popupVisible} onClose={togglePopup} />}
      </div>
  );
};

export default App;
