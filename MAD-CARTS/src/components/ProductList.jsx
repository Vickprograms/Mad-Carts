
import React, { useState, useEffect } from 'react';
import ProductCard from './ProductCard';
import './styles/product.css';

const Products = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [category, setCategory] = useState('all');

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        
        setTimeout(() => {
          const mockProducts = [
            {
              id: 1,
              name: 'Wireless Headphones',
              price: 99.99,
              image: 'https://via.placeholder.com/300',
              category: 'electronics',
              rating: 4
            },
            
          ];
          const filtered = category === 'all' 
            ? mockProducts 
            : mockProducts.filter(p => p.category === category);
          setProducts(filtered);
          setLoading(false);
        }, 800);
      } catch (error) {
        console.error('Error fetching products:', error);
        setLoading(false);
      }
    };

    fetchProducts();
  }, [category]);

  return (
    <div className="products-page">
      <h1>Browse Products</h1>
      
      <div className="filter-section">
        <select 
          value={category} 
          onChange={(e) => setCategory(e.target.value)}
          className="category-filter"
        >
          <option value="all">All Categories</option>
          <option value="electronics">Electronics</option>
          <option value="clothing">Clothing</option>
          <option value="home">Home & Garden</option>
        </select>
      </div>

      {loading ? (
        <div className="loading-spinner">Loading...</div>
      ) : (
        <div className="products-grid">
          {products.length > 0 ? (
            products.map(product => (
              <ProductCard key={product.id} product={product} />
            ))
          ) : (
            <p className="no-products">No products found in this category.</p>
          )}
        </div>
      )}
    </div>
  );
};

export default Products;