/**
 * API service layer for the ID-Oto frontend.
 * All requests go directly to the Flask backend.
 */

// Flask Backend URL
const API_BASE_URL = "http://localhost:8000/api";

/**
 * Process the complete ID photo pipeline.
 * The Flask backend will:
 * 1. Validate Image
 * 2. Remove Background
 * 3. Analyze Image
 * 4. Apply Fuzzy Logic
 * 5. Crop to Selected Size
 * 6. Return Processed Image
 */
export async function enhanceImage(file, type = "2x2") {

    console.log("[FRONTEND] Processing started");

    const formData = new FormData();

    formData.append("image", file);
    formData.append("type", type);

    console.log("[FRONTEND] API request sent");

    const response = await fetch(`${API_BASE_URL}/process`, {
        method: "POST",
        body: formData
    });

    console.log("[FRONTEND] API response received");
    console.log("Status:", response.status);
    console.log("Content-Type:", response.headers.get("content-type"));

    if (!response.ok) {
        // Try to parse error message from JSON response
        let errorMessage = `Processing failed: ${response.status}`;

        try {
            const errorData = await response.json();
            if (errorData && errorData.error) {
                errorMessage = errorData.error;
            }
        } catch (e) {
            // Not JSON, use default message
        }

        throw new Error(errorMessage);
    }

    const blob = await response.blob();

    console.log("[FRONTEND] Blob received");
    console.log("Blob type:", blob.type);
    console.log("Blob size:", blob.size);

    return blob;
}

/**
 * Get fuzzy logic analysis.
 */
export async function analyzeImage(file) {
    const formData = new FormData();
    formData.append("image", file);

    const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: "POST",
        body: formData
    });

    if (!response.ok) {
        let errorMessage = `Analysis failed: ${response.status}`;

        try {
            const errorData = await response.json();
            if (errorData && errorData.error) {
                errorMessage = errorData.error;
            }
        } catch (e) {
            // Not JSON, use default message
        }

        throw new Error(errorMessage);
    }

    return await response.json();
}

/**
 * Remove Background only.
 */
export async function removeBackground(file) {
    const formData = new FormData();
    formData.append("image", file);

    const response = await fetch(`${API_BASE_URL}/remove-bg`, {
        method: "POST",
        body: formData
    });

    if (!response.ok) {
        let errorMessage = `Background removal failed: ${response.status}`;

        try {
            const errorData = await response.json();
            if (errorData && errorData.error) {
                errorMessage = errorData.error;
            }
        } catch (e) {
            // Not JSON, use default message
        }

        throw new Error(errorMessage);
    }

    return await response.blob();
}

/**
 * Crop only.
 */
export async function cropIdPhoto(file, type) {
    const formData = new FormData();

    formData.append("image", file);
    formData.append("type", type);

    const response = await fetch(`${API_BASE_URL}/id-crop`, {
        method: "POST",
        body: formData
    });

    if (!response.ok) {
        let errorMessage = `Crop failed: ${response.status}`;

        try {
            const errorData = await response.json();
            if (errorData && errorData.error) {
                errorMessage = errorData.error;
            }
        } catch (e) {
            // Not JSON, use default message
        }

        throw new Error(errorMessage);
    }

    return await response.blob();
}