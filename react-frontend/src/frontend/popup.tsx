// src/PopupWindow.tsx
import React, { useState, useEffect } from 'react';
import './popup.css';
import MultiStepForm from './form';

interface PopupWindowProps {
  show: boolean;
  onClose: () => void;
  title?: string;
}

const PopupWindow: React.FC<PopupWindowProps> = ({ show, onClose, title }) => {
  const [visible, setVisible] = useState(show);
  const [fadeIn, setFadeIn] = useState(false);

  useEffect(() => {
    if (show) {
      setVisible(true);
      setTimeout(() => {
        setFadeIn(true);
      }, 10);
    } else {
      setFadeIn(false)
      const timer = setTimeout(() => {
        setVisible(false);
      }, 300); // Duration of the fade-out transition
      return () => clearTimeout(timer);
    }
  }, [show]);

  return visible ? (
      <div className={`popup-overlay ${fadeIn ? 'fade-in' : 'fade-out'}`} onClick={onClose}>
        <div className="popup-content" onClick={(e) => e.stopPropagation()}>
          <div className="popup-header">
            <h2>{title}</h2>
            <button className="close-button" onClick={onClose}>×</button>
          </div>
          <div className="popup-body">
            <MultiStepForm onComplete={onClose} />
          </div>
        </div>
      </div>
  ) : null;
};

export default PopupWindow;
