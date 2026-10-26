import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import LandingPage from "../src/pages/LandingPage/LandingPage";
import MainLayout from "../src/layout/Layout";
function App(){
  return (
    <Router>
      <Routes>
        <Route element = {<MainLayout />}>
          <Route path = "/" element = {<LandingPage />} />
        </Route>
      </Routes>
    </Router>
  )
}

export default App;