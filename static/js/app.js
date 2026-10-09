// Authentication removed as requested

// Unregister any rogue service workers (common issue on localhost)
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.getRegistrations().then(function(registrations) {
        for(let registration of registrations) {
            registration.unregister();
        }
    });
}

// Active Nav state
document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    const navId = 'nav-' + path.replace('/', '');
    const navEl = document.getElementById(navId);
    if(navEl) navEl.classList.add('active');
    
    // Fetch Settings for header
    if(path !== '/login' && path !== '/') {
        fetch('/api/settings')
            .then(res => res.json())
            .then(data => {
                if(data.shop_name) {
                    document.getElementById('shop-name-header').innerText = data.shop_name;
                }
            });
    }
});

function logout() {
    localStorage.removeItem('token');
    window.location.href = '/login';
}

function showToast(message) {
    const toast = document.getElementById('toast');
    toast.innerText = message;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 3000);
}

// Global modal helpers
function openModal(id) {
    document.getElementById(id).classList.add('show');
}
function closeModal(id) {
    document.getElementById(id).classList.remove('show');
}
