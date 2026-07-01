API_BASE = "https://recycling-kx0n.onrender.com";
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

    const response = await fetch(`${API_BASE}${url}`, options);

    if (response.status === 401) {
        window.location.href = `${API_BASE}/login.html`;
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