// GreenLink JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    console.log('GreenLink platform loaded successfully!');
    
    // Initialize any interactive features here
    initializeLikeButtons();
    initializeFollowButtons();
});

function initializeLikeButtons() {
    const likeButtons = document.querySelectorAll('.like-btn');
    likeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            // AJAX like functionality would go here
            console.log('Like button clicked');
        });
    });
}

function initializeFollowButtons() {
    const followButtons = document.querySelectorAll('.follow-btn');
    followButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            // AJAX follow functionality would go here
            console.log('Follow button clicked');
        });
    });
}

// Toast notification function
function showToast(message, type = 'success') {
    // Create toast notification
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} position-fixed top-0 end-0 m-3`;
    toast.style.zIndex = '9999';
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    // Remove toast after 3 seconds
    setTimeout(() => {
        toast.remove();
    }, 3000);
}
