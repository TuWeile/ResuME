import React from "react";
import './homepage.css';

interface ThreeSegmentLayoutProps {
    leftRatio: number;
    midRatio: number;
    rightRatio: number;
}

const ThreeSegmentLayout: React.FC<ThreeSegmentLayoutProps> = ({leftRatio, midRatio, rightRatio}) => {
    return (
        <div className="container" style={{flex: leftRatio}}>
            <div className="left-segment">
                Navigation menu
            </div>
            <div className="mid-segment" style={{flex:midRatio}}>
                <div className="taskbar">
                    WhatsApp like front goes here
                </div>
                <div className="chatbot">
                    Chatbot goes here
                </div>
            </div>
            <div className="right-segment" style={{flex:rightRatio}}>
                Profile goes here
            </div>
        </div>
    );
}

export default ThreeSegmentLayout;
