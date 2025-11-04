// Main JavaScript file for Web Mapping Platform
// Global utilities and common functionality

// Global variables
window.MapTech = window.MapTech || {};

// Initialize common functionality when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeCommonFeatures();
});

function initializeCommonFeatures() {
    // Initialize tooltips
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Add loading states to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                const originalText = submitButton.innerHTML;
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Loading...';
                
                // Re-enable after 3 seconds as fallback
                setTimeout(() => {
                    submitButton.disabled = false;
                    submitButton.innerHTML = originalText;
                }, 3000);
            }
        });
    });
}

// Utility functions
window.MapTech.utils = {
    // Show notification message
    showMessage: function(message, type = 'info', duration = 3000) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        messageDiv.style.top = '20px';
        messageDiv.style.right = '20px';
        messageDiv.style.zIndex = '9999';
        messageDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(messageDiv);
        
        // Auto-remove after specified duration
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.parentNode.removeChild(messageDiv);
            }
        }, duration);
    },

    // Format coordinates
    formatCoordinates: function(lat, lng, precision = 6) {
        return `${lat.toFixed(precision)}, ${lng.toFixed(precision)}`;
    },

    // Validate coordinates
    isValidCoordinate: function(lat, lng) {
        return !isNaN(lat) && !isNaN(lng) && 
               lat >= -90 && lat <= 90 && 
               lng >= -180 && lng <= 180;
    }
};

// Console welcome message
console.log('%c🗺️ MapTech Solutions Web Mapping Platform', 'color: #0d6efd; font-size: 16px; font-weight: bold;');
console.log('%cDeveloped for CMPU4058 - Advanced Web Mapping', 'color: #6c757d;');
