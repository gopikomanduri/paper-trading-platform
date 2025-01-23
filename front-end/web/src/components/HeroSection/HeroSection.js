import React from 'react';
import './HeroSection.css';

const HeroSection = () => {
  return (
    <div className="hero-section">
      <div className="hero-content">
        <h1>Welcome to the Paper Trading Platform!</h1>
        <p>Experience the thrill of trading with zero risk.</p>
        <button className="cta-button">Start Trading Now</button>
      </div>
    </div>
  );
};

export default HeroSection;
