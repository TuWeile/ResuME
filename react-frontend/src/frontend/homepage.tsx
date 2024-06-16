import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import './homepage.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import Chatbot from "./component/chatbot_component";
import PopupWindow from './component/popup'; // Import the PopupWindow component

interface ThreeSegmentLayoutProps {
    leftRatio: number;
    midRatio: number;
    rightRatio: number;
    userData: any;
}

const ThreeSegmentLayout: React.FC<ThreeSegmentLayoutProps> = ({ leftRatio, midRatio, rightRatio, userData }) => {
    const navigate = useNavigate();
    const [isProfilePopupVisible, setProfilePopupVisible] = useState(false);
    const [isAboutUsPopupVisible, setAboutUsPopupVisible] = useState(false);

    const handleCreateBotClick = () => {
        navigate('/');
        window.location.reload();
    };

    const handleViewProfileClick = () => {
        setProfilePopupVisible(true);
    };

    const handleCloseProfilePopup = () => {
        setProfilePopupVisible(false);
    };

    const handleEmailClick = () => {
        console.log('Email John clicked');
    };

    const handleViewAttachmentsClick = () => {
        console.log('View Attachments clicked');
    };

    const handleMoreOptionsClick = () => {
        console.log('More Options clicked');
    };

    const handleAboutUsClick = () => {
        setAboutUsPopupVisible(true);
    };

    const handleCloseAboutUsPopup = () => {
        setAboutUsPopupVisible(false);
    };

    const formatDate = (unixTimestamp: number) => {
        const date = new Date(unixTimestamp * 1000);
        const options: Intl.DateTimeFormatOptions = { day: '2-digit', month: 'short', year: 'numeric' };
        return date.toLocaleDateString('en-GB', options);
    };

    return (
        <div className="container">
            <div className="left-segment" style={{ flex: leftRatio }}>
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
                    {userData ? (
                        <div className="chat-entry">
                            <img src="/avatar.png" alt="Avatar" className="avatar" />
                            <div className="chat-details">
                                <p className="user-name">{userData.personalInfo.first_name} {userData.personalInfo.last_name}</p>
                                <p className="chat-message">Chat to find out more about me!</p>
                            </div>
                        </div>
                    ) : (
                        <p>No user data available</p>
                    )}
                </div>
                <div className="create-bot-container">
                    <button className="create-bot-button" onClick={handleCreateBotClick}>
                        Create Bot
                    </button>
                </div>
            </div>
            <div className="mid-segment" style={{ flex: midRatio }}>
                <div className="taskbar">
                    {userData ? (
                        <>
                            <div className="taskbar-left">
                                <img src="/avatar.png" alt="Avatar" className="taskbar-avatar" />
                                <div className="taskbar-details">
                                    <p className="taskbar-name">{userData.personalInfo.first_name} {userData.personalInfo.last_name}</p>
                                    <p className="taskbar-date">Created on {formatDate(userData.created_at)}</p>
                                </div>
                            </div>
                            <div className="taskbar-right">
                                <button className="taskbar-icon-button" onClick={handleEmailClick}>
                                    <i className="fas fa-envelope"></i>
                                </button>
                                <button className="taskbar-icon-button" onClick={handleViewAttachmentsClick}>
                                    <i className="fas fa-paperclip"></i>
                                </button>
                                <button className="taskbar-icon-button" onClick={handleMoreOptionsClick}>
                                    <i className="fas fa-user"></i>
                                </button>
                            </div>
                        </>
                    ) : (
                        <>
                            <div className="taskbar-left">
                                <img src="/botface.png" alt="Bot" className="taskbar-avatar" />
                                <div className="taskbar-details">
                                    <p className="taskbar-name">Chatbot Assistant</p>
                                    <p className="taskbar-date">Created to serve humans</p>
                                </div>
                            </div>
                            <div className="taskbar-right">
                                <button className="taskbar-icon-button" onClick={handleEmailClick}>
                                    <i className="fas fa-envelope"></i>
                                </button>
                                <button className="taskbar-icon-button" onClick={handleViewAttachmentsClick}>
                                    <i className="fas fa-paperclip"></i>
                                </button>
                                <button className="taskbar-icon-button" onClick={handleMoreOptionsClick}>
                                    <i className="fas fa-user"></i>
                                </button>
                            </div>
                        </>
                    )}
                </div>
                <div className="chatbot">
                    <Chatbot />
                </div>
            </div>
            <div className="right-segment" style={{ flex: rightRatio }}>
                {userData ? (
                    <div className="profile">
                        <img src="/avatar.png" alt="Avatar" className="profile-avatar" />
                        <p className="profile-name">{userData.personalInfo.first_name} {userData.personalInfo.last_name}</p>
                        <p className="profile-date">Created on {formatDate(userData.created_at)}</p>
                        <button className="view-profile-button" onClick={handleViewProfileClick}>View Profile</button>
                        <button className="profile-action-button" onClick={handleEmailClick}>
                            <i className="fas fa-envelope"></i> E-mail {userData.personalInfo.first_name}
                        </button>
                        <button className="profile-action-button" onClick={handleViewAttachmentsClick}>
                            <i className="fas fa-paperclip"></i> View attachments
                        </button>
                        <button className="profile-action-button" onClick={handleMoreOptionsClick}>
                            <i className="fas fa-ellipsis-h"></i> More options
                        </button>
                    </div>
                ) : (
                    <p>No user data available</p>
                )}
                <div className="about-us-container">
                    <button className="about-us-button" onClick={handleAboutUsClick}>
                        About us
                    </button>
                </div>
            </div>
            {isProfilePopupVisible && (
                <PopupWindow show={isProfilePopupVisible} onClose={handleCloseProfilePopup}>
                    <div className="profile-popup-content">
                        <div className="review-section">
                            <h3>Personal Information</h3>
                            <p><strong>Name:</strong> {userData.personalInfo.first_name} {userData.personalInfo.last_name}</p>
                            <p><strong>Email:</strong> {userData.personalInfo.email}</p>
                            <p><strong>Phone:</strong> {userData.personalInfo.phone}</p>
                            <p><strong>Date of Birth:</strong> {userData.personalInfo.date_of_birth}</p>
                        </div>
                        <div className="review-section">
                            <h3>Address</h3>
                            <p><strong>Street:</strong> {userData.address.street}</p>
                            <p><strong>City:</strong> {userData.address.city}</p>
                            <p><strong>State:</strong> {userData.address.state}</p>
                            <p><strong>Zip:</strong> {userData.address.zip}</p>
                            <p><strong>Country:</strong> {userData.address.country}</p>
                        </div>
                    </div>
                </PopupWindow>
            )}
            {isAboutUsPopupVisible && (
                <PopupWindow show={isAboutUsPopupVisible} onClose={handleCloseAboutUsPopup}>
                    <div className="about-us-popup-content">
                        <p>This submission is done in fulfillment of the requirements for the <a href="https://azurecosmosdb.devpost.com/" target="_blank" rel="noopener noreferrer">Microsoft Developers AI Hackathon 2024</a> in Devpost. Find out more about this project from our <a href={"https://github.com/TuWeile/microsoftHackathon"} target={"_blank"} rel={"noopener noreferrer"}>Github repository</a> here!</p>
                        <div className="about-us-content">
                            <h3>Team members</h3>
                            <ul>
                                <li>Chong Jun Hao <a href={"https://www.linkedin.com/in/xiuqun-cui/"} target={"_blank"} rel={"noopener noreferrer"}><i className="fab fa-linkedin linkedin-icon"></i></a></li>
                                <li>Cui Xiuqun <a href={"https://www.linkedin.com/in/xiuqun-cui/"} target={"_blank"} rel={"noopener noreferrer"}><i className="fab fa-linkedin linkedin-icon"></i></a></li>
                                <li>Tu Weile <a href={"https://www.linkedin.com/in/tuweile/"} target={"_blank"} rel={"noopener noreferrer"}><i className="fab fa-linkedin linkedin-icon"></i></a></li>
                                <li>Yap Wei Xuan <a href={"https://www.linkedin.com/in/yap-wei-xuan-844106158"} target={"_blank"} rel={"noopener noreferrer"}><i className="fab fa-linkedin linkedin-icon"></i></a></li>
                            </ul>
                        </div>
                    </div>
                </PopupWindow>
            )}
        </div>
    );
}

export default ThreeSegmentLayout;
