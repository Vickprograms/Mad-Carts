
import { Link } from 'react-router-dom';
import '../styles/main.css';

export default function Home() {
  return (
    <div className="home">
      <h1>Welcome to Mad Carts</h1>
      <p>Your ultimate online marketplace</p>
      <Link to="/products" className="btn">
        Browse Products
      </Link>
    </div>
  );
}