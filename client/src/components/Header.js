import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

const Header = () => {
  return (
    <header className="header">
      <div className="header-container">
        <div className="logo">
          <Link to="/">
            <h1>RecipeIQ</h1>
          </Link>
        </div>
        <nav className="navigation">
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/upload">Upload Image</Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header; 