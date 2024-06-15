import React, {useState, useEffect} from 'react';
import './chatbotpage.css';
import ThreeSegmentLayout from '../homepage';
import PopupWindow from '../popup';
import LoadingScreen from '../loadingscreen';
import Chatbot from '../component/chatbot_component';

function ChatBotPage() {



    const leftRatio= 1;
    const midRatio= 2.5;
    const rightRatio= 0.8;

    return (
        <div className="container" style={{flex: leftRatio}}>
            <div className="left-segment">
                Navigation menu
            </div>s
            <div className="mid-segment" style={{flex:midRatio}}>
                <div className="taskbar">
                    WhatsApp like front goes here
                </div>
                <div className="chatbot">
                    <Chatbot/>
                </div>
            </div>
            <div className="right-segment" style={{flex:rightRatio}}>
                Profile goes here
            </div>
        </div>
    );
  };

  export default ChatBotPage;
