import React, { useState, useEffect } from 'react';
import './popup.css';

interface PopupWindowProps {
    show: boolean;
    onClose: () => void;
    children: React.ReactNode;
}

const PopupWindow: React.FC<PopupWindowProps> = ({ show, onClose, children }) => {
    const [isVisible, setIsVisible] = useState(show);

    useEffect(() => {
        if (show) {
            setIsVisible(true);
        } else {
            const timer = setTimeout(() => setIsVisible(false), 300);
            return () => clearTimeout(timer);
        }
    }, [show]);

    if (!isVisible) return null;

    return (
        <div className={`popup-overlay ${show ? 'fade-in' : 'fade-out'}`}>
            <div className={`popup-content ${show ? 'fade-in' : 'fade-out'}`}>
                <button className="close-button" onClick={onClose}>×</button>
                {children}
            </div>
        </div>
    );
};

export default PopupWindow;
