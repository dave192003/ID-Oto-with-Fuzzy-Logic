import { analyzeImage } from "./js/api.js";

/**
 * Initialize the fuzzy analysis page.
 * Checks for stored data from the main page, or sets up
 * the file upload handler for direct image uploads.
 */
function init() {
    console.log("🔥 fuzzy-analysis.js loaded");

    // Check if there's stored data from the main page
    checkForStoredData();

    // Set up file upload handler for direct image uploads
    const analysisImageInput = document.getElementById("analysisImageInput");
    if (analysisImageInput) {
        analysisImageInput.addEventListener("change", handleFileUpload);
    }
}

/**
 * Handle direct file upload on the fuzzy analysis page.
 */
async function handleFileUpload(event) {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
        const analysisUpload = document.getElementById("analysisUpload");
        const analysisContent = document.getElementById("analysisContent");
        const analysisLoading = document.getElementById("analysisLoading");
        const analysisError = document.getElementById("analysisError");

        // Show loading state
        if (analysisUpload) analysisUpload.classList.add("done");
        if (analysisContent) analysisContent.classList.add("active");
        if (analysisLoading) analysisLoading.classList.add("active");
        if (analysisError) analysisError.hidden = true;

        // Call the analysis API
        const analysis = await analyzeImage(file);

        // Populate the UI with results
        populateStatistics(analysis);
        populateParameters(analysis.parameters);
        populateRules(analysis.fired_rules);
        populateComparison(analysis);

        // Hide loading
        if (analysisLoading) analysisLoading.classList.remove("active");

        console.log("✅ Fuzzy analysis complete for uploaded file");
    } catch (error) {
        console.error("❌ Error analyzing uploaded image:", error);
        const analysisLoading = document.getElementById("analysisLoading");
        const analysisError = document.getElementById("analysisError");
        if (analysisLoading) analysisLoading.classList.remove("active");
        if (analysisError) analysisError.hidden = false;
    }
}

/**
 * Convert a data URL (base64) to a Blob.
 */
function dataURLToBlob(dataURL) {
    const parts = dataURL.split(",");
    const mimeMatch = parts[0].match(/:(.*?);/);
    if (!mimeMatch) return null;
    const mime = mimeMatch[1];
    const byteString = atob(parts[1]);
    const ab = new ArrayBuffer(byteString.length);
    const ia = new Uint8Array(ab);
    for (let i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    return new Blob([ab], { type: mime });
}

/**
 * Check for stored processed image data from the main page,
 * then call the analysis API and populate the UI.
 */
async function checkForStoredData() {
    const hasProcessedImage = sessionStorage.getItem("hasProcessedImage");
    if (hasProcessedImage !== "true") return;

    try {
        const originalImageBase64 = sessionStorage.getItem("originalImage");
        const processedImageBase64 = sessionStorage.getItem("processedImage");

        if (!processedImageBase64) return;

        const analysisOriginalImage = document.getElementById("analysisOriginalImage");
        const analysisProcessedImage = document.getElementById("analysisProcessedImage");
        const analysisUpload = document.getElementById("analysisUpload");
        const analysisContent = document.getElementById("analysisContent");
        const analysisLoading = document.getElementById("analysisLoading");
        const analysisError = document.getElementById("analysisError");

        // Load original image if available
        if (originalImageBase64 && analysisOriginalImage) {
            analysisOriginalImage.src = originalImageBase64;
            await new Promise((resolve, reject) => {
                analysisOriginalImage.onload = resolve;
                analysisOriginalImage.onerror = reject;
            });
        }

        // Convert the processed image data URL to a File
        const blob = dataURLToBlob(processedImageBase64);
        if (!blob) {
            throw new Error("Failed to convert data URL to blob");
        }
        const processedFile = new File([blob], "processed-image.png", { type: "image/png" });
        const processedUrl = URL.createObjectURL(blob);

        // Load processed image preview
        if (analysisProcessedImage) {
            analysisProcessedImage.src = processedUrl;
            await new Promise((resolve, reject) => {
                analysisProcessedImage.onload = resolve;
                analysisProcessedImage.onerror = reject;
            });
        }

        // Show upload as done and content as active
        if (analysisUpload) analysisUpload.classList.add("done");
        if (analysisContent) analysisContent.classList.add("active");
        if (analysisLoading) analysisLoading.classList.add("active");
        if (analysisError) analysisError.hidden = true;

        // Call the analysis API with the processed image
        const analysis = await analyzeImage(processedFile);

        // Populate the UI
        populateStatistics(analysis);
        populateParameters(analysis.parameters);
        populateRules(analysis.fired_rules);
        populateComparison(analysis);

        // Hide loading
        if (analysisLoading) analysisLoading.classList.remove("active");

        // Clean up sessionStorage
        sessionStorage.removeItem("originalImage");
        sessionStorage.removeItem("processedImage");
        sessionStorage.removeItem("photoSize");
        sessionStorage.removeItem("hasProcessedImage");

        console.log("✅ Fuzzy analysis complete");
    } catch (error) {
        console.error("❌ Error loading stored data:", error);
        const analysisLoading = document.getElementById("analysisLoading");
        const analysisError = document.getElementById("analysisError");
        if (analysisLoading) analysisLoading.classList.remove("active");
        if (analysisError) analysisError.hidden = false;
    }
}

/**
 * Populate the statistics section with original and processed image features.
 */
function populateStatistics(analysis) {
    const orig = analysis.original_features || {};
    const proc = analysis.processed_features || {};

    setText("origBrightness", orig.brightness != null ? orig.brightness.toFixed(2) : "-");
    setText("origContrast", orig.contrast != null ? orig.contrast.toFixed(2) : "-");
    setText("origSharpness", orig.sharpness != null ? orig.sharpness.toFixed(2) : "-");
    setText("origNoise", orig.noise != null ? orig.noise.toFixed(2) : "-");

    setText("procBrightness", proc.brightness != null ? proc.brightness.toFixed(2) : "-");
    setText("procContrast", proc.contrast != null ? proc.contrast.toFixed(2) : "-");
    setText("procSharpness", proc.sharpness != null ? proc.sharpness.toFixed(2) : "-");
    setText("procNoise", proc.noise != null ? proc.noise.toFixed(2) : "-");
}

/**
 * Populate the enhancement parameters section.
 */
function populateParameters(params) {
    if (!params) return;

    setText("paramAlpha", params.alpha != null ? params.alpha.toFixed(4) : "-");
    setText("paramBeta", params.beta != null ? params.beta.toFixed(4) : "-");
    setText("paramSharpen", params.sharpen != null ? params.sharpen.toFixed(4) : "-");
    setText("paramDenoise", params.denoise != null ? params.denoise.toFixed(4) : "-");
}

/**
 * Populate the fired rules section.
 */
function populateRules(rules) {
    const container = document.getElementById("rulesContainer");
    if (!container) return;

    if (!rules || rules.length === 0) {
        container.innerHTML = '<p class="no-rules">No rules fired.</p>';
        return;
    }

    container.innerHTML = "";
    rules.forEach((rule) => {
        const card = document.createElement("div");
        card.className = "rule-card";

        const header = document.createElement("div");
        header.className = "rule-header";

        const title = document.createElement("h3");
        title.textContent = `Rule ${rule.id}`;

        const badge = document.createElement("span");
        badge.className = "activation-badge";
        badge.textContent = `${(rule.activation * 100).toFixed(1)}%`;

        header.appendChild(title);
        header.appendChild(badge);

        const desc = document.createElement("p");
        desc.className = "rule-description";
        desc.textContent = rule.description;

        const bar = document.createElement("div");
        bar.className = "activation-bar";

        const fill = document.createElement("div");
        fill.className = "activation-fill";
        fill.style.width = `${(rule.activation * 100).toFixed(1)}%`;

        bar.appendChild(fill);

        card.appendChild(header);
        card.appendChild(desc);
        card.appendChild(bar);

        container.appendChild(card);
    });
}

/**
 * Populate the comparison table with before/after data.
 */
function populateComparison(analysis) {
    const orig = analysis.original_features || {};
    const proc = analysis.processed_features || {};

    const features = ["Brightness", "Contrast", "Sharpness", "Noise"];
    const keys = ["brightness", "contrast", "sharpness", "noise"];

    keys.forEach((key, index) => {
        const origVal = orig[key];
        const procVal = proc[key];

        const origStr = origVal != null ? origVal.toFixed(2) : "-";
        const procStr = procVal != null ? procVal.toFixed(2) : "-";

        setText(`cmpOrig${features[index]}`, origStr);
        setText(`cmpProc${features[index]}`, procStr);

        if (origVal != null && procVal != null) {
            const change = procVal - origVal;
            const pctChange = origVal !== 0 ? ((change / origVal) * 100) : 0;

            setText(`cmpChange${features[index]}`, (change >= 0 ? "+" : "") + change.toFixed(2));
            setText(`cmpPct${features[index]}`, (pctChange >= 0 ? "+" : "") + pctChange.toFixed(2) + "%");
        } else {
            setText(`cmpChange${features[index]}`, "-");
            setText(`cmpPct${features[index]}`, "-");
        }
    });
}

/**
 * Helper to set text content of an element by ID.
 */
function setText(id, text) {
    const el = document.getElementById(id);
    if (el) {
        el.textContent = text;
    }
}

// Initialize when the DOM is ready
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
} else {
    init();
}