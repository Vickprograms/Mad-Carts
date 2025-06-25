import { Link } from 'react-router-dom';
import { FaShoppingCart, FaUser, FaPalette } from 'react-icons/fa';
import '../styles/navbar.css';

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="container">
        <Link to="/" className="logo">Mad Carts</Link>
        <div className="nav-links">
          <Link to="/products">Products</Link>
          <Link to="/design-preview">Design</Link>
          <Link to="/cart"><FaShoppingCart /></Link>
        </div>
      </div>
    </nav>
  );
}