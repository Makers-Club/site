Feature: User authentication
    As a visitor,
    I want to sign up or sign in using my github identity,
    So I can use the platform.

Scenario: User sign up
Given a user signs up
Then we should recognize them as one of our users

Scenario: A logged in user visits the home page
Given the user was already logged in
When they visit the home page
Then they should be sent to their dashboard

Scenario: A visitor visits the homepage
Given the visitor is not signed in
When they visit the home page
Then they should see the landing page

Scenario: A logged in user accesses a non public page
Given a user is logged in
When the user visits a non public page
Then they should be able to view the page

Scenario: A visitor tries to access a non public page
Given the visitor is not logged in
When the user visits a non public page
Then they should be redirected to a signup page with a message

# logs out
# deletes account
# log out of all devices