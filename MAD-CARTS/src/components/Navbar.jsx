import React from 'react';
import { Link } from 'react-router-dom';
import { FaShoppingCart, FaUser, FaPalette } from 'react-icons/fa';
import './styles/navbar.css';

const Navbar = () => {
  const [isLoggedIn, setIsLoggedIn] = React.useState(false);
  const [cartCount, setCartCount] = React.useState(0);

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          MarketPlace
        </Link>
        
        <ul className="nav-menu">
          <li className="nav-item">
            <Link to="/products" className="nav-links">
              Browse
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/design-preview" className="nav-links">
              <FaPalette className="nav-icon" />
              Designs
            </Link>
          </li>
          {!isLoggedIn ? (
            <>
              <li className="nav-item">
                <Link to="/login" className="nav-links">
                  Login
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/register" className="nav-links">
                  Register
                </Link>
              </li>
            </>
          ) : (
            <>
              <li className="nav-item">
                <Link to="/dashboard" className="nav-links">
                  <FaUser className="nav-icon" />
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/cart" className="nav-links">
                  <FaShoppingCart className="nav-icon" />
                  {cartCount > 0 && <span className="cart-badge">{cartCount}</span>}
                </Link>
              </li>
              <li className="nav-item">
                <button 
                  className="nav-links logout-btn"
                  onClick={() => setIsLoggedIn(false)}
                >
                  Logout
                </button>
              </li>
            </>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;