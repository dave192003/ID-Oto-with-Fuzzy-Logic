import "./landing-page.css";
import NavBar from "../../components/navBar/navBar";
function LandingPage() {
  return (
    <>
      {/* Left Section */}
      <NavBar />
      <section className="left-section">
        <header className="header-container">
          <div className="top-header-container">
            <div className="marquee-track">
              <div className="marquee-group">
                <span className="marquee-item">AI Powered</span>
                <span className="marquee-item">Fast</span>
                <span className="marquee-item">Easy to Use</span>
              </div>

              <div className="marquee-group" aria-hidden="true">
                <span className="marquee-item">AI Powered</span>
                <span className="marquee-item">Fast</span>
                <span className="marquee-item">Easy to Use</span>
              </div>
            </div>
          </div>

          <h1 className="name-header">ID-Oto</h1>
          <h2>Automated ID Photo Processor</h2>

          <h3>
            MAKE Your Printing ID Service{" "}
            <span className="easier">EASIER</span>
          </h3>

          <div className="info-header">
            <p>
              Upload a photo and let ID-Oto automatically remove the
              background, crop, and generate ID photos for you.
            </p>
          </div>

          {/* UPLOAD AREA */}
            <div className ="upload-area" id="uploadArea">
                <label for="imageInput" className="upload-card" id="file-input">
                    <div className ="upload-icon">

                    </div>
                    <h2>Upload Your Photo</h2>
                    <p className ="upload-description">Drag &amp; drop or click to upload</p>
                    <span className ="choose-file-btn">Choose File</span>
                    <p className ="file-info">JPG, PNG or JPEG • Max size 10MB</p>
                </label>
                <input
                    type="file"
                    id="imageInput"
                    accept="image/png,image/jpeg,image/jpg"
                    hidden
                />
            </div>

            <div className ="privacy-info-container">
                <p>Your photos are secure and private. They are not stored.</p>
            </div>

        </header>
      </section>
    </>
  );
}

export default LandingPage;
