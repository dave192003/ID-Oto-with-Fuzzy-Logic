/**
 * ID-Oto main application script
 *
 * Handles:
 * - Image upload
 * - Original image preview
 * - Calling Flask API
 * - Processed image preview
 * - Print layout
 * - Download
 * - Fuzzy analysis navigation
 */

import { enhanceImage } from "./js/api.js";

console.log("🔥 SCRIPT.JS STARTED");

// ============================================================
// STATE
// ============================================================

let selectedFile = null;
let processedBlob = null;

let processedImageURL = null;
let originalImageURL = null;

let isProcessing = false;


// ============================================================
// DOM ELEMENTS
// ============================================================

const imageInput = document.getElementById("imageInput");
const uploadArea = document.getElementById("uploadArea");
const previewContainer = document.getElementById("previewContainer");

const originalPreview = document.getElementById("originalPreview");
const outputPreview = document.getElementById("outputPreview");

const status = document.getElementById("status");
const processButton = document.getElementById("process-button");

const downloadButton = document.getElementById("download-button");
const printButton = document.getElementById("print-button");
const fuzzyAnalysisButton =
    document.getElementById("fuzzy-analysis-button");

const photoSize = document.getElementById("photoSize");
const printSheet = document.getElementById("printSheet");


// ============================================================
// DOM CHECK
// ============================================================

console.log("===== DOM CHECK =====");

console.log("imageInput:", imageInput);
console.log("uploadArea:", uploadArea);
console.log("previewContainer:", previewContainer);
console.log("originalPreview:", originalPreview);
console.log("outputPreview:", outputPreview);
console.log("status:", status);
console.log("processButton:", processButton);
console.log("downloadButton:", downloadButton);
console.log("printButton:", printButton);
console.log("fuzzyAnalysisButton:", fuzzyAnalysisButton);
console.log("photoSize:", photoSize);
console.log("printSheet:", printSheet);

console.log("=====================");


// ============================================================
// VALIDATE DOM
// ============================================================

const requiredElements = [
    imageInput,
    uploadArea,
    previewContainer,
    originalPreview,
    outputPreview,
    status,
    processButton,
    downloadButton,
    printButton,
    fuzzyAnalysisButton,
    photoSize,
    printSheet
];

if (requiredElements.some((element) => !element)) {

    console.error(
        "❌ One or more required HTML elements are missing."
    );

}


// ============================================================
// PHOTO DIMENSIONS
// ============================================================

const PHOTO_DIMENSIONS = {

    "1x1": {
        width: "1in",
        height: "1in"
    },

    "1.5x1.5": {
        width: "1.5in",
        height: "1.5in"
    },

    "2x2": {
        width: "2in",
        height: "2in"
    },

    "passport": {
        width: "35mm",
        height: "45mm"
    }

};


// ============================================================
// INITIAL UI STATE
// ============================================================

function showUploadState() {

    uploadArea.classList.remove("done");

    previewContainer.classList.remove("active");

}


function showPreviewState() {

    uploadArea.classList.add("done");

    previewContainer.classList.add("active");

}


function resetProcessedState() {

    processedBlob = null;

    if (processedImageURL) {

        URL.revokeObjectURL(
            processedImageURL
        );

        processedImageURL = null;

    }

    outputPreview.removeAttribute("src");

    outputPreview.style.display = "none";

    printSheet.innerHTML = "";

}


function resetOriginalState() {

    if (originalImageURL) {

        URL.revokeObjectURL(
            originalImageURL
        );

        originalImageURL = null;

    }

    originalPreview.removeAttribute("src");

}


// ============================================================
// FILE INPUT
// ============================================================

imageInput.addEventListener(
    "change",
    handleFileSelect
);


// ============================================================
// HANDLE FILE SELECT
// ============================================================

function handleFileSelect(event) {

    console.log("");
    console.log("================================");
    console.log("🔥 HANDLE FILE SELECT");
    console.log("================================");


    const file =
        event.target.files?.[0];


    if (!file) {

        console.log(
            "No file selected."
        );

        return;

    }


    // --------------------------------------------------------
    // Validate file type
    // --------------------------------------------------------

    const allowedTypes = [
        "image/jpeg",
        "image/png",
        "image/jpg"
    ];


    if (!allowedTypes.includes(file.type)) {

        alert(
            "Please select a JPG, JPEG, or PNG image."
        );

        imageInput.value = "";

        return;

    }


    // --------------------------------------------------------
    // Validate file size
    // --------------------------------------------------------

    const maxSize =
        10 * 1024 * 1024;


    if (file.size > maxSize) {

        alert(
            "Maximum file size is 10MB."
        );

        imageInput.value = "";

        return;

    }


    // --------------------------------------------------------
    // Store file
    // --------------------------------------------------------

    selectedFile = file;

    console.log("[FRONTEND] File selected");

    console.log(
        "Selected file:",
        selectedFile.name
    );

    console.log(
        "File type:",
        selectedFile.type
    );

    console.log(
        "File size:",
        selectedFile.size
    );


    // --------------------------------------------------------
    // Reset previous processed image
    // --------------------------------------------------------

    resetProcessedState();


    // --------------------------------------------------------
    // Reset original URL
    // --------------------------------------------------------

    resetOriginalState();


    // --------------------------------------------------------
    // Create original preview
    // --------------------------------------------------------

    originalImageURL =
        URL.createObjectURL(
            selectedFile
        );


    originalPreview.src =
        originalImageURL;


    originalPreview.style.display =
        "block";


    // --------------------------------------------------------
    // Show preview state
    // --------------------------------------------------------

    showPreviewState();


    // --------------------------------------------------------
    // Reset controls
    // --------------------------------------------------------

    status.textContent =
        "Image ready to process.";

    processButton.disabled =
        false;

    processButton.classList.remove(
        "active"
    );


    console.log(
        "✅ Upload state changed to PREVIEW state."
    );

}


// ============================================================
// PROCESS BUTTON
// ============================================================

processButton.addEventListener(
    "click",
    function (event) {

        event.preventDefault();

        event.stopPropagation();

        console.log(
            "🔥 PROCESS BUTTON EVENT"
        );

        processImage();

    }
);


// ============================================================
// PROCESS IMAGE
// ============================================================

async function processImage() {

    console.log("");
    console.log("================================");
    console.log("🔥 PROCESS IMAGE START");
    console.log("================================");


    // --------------------------------------------------------
    // Prevent duplicate processing
    // --------------------------------------------------------

    if (isProcessing) {

        console.log(
            "⚠️ Already processing."
        );

        return;

    }


    // --------------------------------------------------------
    // Check selected file
    // --------------------------------------------------------

    if (!selectedFile) {

        alert(
            "Please upload an image first."
        );

        return;

    }


    isProcessing = true;

    processButton.disabled =
        true;

    processButton.classList.add(
        "active"
    );

    status.textContent =
        "Processing image...";


    try {

        console.log(
            "1️⃣ BEFORE API"
        );


        // ----------------------------------------------------
        // Call Flask backend
        // ----------------------------------------------------

        const blob =
            await enhanceImage(
                selectedFile,
                photoSize.value
            );


        console.log(
            "2️⃣ API RETURNED"
        );

        console.log(
            "Blob:",
            blob
        );

        console.log(
            "Blob size:",
            blob?.size
        );

        console.log(
            "Blob type:",
            blob?.type
        );


        // ----------------------------------------------------
        // Validate response
        // ----------------------------------------------------

        if (!blob) {

            throw new Error(
                "No blob returned from API."
            );

        }


        if (blob.size === 0) {

            throw new Error(
                "Empty blob received."
            );

        }


        // ----------------------------------------------------
        // Store processed blob
        // ----------------------------------------------------

        processedBlob =
            blob;


        console.log(
            "3️⃣ processedBlob STORED"
        );


        // ----------------------------------------------------
        // Revoke previous object URL
        // ----------------------------------------------------

        if (processedImageURL) {

            URL.revokeObjectURL(
                processedImageURL
            );

            processedImageURL =
                null;

        }


        // ----------------------------------------------------
        // Create object URL
        // ----------------------------------------------------

        processedImageURL =
            URL.createObjectURL(
                processedBlob
            );

        console.log("[FRONTEND] Object URL created");

        console.log(
            "4️⃣ OBJECT URL CREATED:",
            processedImageURL
        );


        // ----------------------------------------------------
        // IMPORTANT:
        //
        // Keep preview state visible.
        // Do NOT call showUploadState().
        // ----------------------------------------------------

        showPreviewState();


        console.log(
            "5️⃣ PREVIEW STATE FORCED ACTIVE"
        );


        // ----------------------------------------------------
        // Load processed image
        // ----------------------------------------------------

        outputPreview.onload =
            function () {

                console.log("[FRONTEND] Preview updated");

                console.log(
                    "6️⃣ PROCESSED IMAGE LOADED"
                );


                outputPreview.style.display =
                    "block";


                status.textContent =
                    "Processing complete.";

                console.log("[FRONTEND] Processing complete");


                processButton.disabled =
                    false;


                processButton.classList.remove(
                    "active"
                );


                isProcessing =
                    false;


                // Generate print layout
                generatePrintLayout();


                console.log(
                    "7️⃣ PROCESS FINISHED"
                );

            };


        outputPreview.onerror =
            function (error) {

                console.error(
                    "❌ PROCESSED IMAGE LOAD ERROR",
                    error
                );


                status.textContent =
                    "Image failed to load.";


                processButton.disabled =
                    false;


                processButton.classList.remove(
                    "active"
                );


                isProcessing =
                    false;

            };


        // ----------------------------------------------------
        // Set output image
        // ----------------------------------------------------

        outputPreview.src =
            processedImageURL;


        console.log(
            "8️⃣ OUTPUT SRC SET:",
            outputPreview.src
        );


    } catch (error) {

        console.error(
            "❌ PROCESS ERROR:",
            error
        );


        status.textContent =
            "Error processing image.";


        processButton.disabled =
            false;


        processButton.classList.remove(
            "active"
        );


        isProcessing =
            false;

    }

}


// ============================================================
// PHOTO SIZE CHANGE
// ============================================================

photoSize.addEventListener(
    "change",
    function () {

        console.log(
            "Photo size changed:",
            photoSize.value
        );


        if (processedImageURL) {

            generatePrintLayout();

        }

    }
);


// ============================================================
// GENERATE PRINT LAYOUT
// ============================================================

function generatePrintLayout() {

    console.log(
        "===== GENERATE PRINT LAYOUT ====="
    );


    if (!processedImageURL) {

        console.log(
            "No processed image available."
        );

        return;

    }


    const size =
        photoSize.value;


    const dimensions =
        PHOTO_DIMENSIONS[size];


    if (!dimensions) {

        console.error(
            "Invalid photo size:",
            size
        );

        return;

    }


    printSheet.innerHTML =
        "";


    for (
        let i = 0;
        i < 6;
        i++
    ) {

        const img =
            document.createElement(
                "img"
            );


        img.src =
            processedImageURL;


        img.classList.add(
            "print-photo"
        );


        img.style.width =
            dimensions.width;


        img.style.height =
            dimensions.height;


        printSheet.appendChild(
            img
        );

    }


    console.log(
        "✅ Print layout generated."
    );

}


// ============================================================
// DOWNLOAD
// ============================================================

function downloadImage() {

    console.log(
        "===== DOWNLOAD IMAGE ====="
    );


    if (!processedBlob) {

        alert(
            "Please process an image first."
        );

        return;

    }


    const url =
        URL.createObjectURL(
            processedBlob
        );


    const link =
        document.createElement(
            "a"
        );


    link.href =
        url;


    link.download =
        "id-photo.png";


    document.body.appendChild(
        link
    );


    link.click();


    link.remove();


    setTimeout(
        function () {

            URL.revokeObjectURL(
                url
            );

        },
        1000
    );

}


// ============================================================
// PRINT
// ============================================================

function printPhotos() {

    console.log(
        "===== PRINT PHOTOS ====="
    );


    if (!processedImageURL) {

        alert(
            "Please process an image first."
        );

        return;

    }


    window.print();

}


// ============================================================
// STORE PROCESSED IMAGE
// ============================================================

function storeProcessedData() {

    if (!processedBlob) {

        console.error(
            "No processed blob."
        );

        return Promise.resolve();

    }


    return new Promise(
        function (resolve) {

            // ----------------------------------------------------
            // Track completion of both readers
            // ----------------------------------------------------

            let processedDone = false;
            let originalDone = true; // If no original file, consider it done


            function checkDone() {

                if (processedDone && originalDone) {

                    resolve();

                }

            }


            // ----------------------------------------------------
            // Store processed image
            // ----------------------------------------------------

            const processedReader =
                new FileReader();


            processedReader.onloadend =
                function () {

                    sessionStorage.setItem(
                        "processedImage",
                        processedReader.result
                    );


                    sessionStorage.setItem(
                        "photoSize",
                        photoSize.value
                    );


                    sessionStorage.setItem(
                        "hasProcessedImage",
                        "true"
                    );


                    console.log(
                        "✅ Processed image stored."
                    );


                    processedDone = true;
                    checkDone();

                };


            processedReader.onerror =
                function (error) {

                    console.error(
                        "Processed image FileReader error:",
                        error
                    );


                    processedDone = true;
                    checkDone();

                };


            processedReader.readAsDataURL(
                processedBlob
            );


            // ----------------------------------------------------
            // Store original image (if selected)
            // ----------------------------------------------------

            if (selectedFile) {

                originalDone = false;


                const originalReader =
                    new FileReader();


                originalReader.onloadend =
                    function () {

                        sessionStorage.setItem(
                            "originalImage",
                            originalReader.result
                        );

                        console.log(
                            "✅ Original image stored."
                        );


                        originalDone = true;
                        checkDone();

                    };


                originalReader.onerror =
                    function (error) {

                        console.error(
                            "Original image FileReader error:",
                            error
                        );


                        originalDone = true;
                        checkDone();

                    };


                originalReader.readAsDataURL(
                    selectedFile
                );

            } else {

                processedDone = true;
                originalDone = true;
                resolve();

            }

        }
    );

}


// ============================================================
// FUZZY ANALYSIS
// ============================================================

async function goToFuzzyAnalysis() {

    console.log(
        "===== FUZZY ANALYSIS ====="
    );


    if (!processedBlob) {

        alert(
            "Please process an image first."
        );

        return;

    }


    await storeProcessedData();


    console.log(
        "✅ Data stored, navigating to analysis..."
    );


    window.location.href =
        "fuzzy-analysis.html";

}


// ============================================================
// BUTTON EVENTS
// ============================================================

downloadButton.addEventListener(
    "click",
    function (event) {

        event.preventDefault();

        event.stopPropagation();

        downloadImage();

    }
);


printButton.addEventListener(
    "click",
    function (event) {

        event.preventDefault();

        event.stopPropagation();

        printPhotos();

    }
);


fuzzyAnalysisButton.addEventListener(
    "click",
    function (event) {

        event.preventDefault();

        event.stopPropagation();

        goToFuzzyAnalysis();

    }
);


// ============================================================
// PAGE LIFECYCLE
// ============================================================
//
// IMPORTANT:
//
// Do NOT reset UI here.
// Do NOT remove "active".
// Do NOT add "done".
// Do NOT reload the page.
//
// pagehide is ONLY for releasing object URLs.
//

window.addEventListener(
    "pagehide",
    function () {

        console.log(
            "📄 PAGEHIDE"
        );


        // Only clean object URLs.
        // This does NOT change DOM state.

        if (processedImageURL) {

            URL.revokeObjectURL(
                processedImageURL
            );

            processedImageURL =
                null;

        }


        if (originalImageURL) {

            URL.revokeObjectURL(
                originalImageURL
            );

            originalImageURL =
                null;

        }

    }
);


// ============================================================
// PAGESHOW DEBUG
// ============================================================

window.addEventListener(
    "pageshow",
    function (event) {

        console.log(
            "📄 PAGESHOW FIRED"
        );


        console.log(
            "Persisted:",
            event.persisted
        );


        console.log(
            "URL:",
            window.location.href
        );

    }
);


// ============================================================
// EXPOSE FUNCTIONS
// ============================================================

window.processImage =
    processImage;

window.downloadImage =
    downloadImage;

window.printPhotos =
    printPhotos;

window.goToFuzzyAnalysis =
    goToFuzzyAnalysis;


// ============================================================
// INITIAL STATE
// ============================================================

showUploadState();


console.log("");
console.log(
    "======================================"
);

console.log(
    "✅ ID-Oto script.js loaded successfully"
);

console.log(
    "======================================"
);