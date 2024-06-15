import React, {useState, useEffect} from 'react';
import { useLocation, useSearchParams } from 'react-router-dom';
import axios from 'axios';
import './home.css';
import ThreeSegmentLayout from '../homepage';
import PopupWindow from '../popup';
import LoadingScreen from '../loadingscreen';

const API_URL = 'http://localhost:4242/api/chat';

function HomePage() {
    const [loading, setLoading] = useState(true);
    const [popupVisible, setPopupVisible] = useState(false);
    const [popupShow, setPopupShow] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [userData, setUserData] = useState<any>(null);
    const endLocation = useLocation();
    const [searchParams] = useSearchParams();

    useEffect(() => {
        const queryParam = searchParams.get('q');

        if (endLocation.pathname === '/chat' && queryParam) {
            axios.get(`${API_URL}?q=${queryParam}`)
                .then(response => {
                    const {status, user} = response.data;
                    if (status === 'ok') {
                        setUserData(user);
                    } else {
                        setError(`Error: Unable to fetch data. Please try again.`);
                    }
                })
                .catch(error => {
                    setError(`Error: Unable to fetch data. Please try again.`);
                })
                .finally(() => {
                    setLoading(false);
                });
        } else if (endLocation.pathname === '/chat' && !queryParam) {
            setError(`Error: No query parameter provided.`);
            setLoading(false);
        } else {
            const timer = setTimeout(() => {
                setLoading(false);
                setPopupShow(true);
                setTimeout(() => {
                    setPopupVisible(true);
                }, 300);
            }, 6000);

            return () => clearTimeout(timer);
        }
    }, [endLocation.pathname, searchParams]);

    const togglePopup = () => {
      setPopupVisible(!popupVisible);
    };

    if (loading) {
      return <LoadingScreen />;
    }

    if (error) {
        return (
            <div className="App">
                <ThreeSegmentLayout leftRatio={1} midRatio={2.5} rightRatio={0.8} userData={userData} />
                <div className="error-popup">
                    <h2>Error</h2>
                    <p>{error}</p>
                </div>
            </div>
        );
    }

    if (endLocation.pathname === '/chat' && userData) {
        return (
            <div className="App">
                <ThreeSegmentLayout leftRatio={1} midRatio={2.5} rightRatio={0.8} userData={userData} />
                {/*<div className="user-data">*/}
                {/*    /!* Display user data here *!/*/}
                {/*    <pre>{JSON.stringify(userData, null, 2)}</pre>*/}
                {/*</div>*/}
            </div>
        );
    }

    return (
      <div className="App">
        <ThreeSegmentLayout leftRatio={1} midRatio={2.5} rightRatio={0.8} userData={userData} />
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
