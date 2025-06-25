
import React from 'react';
import { Link } from 'react-router-dom';
import { FaShoppingCart, FaStar } from 'react-icons/fa';
import './styles/product.css';

const ProductCard = ({ product }) => {
  const [isInCart, setIsInCart] = React.useState(false);

  const handleAddToCart = () => {
    setIsInCart(true);
    
  };

  return (
    <div className="product-card">
      <div className="product-image">
        <img src={product.image} alt={product.name} />
        <button 
          className={`add-to-cart ${isInCart ? 'in-cart' : ''}`}
          onClick={handleAddToCart}
        >
          <FaShoppingCart />
          {isInCart ? 'Added!' : 'Add to Cart'}
        </button>
      </div>
      <div className="product-info">
        <h3 className="product-name">
          <Link to={`/products/${product.id}`}>{product.name}</Link>
        </h3>
        <div className="product-price">${product.price.toFixed(2)}</div>
        <div className="product-rating">
          {[...Array(5)].map((_, i) => (
            <FaStar 
              key={i} 
              className={i < product.rating ? 'star-filled' : 'star-empty'} 
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default ProductCard;