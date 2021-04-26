---
name: New Route
about: A template for new routes
title: 'Route: `POST example.com/user/posts`'
labels: back-end
assignees: ''

---

* **Description:** _One to three sentence description of what the route does, how it's used, and what data it needs_
* **File:** `routes/users.py`
* **Function:** `def new_post(text)`
    * Parameters:
        * `text` (str)
    * Return (or Redirect):
        * `templates/post_success.html`
    * Other data sources:
        * `GET example.com/api/users`
