import "./landing-page.css";
// icons and images imports
import Arrow from "../../assets/resources/icons/arrow.png";
import Crop from "../../assets/resources/icons/crop.png";
import Dashboard from "../../assets/resources/icons/dashboard.png";
import imageUpload from "../../assets/resources/icons/image-.png";
import MagicWand from "../../assets/resources/icons/magic-wand.png";
import Magic from "../../assets/resources/icons/magic.png";
import Lock from "../../assets/resources/icons/padlock.png";
import Printer from "../../assets/resources/icons/printer.png";
import IDs from "../../assets/resources/images/id-photo.png";
import Image from "../../assets/resources/images/images.jpg";
// import NoBGImage from "../../assets/resources/images/imgBG.jpg";
import { useState } from "react";

function LandingPage() {
    const [buttonText, setButtonText] = useState("Choose file");

    return (
        <main className="landing-page-main">
            {/* Left Section */}
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
                    <div className="upload-area" id="uploadArea">
                        <label htmlFor="imageInput" className="upload-card" id="file-input" >
                            <div className="upload-icon">
                                <img src={imageUpload} />
                            </div>
                            <h2>Upload Your Photo </h2>
                            <p className="upload-description">Drag &amp; drop or click to upload</p>
                            <span className="choose-file-btn">{buttonText}</span>
                            <p className="file-info">JPG, PNG or JPEG (Max size 10MB)</p>
                        </label>

                        <input
                            type="file"
                            id="imageInput"
                            accept="image/png,image/jpeg"
                            hidden
                            onCancel={() => {
                                setButtonText("Choose File");
                            }}
                            onClick={() => {
                                setButtonText("Choosing File...");
                            }}
                            onChange={() => {
                                setButtonText("Choose File");
                            }}
                        />


                    </div>

                    <div className="privacy-info-container">
                        <img src={Lock} />
                        <p>Photos are secure and private. They are not stored.</p>
                    </div>
                </header>
            </section>

            {/* Right Section */}
            <section className="right-section">
                <div className="hero-image-container">
                    <img src={Image} className="image1" alt="Original photo" />
                    <img src={Arrow} className="arrow" alt="Arrow" />
                    <img src={IDs} className="image2" alt="ID photo" />
                </div>
            </section>

            <section className="feature-info-section">
                <div className="box">
                    <img src={MagicWand} alt="Background removal" />
                    <h3>Auto Background Removal</h3>
                    <span role="tooltip" id="hv-tip-1">Remove the background of image automatically.</span>
                </div>

                <div className="box">
                    <img src={Crop} alt="Cropping" />
                    <h3>Smart Cropping</h3>
                </div>

                <div className="box">
                    <img src={Magic} alt="Enhancement" />
                    <h3>Auto Enhance</h3>
                </div>

                <div className="box">
                    <img src={Dashboard} alt="Layout" />
                    <h3>Auto Layout</h3>
                </div>

                <div className="box">
                    <img src={Printer} alt="Printing" />
                    <h3>Print Ready</h3>
                </div>
            </section>

            <footer class="footer-container">
                <p>&copy; 2026 Dave Daryl Lebico. All Rights Reserved.</p>
            </footer>
        </main>
    );
}

export default LandingPage;


