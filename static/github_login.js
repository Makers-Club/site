function github_login(client_id) {
    const url = `https://github.com/login/oauth/authorize?client_id=${client_id}&scope=user`;
    window.location.href = url;
}