async function logout() {
    await fetch('/logout', {  // use relative URL, same origin
        method: 'POST'
        // no credentials needed, same origin sends cookies automatically
    }).catch(() => {});

    // remove these — you're not using localStorage for auth anymore
    // localStorage.removeItem('isLoggedIn');
    // localStorage.removeItem('ecoUser');

    window.location.replace('/static/login.html');  // full path
}