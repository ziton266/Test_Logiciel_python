*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}    https://www.saucedemo.com/
${USERNAME}    standard_user
${PASSWORD}    secret_sauce

*** Test Cases ***
Test Login to SauceDemo
    [Documentation]    Test the login functionality of SauceDemo
    Open Browser    ${URL}    chrome
    Input Text    id:user-name    ${USERNAME}
    Input Text    id:password    ${PASSWORD}
    Click Button    id:login-button
    Page Should Contain Element    css:.inventory_list
    Close Browser
