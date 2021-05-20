Feature: User authentication
    As a visitor,
    I want to sign up or sign in using my github identity,
    So I can use the platform.

Scenario: User sign up
Given a user signs up
Then we should recognize them as one of our users

Scenario: User views non-public content
Given a logged in user requests a non-public page
When the user visits a non-public page
Then they shouldn't get any errors or be redirected


