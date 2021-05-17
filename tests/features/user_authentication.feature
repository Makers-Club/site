Feature: User authentication
    As a visitor,
    I want to sign up or sign in using my github identity,
    So I can use the platform.

Scenario: A visitor uses their github identity to registers as a user
Given github confirms the identity of a visitor
When we register a github identity as a new user
Then a new user should exist in our database, based on the visitor identity

Scenario: A logged in user accesses a non public page
Given a user is logged in
When the user visits a non public page
Then they should be able to view the page

Scenario: A visitor tries to access a non public page
Given the visitor is not logged in
When the user visits a non public page
Then they should be redirected to a signup page with a message

# visits public page / home page
# logs out
# deletes account
# log out of all devices