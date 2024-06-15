// src/Chatbot.tsx
import React, { useState, ChangeEvent, KeyboardEvent, FC, CSSProperties } from 'react';
import axios from 'axios';

interface Message {
  text: string;
  sender: 'bot' | 'user';
}

const Chatbot: FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    { text: 'Hello! How can I help you today?', sender: 'bot' }
  ]);
  const [input, setInput] = useState<string>('');
  const url=window.location.href.split('=')
  const lenurl=url.length-1
  const q=url[lenurl]


  const backend_service_name="localhost"
  const backendUrl='http://'+backend_service_name+':4242/api/prompt_response'




  const handleSend = async () => {
    if (input.trim() !== '') {
      const userMessage: Message = { text: input, sender: 'user' };
      setMessages([...messages, userMessage]);
      setInput('');

      try {
        const response = await axios.post('http://127.0.0.1:4242/api/prompt_response', {
          q: q.toString(),
          prompt: input,
        });

        const botMessage: Message = { text: response.data.output, sender: 'bot' };
        setMessages((prevMessages) => [...prevMessages, botMessage]);
      } catch (error) {
        console.error('Error sending message to the backend:', error);
        const botErrorMessage: Message = { text: 'Sorry, there was an error processing your message.', sender: 'bot' };
        setMessages((prevMessages) => [...prevMessages, botErrorMessage]);
      }
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
              ...styles.messageContainer,
              ...(message.sender === 'bot' ? styles.botMessageContainer : styles.userMessageContainer)
            }}
          >
            <div
              style={{
                ...styles.message,
                ...(message.sender === 'bot' ? styles.botMessage : styles.userMessage)
              }}
            >
              {message.text}
            </div>
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
        {/*<button onClick={handleSend} style={styles.sendButton}>*/}
        {/*  Send*/}
        {/*</button>*/}
      </div>
    </div>
  );
};

const styles: { [key: string]: CSSProperties } = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    width: '100%',
    height: '100%',

  },
  chatWindow: {
    flex: 1,
    padding: '10px',

  },
  messageContainer: {
    display: 'flex',
    marginBottom: '10px',
    width: '100%',
  },
  botMessageContainer: {
    justifyContent: 'flex-start',
  },
  userMessageContainer: {
    justifyContent: 'flex-end',
  },
  message: {
    padding: '10px',
    borderRadius: '4px',
    display: 'inline-block',
    maxWidth: '80%',
    wordWrap: 'break-word', // Wrap long words
  },
  botMessage: {
    backgroundColor: 'rgba(224,224,224,255)',
    borderRadius: '12px 12px 12px 4px',
  },
  userMessage: {
    backgroundColor: 'rgba(0,0,0,255)',
    color: 'white',
    textAlign: 'right',
    borderRadius: '12px 12px 4px 12px',
  },
  inputContainer: {
    display: 'flex',

  },
  input: {
    flex: 1,


    borderTop: '1px solid #ccc',
    borderRadius: '4px',
    height: "100%",
    border: '3px solid #E0E0E0',
  },
  sendButton: {

    border: 'none',
    backgroundColor: '#0084ff',
    color: 'white',
    cursor: 'pointer',
    height: "100%"
  },
};

export default Chatbot;
