import React from "react";
import {useNavigate} from 'react-router-dom';
import './homepage.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import Chatbot from "./component/chatbot_component";


interface ThreeSegmentLayoutProps {
    leftRatio: number;
    midRatio: number;
    rightRatio: number;
    userData: any;
}

const ThreeSegmentLayout: React.FC<ThreeSegmentLayoutProps> = ({leftRatio, midRatio, rightRatio, userData}) => {
    const navigate = useNavigate();

    const handleCreateBotClick = () => {
        navigate('/');
        window.location.reload();
    };

    return (
        <div className="container">
            <div className="left-segment" style={{flex: leftRatio}}>
                <div className="left-header">
                    <img src="/logo.png" alt="Logo" className="logo-corner" />
                    <h1 className="title">Resume Chatbot</h1>
                </div>
                <div className="search-chat">
                    <div className="search-chat-container">
                        <button className="search-chat-button">
                            <i className="fas fa-search"></i>
                        </button>
                        <input type="text" placeholder="Search chats..." className="search-chat-input" />
                    </div>
                </div>
                <div className="chat-list">
                    {userData && (
                        <div className="chat-entry">
                            <img src="/avatar.png" alt="Avatar" className="avatar" />
                            <div className="chat-details">
                                <p className="user-name">{userData.personalInfo.first_name} {userData.personalInfo.last_name}</p>
                                <p className="chat-message">This is a placeholder message from the chatbot.</p>
                            </div>
                        </div>
                    )}
                </div>
                <div className="create-bot-container">
                    <button className="create-bot-button" onClick={handleCreateBotClick}>
                        Create Bot
                    </button>
                </div>
                {/* Add more content here if needed */}
            </div>
            <div className="mid-segment" style={{flex: midRatio}}>
                <div className="taskbar">
                    WhatsApp like front goes here
                </div>
                <div className="chatbot">
                    <Chatbot/>
                </div>
            </div>
            <div className="right-segment" style={{flex: rightRatio}}>
                Profile goes here
            </div>
        </div>
    );
}

export default ThreeSegmentLayout;
