import { enhanceImage } from "./js/api.js";

// ######### State #########
let selectedFile = null;
let processedBlob = null;
let processedImageURL = null;
let originalImageURL = null;
let isProcessing = false;

// ######### DOM Elements #########
const imageInput = document.getElementById("imageInput");
const uploadArea = document.getElementById("uploadArea");
const previewContainer = document.getElementById("previewContainer");
const originalPreview = document.getElementById("originalPreview");
const outputPreview = document.getElementById("outputPreview");
const status = document.getElementById("status");
const processButton = document.getElementById("process-button");
const downloadButton = document.getElementById("download-button");
const printButton = document.getElementById("print-button");
const fuzzyAnalysisButton = document.getElementById("fuzzy-analysis-button");
const photoSize = document.getElementById("photoSize");
const printSheet = document.getElementById("printSheet");

// ######### DOM Check #########
console.log("DOM Elements:", {
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
});

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

if (requiredElements.some(element => !element)) {
    console.error("One or more required HTML elements are missing.");
}

// ######### Photo Dimensions #########
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
    passport: {
        width: "35mm",
        height: "45mm"
    }
};

// ######### UI State #########
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
        URL.revokeObjectURL(processedImageURL);
        processedImageURL = null;
    }

    outputPreview.removeAttribute("src");
    outputPreview.style.display = "none";
    printSheet.innerHTML = "";
}

function resetOriginalState() {
    if (originalImageURL) {
        URL.revokeObjectURL(originalImageURL);
        originalImageURL = null;
    }

    originalPreview.removeAttribute("src");
}

// ######### File Input #########
imageInput.addEventListener("change", handleFileSelect);

function handleFileSelect(event) {
    console.log("HANDLE FILE SELECT");
    const file = event.target.files?.[0];

    if (!file) {
        console.log("No file selected.");
        return;
    }
    const allowedTypes = [
        "image/jpeg",
        "image/png",
        "image/jpg"
    ];

    if (!allowedTypes.includes(file.type)) {
        alert("Please select a JPG, JPEG, or PNG image.");
        imageInput.value = "";
        return;
    }

    const maxSize = 10 * 1024 * 1024;

    if (file.size > maxSize) {
        alert("Maximum file size is 10MB.");
        imageInput.value = "";
        return;
    }

    selectedFile = file;

    console.log("[FRONTEND] File selected:", selectedFile.name);
    console.log("File type:", selectedFile.type);
    console.log("File size:", selectedFile.size);
    resetProcessedState();
    resetOriginalState();
    originalImageURL = URL.createObjectURL(selectedFile);
    originalPreview.src = originalImageURL;
    originalPreview.style.display = "block";
    showPreviewState();
    status.textContent = "Image ready to process.";
    processButton.disabled = false;
    processButton.classList.remove("active");

    console.log("Upload state changed to PREVIEW state.");
}

// ######### Process Button #########
processButton.addEventListener("click", event => {
    event.preventDefault();
    event.stopPropagation();
    console.log("PROCESS BUTTON EVENT");
    processImage();
});

// ######### Process Image #########
async function processImage() {
    console.log("PROCESS IMAGE START");
    if (isProcessing) {
        console.log("Already processing.");
        return;
    }

    if (!selectedFile) {
        alert("Please upload an image first.");
        return;
    }

    isProcessing = true;
    processButton.disabled = true;
    processButton.classList.add("active");
    status.textContent = "Processing image...";

    try {
        console.log("1. BEFORE API");

        const blob = await enhanceImage(
            selectedFile,
            photoSize.value
        );

        console.log("2. API RETURNED");
        console.log("Blob:", blob);
        console.log("Blob size:", blob?.size);
        console.log("Blob type:", blob?.type);

        if (!blob) {
            throw new Error("No blob returned from API.");
        }

        if (blob.size === 0) {
            throw new Error("Empty blob received.");
        }

        processedBlob = blob;

        console.log("3. processedBlob STORED");

        if (processedImageURL) {
            URL.revokeObjectURL(processedImageURL);
            processedImageURL = null;
        }

        processedImageURL = URL.createObjectURL(processedBlob);

        console.log(
            "4. OBJECT URL CREATED:",
            processedImageURL
        );

        showPreviewState();
        console.log("5. PREVIEW STATE FORCED ACTIVE");
        outputPreview.onload = () => {
            console.log("[FRONTEND] Preview updated");
            console.log("6. PROCESSED IMAGE LOADED");
            outputPreview.style.display = "block";
            status.textContent = "Processing complete.";
            processButton.disabled = false;
            processButton.classList.remove("active");
            isProcessing = false;
            generatePrintLayout();
            console.log("7. PROCESS FINISHED");
        };

        outputPreview.onerror = error => {
            console.error("PROCESSED IMAGE LOAD ERROR", error);
            status.textContent = "Image failed to load.";
            processButton.disabled = false;
            processButton.classList.remove("active");
            isProcessing = false;
        };

        outputPreview.src = processedImageURL;
        console.log("8. OUTPUT SRC SET:", outputPreview.src);

    } catch (error) {
        console.error("PROCESS ERROR:", error);
        status.textContent = "Error processing image.";
        processButton.disabled = false;
        processButton.classList.remove("active");
        isProcessing = false;
    }
}

// ######### Photo Size Change #########
photoSize.addEventListener("change", () => {
    console.log("Photo size changed:", photoSize.value);

    if (processedImageURL) {
        generatePrintLayout();
    }
});

// ######### Generate Print Layout #########
function generatePrintLayout() {
    console.log("GENERATE PRINT LAYOUT");
    if (!processedImageURL) {
        console.log("No processed image available.");
        return;
    }

    const size = photoSize.value;
    const dimensions = PHOTO_DIMENSIONS[size];

    if (!dimensions) {
        console.error("Invalid photo size:", size);
        return;
    }

    printSheet.innerHTML = "";
    for (let i = 0; i < 6; i++) {
        const img = document.createElement("img");
        img.src = processedImageURL;
        img.classList.add("print-photo");
        img.style.width = dimensions.width;
        img.style.height = dimensions.height;
        printSheet.appendChild(img);
    }

    console.log("Print layout generated.");
}

// ######### Download #########
function downloadImage() {
    console.log("DOWNLOAD IMAGE");

    if (!processedBlob) {
        alert("Please process an image first.");
        return;
    }

    const url = URL.createObjectURL(processedBlob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "id-photo.png";

    document.body.appendChild(link);
    link.click();
    link.remove();

    setTimeout(() => {
        URL.revokeObjectURL(url);
    }, 1000);
}

// ######### Print #########
function printPhotos() {
    console.log("PRINT PHOTOS");

    if (!processedImageURL) {
        alert("Please process an image first.");
        return;
    }

    window.print();
}

// ######### Store Processed Image #########
function storeProcessedData() {
    if (!processedBlob) {
        console.error("No processed blob.");
        return Promise.resolve();
    }

    return new Promise(resolve => {
        let processedDone = false;
        let originalDone = !selectedFile;

        function checkDone() {
            if (processedDone && originalDone) {
                resolve();
            }
        }

        const processedReader = new FileReader();

        processedReader.onloadend = () => {
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

            console.log("Processed image stored.");

            processedDone = true;
            checkDone();
        };

        processedReader.onerror = error => {
            console.error(
                "Processed image FileReader error:",
                error
            );

            processedDone = true;
            checkDone();
        };

        processedReader.readAsDataURL(processedBlob);

        if (selectedFile) {
            const originalReader = new FileReader();

            originalReader.onloadend = () => {
                sessionStorage.setItem(
                    "originalImage",
                    originalReader.result
                );

                console.log("Original image stored.");

                originalDone = true;
                checkDone();
            };

            originalReader.onerror = error => {
                console.error(
                    "Original image FileReader error:",
                    error
                );

                originalDone = true;
                checkDone();
            };

            originalReader.readAsDataURL(selectedFile);
        }
    });
}

// ######### Fuzzy Analysis #########
async function goToFuzzyAnalysis() {
    console.log("FUZZY ANALYSIS");

    if (!processedBlob) {
        alert("Please process an image first.");
        return;
    }

    await storeProcessedData();

    console.log(
        "Data stored, navigating to analysis..."
    );

    window.location.href = "fuzzy-analysis.html";
}

// ######### Button Events #########
downloadButton.addEventListener("click", event => {
    event.preventDefault();
    event.stopPropagation();

    downloadImage();
});

printButton.addEventListener("click", event => {
    event.preventDefault();
    event.stopPropagation();

    printPhotos();
});

fuzzyAnalysisButton.addEventListener("click", event => {
    event.preventDefault();
    event.stopPropagation();

    goToFuzzyAnalysis();
});

// ######### Page Lifecycle #########
window.addEventListener("pagehide", () => {
    console.log("PAGEHIDE");

    if (processedImageURL) {
        URL.revokeObjectURL(processedImageURL);
        processedImageURL = null;
    }

    if (originalImageURL) {
        URL.revokeObjectURL(originalImageURL);
        originalImageURL = null;
    }
});

// ######### Page Show Debug #########
window.addEventListener("pageshow", event => {
    console.log("PAGESHOW FIRED");
    console.log("Persisted:", event.persisted);
    console.log("URL:", window.location.href);
});

// ######### Expose Functions #########
window.processImage = processImage;
window.downloadImage = downloadImage;
window.printPhotos = printPhotos;
window.goToFuzzyAnalysis = goToFuzzyAnalysis;

// ######### Initial State #########
showUploadState();