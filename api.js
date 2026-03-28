async function apiRequest(url, method = 'GET', body = null) {
    const options = {
        method: method,
        credentials: 'include',
        headers: {}
    };

    if (body) {
        options.headers['Content-Type'] = 'application/json';
        options.body = JSON.stringify(body);
    }

    const response = await fetch(`http://127.0.0.1:8000${url}`, options);

    if (response.status === 401) {
        window.location.href = 'http://127.0.0.1:5500/frontend/login.html';
        return null;
    }

    if (response.status === 400) {
        const errorData = await response.json();
        alert(errorData.detail || "Bad request");
        return null;
    }

    if (!response.ok) {
        const text = await response.text();
        throw new Error(`Request failed: ${response.status} - ${text}`);
    }

    return await response.json();
}