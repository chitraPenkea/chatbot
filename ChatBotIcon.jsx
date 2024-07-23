// src/components/ChatBotIcon.jsx
import React from 'react';
import { MdChat } from 'react-icons/md';
import './ChatBotIcon.css';

const ChatBotIcon = ({ onChat }) => (
  <div className="chatbot-icon" onClick={onChat}>
    <MdChat size={32} />
  </div>
);

export default ChatBotIcon;
