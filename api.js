async function apiRequest(url,method = 'GET',body = null){
    const token  = localStorage.getItem('access_token');
    if(!token){
        window.location.href ='login.html';
        return null;
    }
    // const options = {
    //     options.headers['Content-Type'] = "application/json";

    // }
    const options = {
        method: method,
        headers: {
            'Authorization': `Bearer ${token}`,
        }
    };
    if(body){
        options.headers['Content-Type'] = "application/json";
        options.body = JSON.stringify(body);
    }
    const response = await fetch(url,options);
    if(response.status==400 || response.status==401){
        localStorage.clear();
        window.location.href ='login.html';
        return null;
    }
    return await response.json();
}