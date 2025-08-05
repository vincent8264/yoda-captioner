
// Dynamic settings button
const settingsPanel = document.getElementById('settingsPanel');
const toggleBtn = document.getElementById('toggleSettingsBtn');

settingsPanel.addEventListener('show.bs.collapse', () => {
    toggleBtn.textContent = 'Advanced Settings ▲';
});
settingsPanel.addEventListener('hide.bs.collapse', () => {
    toggleBtn.textContent = 'Advanced Settings ▼';
});

// Advanced settings display update
const tempSlider = document.getElementById('temperatureSlider');
const tempValue = document.getElementById('tempValue');
tempSlider.addEventListener('input', () => {
    tempValue.textContent = tempSlider.value;
});

const topKSlider = document.getElementById('topKSlider');
const topKValue = document.getElementById('topKValue');
topKSlider.addEventListener('input', () => {
    topKValue.textContent = topKSlider.value;
});

const topPSlider = document.getElementById('topPSlider');
const topPValue = document.getElementById('topPValue');
topPSlider.addEventListener('input', () => {
    topPValue.textContent = topPSlider.value;
});

// Image Preview
function previewImage(input) {
    const display = document.getElementById('imageDisplay');
    const errorBox = document.getElementById('errorBox');
    const file = input.files[0];
    if (file) {
        errorBox.classList.add('d-none');
        errorBox.textContent = '';
      
        const reader = new FileReader();
        reader.onload = function (e) {
            display.src = e.target.result;
            display.classList.remove('d-none');
      };
        reader.readAsDataURL(file);
    }
  }

async function generateCaption() {
    const fileInput = document.getElementById('imageInput');
    const captionOutput = document.getElementById('captionOutput');
    const captionText = document.getElementById('captionText');
    const errorBox = document.getElementById('errorBox');
    const generateBtn = document.getElementById('generateBtn');

    const file = fileInput.files[0];
    if (!file) {
        errorBox.textContent = 'Please select an image first.';
        errorBox.classList.remove('d-none');
        return;
    }

    // Reset UI and send request
    captionOutput.classList.add('d-none');
    captionText.textContent = '';
    errorBox.classList.add('d-none');
    errorBox.textContent = '';
    generateBtn.disabled = true;
    generateBtn.textContent = 'Generating...';
    
    const settings = {
        temperature: parseFloat(document.getElementById('temperatureSlider').value),
        top_k: parseInt(document.getElementById('topKSlider').value),
        top_p: parseFloat(document.getElementById('topPSlider').value),
    };

    const formData = new FormData();
    formData.append('image', file);
    formData.append('settings', JSON.stringify(settings));

    try {
        const response = await fetch('/caption', {
            method: 'POST',
            body: formData
        });

        let data = null;
        try {
            data = await response.json();
        } catch (jsonError) {
            // Catch invalid JSON response
            throw new Error(`Invalid server response. Status ${response.status}`);
        }

        if (!response.ok) {
            // Check if the response contains errors
            throw new Error(data.error);
        }

        captionText.textContent = data.caption;
        captionOutput.classList.remove('d-none');
    } catch (error) {
        // Show error message
        errorBox.textContent = error.message || 'An unexpected error occurred.';
        errorBox.classList.remove('d-none');
    } finally {
        generateBtn.disabled = false;
        generateBtn.textContent = 'Generate Caption';
    }
}
