import "./navBar.css";

function Navbar() {
  return (
    <nav className="navBar-container">
      <h2 className="nav-logo">ID-Oto</h2>

      <div className="nav-box">
        <ul>
          <li>
            <a href="#features">Feature</a>
          </li>
          <li>
            <a href="#how-it-works">How it Works</a>
          </li>
          <li>
            <a href="#about">About</a>
          </li>
          <li>
            <a href="#contact">Contact</a>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;
