
import { Outlet } from "react-router-dom";
import NavBar from "../components/navBar/navBar";
import "./main-layout.css";

function MainLayout() {
  return (
    <div className="main-layout">
      <NavBar />
      <Outlet />
    </div>
  );
}

export default MainLayout;
