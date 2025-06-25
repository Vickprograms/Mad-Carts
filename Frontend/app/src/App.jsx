
import { BrowserRouter as Router } from 'react-router-dom';
import Navbar from './components/Navbar';
import AppRoutes from './Routes';
import Footer from './components/Footer';
import './styles/main.css';


function App() {
  return (
    <Router>
      <div className="app">
        <Navbar />
        <main>
          <AppRoutes />
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;