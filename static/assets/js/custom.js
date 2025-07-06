// Custom JavaScript for FreelanceCalc

// Auto-hide toasts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide toasts
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            const bsToast = new bootstrap.Toast(toast);
            bsToast.hide();
        }, 5000);
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Fix dropdown positioning
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
        const menu = dropdown.querySelector('.dropdown-menu');
        if (menu) {
            // Ensure dropdown appears above other elements
            menu.style.zIndex = '10000';
            
            // Handle dropdown positioning
            dropdown.addEventListener('show.bs.dropdown', function() {
                const rect = this.getBoundingClientRect();
                const menu = this.querySelector('.dropdown-menu');
                
                // Check if dropdown would go off-screen
                const menuHeight = menu.offsetHeight;
                const spaceBelow = window.innerHeight - rect.bottom;
                const spaceAbove = rect.top;
                
                if (spaceBelow < menuHeight && spaceAbove > spaceBelow) {
                    menu.classList.add('dropup');
                } else {
                    menu.classList.remove('dropup');
                }
            });
        }
    });
});

// Ensure toasts are always visible
function ensureToastVisibility() {
    const toastContainer = document.querySelector('.toast-container');
    if (toastContainer) {
        toastContainer.style.zIndex = '10000';
        toastContainer.style.position = 'fixed';
        toastContainer.style.top = '20px';
        toastContainer.style.right = '20px';
    }
}

// Call on page load
document.addEventListener('DOMContentLoaded', ensureToastVisibility);

// Call on window resize
window.addEventListener('resize', ensureToastVisibility); 