const API_BASE_URL = "http://localhost:8000/api";
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
            // Not JSON, using the default message
        }

        throw new Error(errorMessage);
    }

    const blob = await response.blob();

    console.log("[FRONTEND] Blob received");
    console.log("Blob type:", blob.type);
    console.log("Blob size:", blob.size);

    return blob;
}
// Get the image features
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
        } catch (e) {// Not JSON, use default message/
            }

        throw new Error(errorMessage);
    }

    return await response.json();
}

// Remove the background
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

// Crop the image
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