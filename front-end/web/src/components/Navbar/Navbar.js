import React from 'react';
import './Navbar.css';

const Navbar = () => {
    return (
        <nav className="navbar">
            <div className="navbar-container">
                <h2 className="navbar-title">Paper Trading Platform</h2>
                <ul className="navbar-links">
                    <li><a href="/" className="navbar-link">Home</a></li>
                    <li><a href="/chart" className="navbar-link">Chart</a></li>
                    <li><a href="/history" className="navbar-link">Order History</a></li>
                </ul>
            </div>
        </nav>
    );
};

export default Navbar;
