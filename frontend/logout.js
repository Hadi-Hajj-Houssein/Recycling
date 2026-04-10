async function logout() {
        await fetch('http://127.0.0.1:8000/logout', {
            method: 'POST',
            credentials: 'include'
        }).catch(() => {});

        localStorage.removeItem('isLoggedIn');
        localStorage.removeItem('ecoUser');

        window.location.replace('login.html');
    }