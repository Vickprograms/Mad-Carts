import { Link } from 'react-router-dom';
import './ProductCard.css';

export default function ProductCard({ product }) {
  return (
    <div className="product-card">
      <Link to={`/products/${product.id}`}>
        <img src={product.image} alt={product.title} />
        <h3>{product.title}</h3>
        <p>${product.price}</p>
        <div className="rating">
          {Array(Math.round(product.rating.rate)).fill().map((_, i) => (
            <span key={i}>★</span>
          ))}
        </div>
      </Link>
      <button className="add-to-cart">Add to Cart</button>
    </div>
  );
}