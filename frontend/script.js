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
const processedSkeleton = document.getElementById("processedSkeleton");
const status = document.getElementById("status");
const processButton = document.getElementById("process-button");
const changeImageButton = document.getElementById("change-image-button");
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
    changeImageButton,
    downloadButton,
    printButton,
    fuzzyAnalysisButton,
    photoSize,
    printSheet
});

// Elements the page cannot work without.
const requiredElements = {
    imageInput,
    uploadArea,
    previewContainer,
    originalPreview,
    outputPreview,
    status,
    processButton,
    downloadButton,
    printButton,
    photoSize,
    printSheet
};

// The fuzzy-analysis button is intentionally commented out in the markup, so it
// is optional and must not be treated as a missing required element.
const missingElements = Object.entries(requiredElements)
    .filter(([, element]) => !element)
    .map(([name]) => name);

if (missingElements.length) {
    console.error("Missing required DOM elements:", missingElements);
}

// ######### Photo Dimensions #########
const PHOTO_DIMENSIONS = {
    "1x1": {
        width: "1in",
        height: "1in",
        ratio: "1 / 1"
    },
    "1.5x1.5": {
        width: "1.5in",
        height: "1.5in",
        ratio: "1 / 1"
    },
    "2x2": {
        width: "2in",
        height: "2in",
        ratio: "1 / 1"
    },
    passport: {
        width: "35mm",
        height: "45mm",
        ratio: "35 / 45"
    }
};

// ######### UI State #########
function showUploadState() {
    uploadArea.classList.remove("done");
    previewContainer.classList.remove("active");
    document.body.classList.remove("preview-mode");
}

function showPreviewState() {
    uploadArea.classList.add("done");
    previewContainer.classList.add("active");
    document.body.classList.add("preview-mode");
}

function resetProcessedState() {
    processedBlob = null;

    if (processedImageURL) {
        URL.revokeObjectURL(processedImageURL);
        processedImageURL = null;
    }

    outputPreview.removeAttribute("src");
    outputPreview.style.display = "none";
    if (processedSkeleton) {
        processedSkeleton.style.display = "none";
    }
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

// ######### Change Image Button #########
// Re-opens the file picker so the user can pick a different photo without
// leaving the preview screen. The input value is cleared first, otherwise
// re-picking the very same file would not fire a "change" event.
if (changeImageButton) {
    changeImageButton.addEventListener("click", event => {
        event.preventDefault();
        event.stopPropagation();
        console.log("CHANGE IMAGE BUTTON EVENT");

        if (isProcessing) {
            console.log("Cannot change image while processing.");
            return;
        }

        imageInput.value = "";
        imageInput.click();
    });
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
    if (changeImageButton) {
        changeImageButton.disabled = true;
    }
    status.textContent = "Processing image...";

    // Show skeleton loader on the processed image container while processing
    if (processedSkeleton) {
        processedSkeleton.style.display = "block";
    }
    outputPreview.style.display = "none";

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
            if (processedSkeleton) {
                processedSkeleton.style.display = "none";
            }
            outputPreview.style.display = "block";
            status.textContent = "Processing complete.";
            processButton.disabled = false;
            processButton.classList.remove("active");
            if (changeImageButton) {
                changeImageButton.disabled = false;
            }
            isProcessing = false;
            generatePrintLayout();
            console.log("7. PROCESS FINISHED");
        };

        outputPreview.onerror = error => {
            console.error("PROCESSED IMAGE LOAD ERROR", error);
            if (processedSkeleton) {
                processedSkeleton.style.display = "none";
            }
            status.textContent = "Image failed to load.";
            processButton.disabled = false;
            processButton.classList.remove("active");
            if (changeImageButton) {
                changeImageButton.disabled = false;
            }
            isProcessing = false;
        };

        outputPreview.src = processedImageURL;
        console.log("8. OUTPUT SRC SET:", outputPreview.src);

    } catch (error) {
        console.error("PROCESS ERROR:", error);
        if (processedSkeleton) {
            processedSkeleton.style.display = "none";
        }
        status.textContent = "Error processing image.";
        processButton.disabled = false;
        processButton.classList.remove("active");
        if (changeImageButton) {
            changeImageButton.disabled = false;
        }
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

        // Keep the selected ID ratio when the preview scales down on screen
        img.style.aspectRatio = dimensions.ratio;

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

// The fuzzy-analysis button is currently commented out in the markup, so the
// element may be missing. Guard the listener so its absence cannot break the
// rest of the page.
if (fuzzyAnalysisButton) {
    fuzzyAnalysisButton.addEventListener("click", event => {
        event.preventDefault();
        event.stopPropagation();

        goToFuzzyAnalysis();
    });
}

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
showUploadState();// ######### Background Removal Mode Selection #########
const bgModeFast = document.getElementById("bgModeFast");
const bgModeHigh = document.getElementById("bgModeHigh");
const bgModalOverlay = document.getElementById("bgModalOverlay");
const bgModalClose = document.getElementById("bgModalClose");

// Currently selected removal mode: "fast" or "high"
let selectedBgMode = "fast";
// ######### Background Removal Mode Features (per category) #########
const bgModeFeatures = {
    fast: {
        title: "Fast Removal",
        items: [
            { label: "Supporting label", value: "Quick processing" },
            { label: "Priority", value: "Speed" },
            { label: "Processing time", value: "Shorter" },
            { label: "Recommended for", value: "Simple images" }
        ]
    },
    high: {
        title: "High-Quality Removal",
        items: [
            { label: "Supporting label", value: "Enhanced detail" },
            { label: "Priority", value: "Accuracy and detail" },
            { label: "Processing time", value: "Longer" },
            { label: "Recommended for", value: "ID photos and complex edges" }
        ]
    }
};

// Open per-category modal when an info icon is clicked
document.querySelectorAll(".bg-mode-info").forEach((info) => {
    info.addEventListener("click", (event) => {
        event.stopPropagation();
        const card = info.closest(".bg-mode-card");
        const mode = card ? card.getAttribute("data-mode") : "fast";
        const data = bgModeFeatures[mode] || bgModeFeatures.fast;
        const titleEl = document.getElementById("bgModalTitle");
        const contentEl = document.getElementById("bgModalContent");
        if (titleEl) titleEl.textContent = data.title;
        if (contentEl) {
            contentEl.innerHTML = data.items
                .map((item) => `<p><strong>${item.label}:</strong> ${item.value}</p>`)
                .join("");
        }
        if (bgModalOverlay) {
            bgModalOverlay.removeAttribute("hidden");
            bgModalOverlay.setAttribute("aria-hidden", "false");
            bgModalOverlay.focus();
        }
    });
});


// Update the visual selected state of the mode cards
function updateBgModeSelection() {
    if (bgModeFast && bgModeHigh) {
        if (selectedBgMode === "fast") {
            bgModeFast.classList.add("bg-mode-selected");
            bgModeFast.setAttribute("aria-pressed", "true");
            bgModeHigh.classList.remove("bg-mode-selected");
            bgModeHigh.setAttribute("aria-pressed", "false");
        } else {
            bgModeHigh.classList.add("bg-mode-selected");
            bgModeHigh.setAttribute("aria-pressed", "true");
            bgModeFast.classList.remove("bg-mode-selected");
            bgModeFast.setAttribute("aria-pressed", "false");
        }
        console.log(`[BG MODE] Selected: ${selectedBgMode}`);
    }
}

// Toggle selection when a mode card is clicked
if (bgModeFast) {
    bgModeFast.addEventListener("click", () => {
        if (selectedBgMode !== "fast") {
            selectedBgMode = "fast";
            updateBgModeSelection();
        }
    });
}

if (bgModeHigh) {
    bgModeHigh.addEventListener("click", () => {
        if (selectedBgMode !== "high") {
            selectedBgMode = "high";
            updateBgModeSelection();
        }
    });
}

// Open the comparison modal when an info icon is clicked
document.querySelectorAll(".bg-mode-info").forEach((info) => {
    info.addEventListener("click", () => {
        if (bgModalOverlay) {
            bgModalOverlay.removeAttribute("hidden");
            bgModalOverlay.setAttribute("aria-hidden", "false");
            bgModalOverlay.focus();
        }
    });
});

// Close modal via close button
if (bgModalClose) {
    bgModalClose.addEventListener("click", () => {
        closeBgModal();
    });
}

// Close modal when clicking the overlay background
if (bgModalOverlay) {
    bgModalOverlay.addEventListener("click", (event) => {
        if (event.target === bgModalOverlay) {
            closeBgModal();
        }
    });
}

// Close modal on Escape key
document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && bgModalOverlay && !bgModalOverlay.hasAttribute("hidden")) {
        closeBgModal();
    }
});

function closeBgModal() {
    if (bgModalOverlay) {
        bgModalOverlay.setAttribute("hidden", "");
        bgModalOverlay.setAttribute("aria-hidden", "true");
    }
}

// Initialize selection state on load
updateBgModeSelection();

// ######### Background Removal Mode Details (inline) #########
// Shows the per-card details with a smooth animation when the question-mark
// icon is clicked, and hides them when clicking anywhere else on the screen.
const bgModeInfoButtons = document.querySelectorAll(".bg-mode-info");

function hideAllBgModeDetails() {
    document.querySelectorAll(".bg-mode-details.open").forEach((panel) => {
        panel.classList.remove("open");
    });
    document.querySelectorAll(".bg-mode-card.bg-mode-expanded").forEach((card) => {
        card.classList.remove("bg-mode-expanded");
    });
}

bgModeInfoButtons.forEach((info) => {
    info.addEventListener("click", (event) => {
        event.stopPropagation(); // prevent card selection toggle & immediate close
        const card = info.closest(".bg-mode-card");
        if (!card) return;
        const panel = card.querySelector(".bg-mode-details");
        if (!panel) return;
        const isOpen = panel.classList.contains("open");
        hideAllBgModeDetails(); // close any other open detail panel
        if (!isOpen) {
            panel.classList.add("open");
            card.classList.add("bg-mode-expanded");
        }
    });
});

// Hide details when clicking any part of the screen outside them
document.addEventListener("click", (event) => {
    if (
        !event.target.closest(".bg-mode-details") &&
        !event.target.closest(".bg-mode-info")
    ) {
        hideAllBgModeDetails();
    }
});
