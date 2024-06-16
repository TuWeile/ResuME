import React, { useState, useEffect } from 'react';
import './loadingscreen.css';

const LoadingScreen: React.FC = () => {
    const messages = ["Loading resumes...", "Getting interviewers...", "Scanning attachments...", "Mass-sending applications...", "Dealing with rejections..."];
    const [currentMessageIndex, setCurrentMessageIndex] = useState(0);
    const [fade, setFade] = useState(true);

    useEffect(() => {
        const interval = setInterval(() => {
            setFade(false);
            setTimeout(() => {
                setCurrentMessageIndex((prevIndex) => (prevIndex + 1) % messages.length);
                setFade(true);
            }, 500)
        }, 1200); // Change message every second
    
        return () => clearInterval(interval);
      }, [messages.length]);

    return (
        <div className='loading-screen'>
            <div className='spinner'></div>
            <div className={`loading-message ${fade ? 'fade-in' : 'fade-out'}`}>{messages[currentMessageIndex]}</div>    
        </div>
    )
}

export default LoadingScreen;
