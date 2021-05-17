Feature: User authentication
    As a visitor,
    I want to sign up or sign in using my github identity,
    So I can use the platform.

Scenario: A visitor uses their github identity to registers as a user
Given github confirms the identity of a visitor
When we register a github identity as a new user
Then a new user should exist in our database, based on the visitor identity
