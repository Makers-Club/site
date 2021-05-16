Feature: User authentication
    As a visitor,
    I want to sign up or sign in using my github identity,
    So I can use the platform.

Scenario: User registers with their github identity
Given github confirms their identity
Then the new user should exist in the database