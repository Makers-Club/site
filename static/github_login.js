// deprecated
function github_login(client_id) {
    window.location.href = "{{ url_for('auth.send_visitor_to_github') }}";
}