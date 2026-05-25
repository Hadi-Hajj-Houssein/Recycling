/* ══════════════════════════════════════════════════════════════════
   logout.js - Authentication and Logout Logic
   Import this in EVERY HTML file that needs authentication
   ══════════════════════════════════════════════════════════════════ */

const API_BASE = 'http://127.0.0.1:8000';
const FRONTEND_BASE = 'http://127.0.0.1:5500/frontend';

// ✅ RUN THIS ONCE on page load
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    preventBackButton();
    attachLogoutHandlers();
});

/* ═══════════════════════════════════════════════════════════════════
   1. CHECK IF USER IS LOGGED IN
   ═══════════════════════════════════════════════════════════════════ */

async function checkAuth() {
    console.log('[AUTH] Checking authentication...');
    
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    const userRole = localStorage.getItem('userRole');
    
    // ✅ If not logged in, redirect to login
    if (isLoggedIn !== 'true' || !userRole) {
        console.log('[AUTH] Not logged in, redirecting...');
        window.location.href = `${FRONTEND_BASE}/login.html`;
        return;
    }
    
    // ✅ Verify token is still valid with backend
    try {
        const res = await fetch(`${API_BASE}/company/user_requests`, {
            method: 'GET',
            credentials: 'include'
        });
        
        if (res.status === 401) {
            console.log('[AUTH] Token expired');
            forceLogout();
        } else {
            console.log('[AUTH] User authenticated');
        }
    } catch (error) {
        console.warn('[AUTH] Token verification error:', error);
    }
}

/* ═══════════════════════════════════════════════════════════════════
   2. PREVENT BACK BUTTON AFTER LOGOUT
   ═══════════════════════════════════════════════════════════════════ */

function preventBackButton() {
    window.history.pushState(null, null, window.location.href);
    
    window.addEventListener('popstate', () => {
        const isLoggedIn = localStorage.getItem('isLoggedIn');
        
        if (isLoggedIn !== 'true') {
            // Not logged in - redirect to login
            window.location.href = `${FRONTEND_BASE}/login.html`;
        }
    });
}

/* ═══════════════════════════════════════════════════════════════════
   3. LOGOUT FUNCTION (Replace your old logout())
   ═══════════════════════════════════════════════════════════════════ */

async function logout() {
    console.log('[AUTH] Logging out...');
    
    try {
        // ✅ 1. Tell backend to clear the HTTP-only cookie
        const response = await fetch(`${API_BASE}/logout`, {
            method: 'POST',
            credentials: 'include'  // Send the cookie
        });
        
        if (response.ok) {
            console.log('[AUTH] Backend logout successful');
        } else {
            console.warn('[AUTH] Backend logout failed');
        }
    } catch (error) {
        console.error('[AUTH] Logout request error:', error);
    }
    
    // ✅ 2. Clear all frontend state
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('userRole');
    localStorage.removeItem('userId');
    localStorage.removeItem('userName');
    
    // ✅ 3. Redirect to login (can't go back)
    window.location.replace(`${FRONTEND_BASE}/login.html`);
}

/* ═══════════════════════════════════════════════════════════════════
   4. FORCE LOGOUT (when token expires)
   ═══════════════════════════════════════════════════════════════════ */

function forceLogout() {
    console.log('[AUTH] Force logout - token expired');
    
    // Clear frontend state
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('userRole');
    localStorage.removeItem('userId');
    localStorage.removeItem('userName');
    
    // Try to clear backend cookie (don't wait for response)
    fetch(`${API_BASE}/logout`, {
        method: 'POST',
        credentials: 'include'
    }).catch(() => {});
    
    // Show message and redirect
    alert('Your session has expired. Please login again.');
    window.location.replace(`${FRONTEND_BASE}/login.html`);
}

/* ═══════════════════════════════════════════════════════════════════
   5. ATTACH LOGOUT TO ALL LOGOUT BUTTONS
   ═══════════════════════════════════════════════════════════════════ */

function attachLogoutHandlers() {
    // Find all logout buttons and attach click handler
    const logoutButtons = document.querySelectorAll(
        '[data-logout], .logout-btn, #logoutBtn, #logoutSidebar, #logoutDropdown, .nav-item.logout-btn'
    );
    
    logoutButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            logout();
        });
    });
}

/* ═══════════════════════════════════════════════════════════════════
   6. TOKEN EXPIRATION CHECK (every 5 minutes)
   ═══════════════════════════════════════════════════════════════════ */

setInterval(() => {
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    
    if (isLoggedIn !== 'true') return;
    
    fetch(`${API_BASE}/company/user_requests`, {
        method: 'GET',
        credentials: 'include'
    })
    .then(res => {
        if (res.status === 401) {
            console.log('[AUTH] Periodic check: Token expired');
            forceLogout();
        }
    })
    .catch(err => console.warn('[AUTH] Periodic check error:', err));
}, 5 * 60 * 1000); // Every 5 minutes