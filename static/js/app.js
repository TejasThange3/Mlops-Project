// Water Potability Prediction - Frontend JavaScript

const API_BASE_URL = 'http://127.0.0.1:8000';

// Parameter information with typical ranges and descriptions
const parameterInfo = {
    ph: {
        name: 'pH Level',
        unit: 'pH units',
        ranges: { safe: [6.5, 8.5], warning: [5, 9], danger: [0, 14] },
        description: 'Measure of water acidity/alkalinity'
    },
    hardness: {
        name: 'Hardness',
        unit: 'mg/L',
        ranges: { safe: [50, 200], warning: [200, 300], danger: [0, 1000] },
        description: 'Mineral content in water'
    },
    solids: {
        name: 'Total Dissolved Solids',
        unit: 'ppm',
        ranges: { safe: [100, 500], warning: [500, 1000], danger: [0, 50000] },
        description: 'Total dissolved substances'
    },
    chloramines: {
        name: 'Chloramines',
        unit: 'ppm',
        ranges: { safe: [4, 10], warning: [0, 4], danger: [10, 20] },
        description: 'Disinfectant concentration'
    },
    sulfate: {
        name: 'Sulfate',
        unit: 'mg/L',
        ranges: { safe: [200, 400], warning: [100, 200], danger: [0, 1000] },
        description: 'Sulfur compound concentration'
    },
    conductivity: {
        name: 'Conductivity',
        unit: 'μS/cm',
        ranges: { safe: [200, 600], warning: [600, 800], danger: [0, 2000] },
        description: 'Electrical conductivity'
    },
    organic_carbon: {
        name: 'Organic Carbon',
        unit: 'ppm',
        ranges: { safe: [2, 15], warning: [15, 20], danger: [0, 50] },
        description: 'Organic matter content'
    },
    trihalomethanes: {
        name: 'Trihalomethanes',
        unit: 'μg/L',
        ranges: { safe: [20, 60], warning: [60, 80], danger: [0, 200] },
        description: 'Disinfection byproducts'
    },
    turbidity: {
        name: 'Turbidity',
        unit: 'NTU',
        ranges: { safe: [0, 1], warning: [1, 5], danger: [0, 20] },
        description: 'Water clarity measure'
    }
};

// Form submission handler
document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Collect form data
    const formData = {
        ph: parseFloat(document.getElementById('ph').value),
        Hardness: parseFloat(document.getElementById('hardness').value),
        Solids: parseFloat(document.getElementById('solids').value),
        Chloramines: parseFloat(document.getElementById('chloramines').value),
        Sulfate: parseFloat(document.getElementById('sulfate').value),
        Conductivity: parseFloat(document.getElementById('conductivity').value),
        Organic_carbon: parseFloat(document.getElementById('organic_carbon').value),
        Trihalomethanes: parseFloat(document.getElementById('trihalomethanes').value),
        Turbidity: parseFloat(document.getElementById('turbidity').value)
    };

    // Validate pH range
    if (formData.ph < 5 || formData.ph > 10) {
        alert('⚠️ Warning: pH value is outside the recommended range (5-10). Prediction accuracy may be affected.');
    }

    // Show loading indicator
    document.getElementById('loadingIndicator').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';

    try {
        // Make API request
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        
        // Display results
        displayResults(result, formData);
        
    } catch (error) {
        console.error('Error:', error);
        alert('❌ Error making prediction. Please ensure the API server is running and try again.');
    } finally {
        // Hide loading indicator
        document.getElementById('loadingIndicator').style.display = 'none';
    }
});

// Display prediction results
function displayResults(prediction, inputData) {
    const resultsSection = document.getElementById('resultsSection');
    const predictionCard = document.getElementById('predictionCard');
    const resultIcon = document.getElementById('resultIcon');
    const resultLabel = document.getElementById('resultLabel');
    const resultConfidence = document.getElementById('resultConfidence');

    // Set prediction result
    const isPotable = prediction.potability === 1;
    
    if (isPotable) {
        predictionCard.className = 'prediction-result potable';
        resultIcon.textContent = '✅';
        resultLabel.textContent = '🌊 Water is Potable';
    } else {
        predictionCard.className = 'prediction-result not-potable';
        resultIcon.textContent = '⚠️';
        resultLabel.textContent = '⛔ Water is Not Potable';
    }

    // Display confidence
    const confidencePercent = (prediction.confidence * 100).toFixed(2);
    resultConfidence.textContent = `Confidence: ${confidencePercent}%`;

    // Populate results table
    populateResultsTable(inputData);

    // Show results section with animation
    resultsSection.style.display = 'block';
    
    // Store prediction data for retraining
    lastPredictionData = inputData;
    
    // Show retrain section
    document.getElementById('retrainSection').style.display = 'block';
    
    // Smooth scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Populate results table with parameter values
function populateResultsTable(data) {
    const tableBody = document.getElementById('resultsTableBody');
    tableBody.innerHTML = '';

    // Map form field names to API names
    const dataMapping = {
        ph: data.ph,
        hardness: data.Hardness,
        solids: data.Solids,
        chloramines: data.Chloramines,
        sulfate: data.Sulfate,
        conductivity: data.Conductivity,
        organic_carbon: data.Organic_carbon,
        trihalomethanes: data.Trihalomethanes,
        turbidity: data.Turbidity
    };

    // Create table rows
    Object.entries(dataMapping).forEach(([key, value]) => {
        const info = parameterInfo[key];
        const status = getParameterStatus(key, value);
        
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${info.name}</strong><br><small style="color: #64748b;">${info.description}</small></td>
            <td class="value-cell">${value.toFixed(2)}</td>
            <td class="unit-cell">${info.unit}</td>
            <td>${status}</td>
        `;
        
        tableBody.appendChild(row);
    });
}

// Determine parameter status based on value
function getParameterStatus(parameter, value) {
    const info = parameterInfo[parameter];
    
    if (value >= info.ranges.safe[0] && value <= info.ranges.safe[1]) {
        return '<span class="status-badge healthy">✓ Healthy</span>';
    } else if (value >= info.ranges.warning[0] && value <= info.ranges.warning[1]) {
        return '<span class="status-badge warning">⚠ Warning</span>';
    } else {
        return '<span class="status-badge danger">✗ Danger</span>';
    }
}

// Reset form
function resetForm() {
    document.getElementById('predictionForm').reset();
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('ph').focus();
}

// Auto-fill with sample data for testing
function loadSampleData() {
    document.getElementById('ph').value = '7.0';
    document.getElementById('hardness').value = '200.0';
    document.getElementById('solids').value = '20000.0';
    document.getElementById('chloramines').value = '7.5';
    document.getElementById('sulfate').value = '350.0';
    document.getElementById('conductivity').value = '400.0';
    document.getElementById('organic_carbon').value = '14.0';
    document.getElementById('trihalomethanes').value = '70.0';
    document.getElementById('turbidity').value = '4.0';
}

// Add keyboard shortcut for sample data (Ctrl + L)
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.key === 'l') {
        e.preventDefault();
        loadSampleData();
    }
});

// Add real-time validation
document.querySelectorAll('input[type="number"]').forEach(input => {
    input.addEventListener('input', function() {
        if (this.value < 0) {
            this.style.borderColor = '#ef4444';
        } else {
            this.style.borderColor = '';
        }
    });
});

// Check API health on page load
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('✅ API server is running');
        }
    } catch (error) {
        console.warn('⚠️ API server is not responding. Please start the server.');
        // Optionally show a notification to the user
    }
}

// ============================================================================
// Model Version Management Functions
// ============================================================================

// Store last prediction data for retraining
let lastPredictionData = null;

// Fetch and populate model versions
async function refreshModelVersions() {
    try {
        const response = await fetch(`${API_BASE_URL}/models/versions`);
        const data = await response.json();
        
        const select = document.getElementById('modelVersionSelect');
        select.innerHTML = ''; // Clear existing options
        
        // Populate with versions
        data.versions.forEach(version => {
            const option = document.createElement('option');
            option.value = version.version;
            
            // Format display text
            let displayText = version.version;
            if (version.version === 'Original') {
                displayText += ' (Ensemble)';
            } else {
                displayText += ` - ${version.training_samples} samples`;
            }
            
            // Add accuracy info
            displayText += ` - ${(version.cv_accuracy * 100).toFixed(1)}% CV`;
            
            option.textContent = displayText;
            
            // Mark current version as selected
            if (version.is_current) {
                option.selected = true;
            }
            
            select.appendChild(option);
        });
        
        showNotification('success', 'Versions Updated', 'Model versions refreshed successfully!');
        
    } catch (error) {
        console.error('Error fetching model versions:', error);
        showNotification('error', 'Error', 'Failed to fetch model versions.');
    }
}

// Switch model version
async function switchModelVersion() {
    const select = document.getElementById('modelVersionSelect');
    const selectedVersion = select.value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/models/switch`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ version: selectedVersion })
        });
        
        if (!response.ok) {
            throw new Error('Failed to switch version');
        }
        
        const result = await response.json();
        
        showNotification('success', 'Model Switched', 
            `Now using: ${result.current_version}`);
        
        console.log(`✅ Switched to model version: ${result.current_version}`);
        
    } catch (error) {
        console.error('Error switching model:', error);
        showNotification('error', 'Switch Failed', 'Could not switch model version.');
        // Revert selection
        refreshModelVersions();
    }
}

// Retrain model with user feedback
async function retrainModel(actualPotability) {
    if (!lastPredictionData) {
        showNotification('error', 'No Data', 'Please make a prediction first!');
        return;
    }
    
    // Disable buttons during retraining
    const buttons = document.querySelectorAll('.btn-retrain');
    buttons.forEach(btn => {
        btn.disabled = true;
        btn.classList.add('loading');
    });
    
    try {
        const retrainRequest = {
            water_quality: lastPredictionData,
            actual_potability: actualPotability
        };
        
        showNotification('info', 'Retraining Started', 
            'Creating new model version... This may take a minute.');
        
        const response = await fetch(`${API_BASE_URL}/retrain`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(retrainRequest)
        });
        
        if (!response.ok) {
            throw new Error('Retraining failed');
        }
        
        const result = await response.json();
        
        // Show success notification with details
        showNotification('success', 'Model Retrained! 🎉', 
            `New version ${result.version} created with ${result.training_samples} samples. ` +
            `CV Accuracy: ${(result.cv_accuracy * 100).toFixed(2)}%`);
        
        console.log('✅ Model retrained:', result);
        
        // Refresh version dropdown
        await refreshModelVersions();
        
        // Clear last prediction data
        lastPredictionData = null;
        
        // Hide retrain section
        document.getElementById('retrainSection').style.display = 'none';
        
    } catch (error) {
        console.error('Error retraining model:', error);
        showNotification('error', 'Retraining Failed', 
            'Could not retrain the model. Please try again.');
    } finally {
        // Re-enable buttons
        buttons.forEach(btn => {
            btn.disabled = false;
            btn.classList.remove('loading');
        });
    }
}

// Show notification/toast message
function showNotification(type, title, message) {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(n => n.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    
    const icons = {
        success: '✅',
        error: '❌',
        info: 'ℹ️',
        warning: '⚠️'
    };
    
    notification.innerHTML = `
        <div class="notification-header">
            <span>${icons[type] || 'ℹ️'}</span>
            <span>${title}</span>
        </div>
        <div class="notification-body">${message}</div>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideInRight 0.4s ease-out reverse';
        setTimeout(() => notification.remove(), 400);
    }, 5000);
}

// Initialize
checkAPIHealth();
refreshModelVersions(); // Load model versions on startup

// Focus on pH input when page loads
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('ph').focus();
});
