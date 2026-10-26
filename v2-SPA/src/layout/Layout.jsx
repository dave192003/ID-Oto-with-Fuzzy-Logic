
import NavBar from "../components/navBar/navBar";
import "./main-layout.css";

function MainLayout({ children }) {
  return (
    <div className="main-layout">
      <NavBar />

      <main className="main-layout">
        {children}
      </main>

    </div>
  );
}

export default MainLayout;
