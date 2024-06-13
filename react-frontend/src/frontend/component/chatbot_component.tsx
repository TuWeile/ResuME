// src/Chatbot.tsx
import React, { useState, ChangeEvent, KeyboardEvent, FC, CSSProperties, useEffect } from 'react';

interface Message {
  text: string;
  sender: 'bot' | 'user';
}


const Chatbot: FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    { text: 'Hello! How can I help you today?', sender: 'bot' }
  ]);
  const [input, setInput] = useState<string>('');
  const url=window.location.href.split('/')
  const lenurl=url.length-1
  const uniqueurl=url[lenurl]



//   useEffect()
// use useeffect to handle the loading of informaiton and make initial api call to get use info

  const handleSend = () => {
    if (input.trim() !== '') {
      setMessages([...messages, { text: input, sender: 'user' }]);
      setInput('');

      // Simulate a bot response
      // replace with api call
      setTimeout(() => {
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: 'This is a static response from the bot.', sender: 'bot' }
        ]);
      }, 1000);
    }
  };

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.chatWindow}>
        {messages.map((message, index) => (
          <div
            key={index}
            style={{
              ...styles.message,
              ...(message.sender === 'bot' ? styles.botMessage : styles.userMessage)
            }}
          >
            {message.text}
          </div>
        ))}
      </div>
      <div style={styles.inputContainer}>
        <input
          type="text"
          value={input}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          style={styles.input}
        />
        <button onClick={handleSend} style={styles.sendButton}>
          Send
        </button>
      </div>
    </div>
  );
};

const styles: { [key: string]: CSSProperties } = {
  container: {
    backgroundColor:'',
    display: 'flex',
    flexDirection: 'column',
    width: '100%',
    height: '100%',

    overflow: 'hidden',
  },
  chatWindow: {
    flex: 1,
    padding: '10px',
    overflowY: 'scroll',
  },
  message: {
    padding: '10px',
    margin: '5px 0',
    borderRadius: '4px',
    maxWidth: '80%',
  },
  botMessage: {
    backgroundColor: '#f1f0f0',
    alignSelf: 'flex-start',
  },
  userMessage: {
    backgroundColor: '#0084ff',
    color: 'white',
    alignSelf: 'flex-end',
  },
  inputContainer: {
    display: 'flex',
    borderTop: '1px solid #ccc',
  },
  input: {
    flex: 1,
    padding: '10px',
    border: 'none',
    borderTop: '1px solid #ccc',
  },
  sendButton: {
    padding: '10px',
    border: 'none',
    backgroundColor: '#0084ff',
    color: 'white',
    cursor: 'pointer',
  },
};

export default Chatbot;
