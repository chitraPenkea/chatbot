// src/pages/Home.jsx
import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import ChatBot from '../components/ChatBot';
import ChatBotIcon from '../components/ChatBotIcon';


const Home = () => {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const playAudio = () => {
      const audio = new Audio(`http://localhost:8000/${location.state.audio}`);
      audio.play();
    };

    if (location.state && location.state.audio) {
      playAudio();
    }
  }, [location.state]);

  return (
    <div className='home-container'>
      <h2 className='home-title'>Welcome to the Home Page</h2>
      {!isChatOpen && <ChatBotIcon onChat={() => setIsChatOpen(true)} />}
      {isChatOpen && <ChatBot onClose={() => setIsChatOpen(false)} />}
    </div>
  );
};

export default Home;
