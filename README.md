## Breakthrough Voting Initiative Repository

### Katrina Wheelan, July 16, 2020

The Breakthrough Collaborative's Voting Initiative is a central site for accessible voting resources in all states that Breakthrough serves. Content is translated into Spanish and Chinese (depending on the state).

This repository contains a Python Flask application. The demo branch is deployed at: https://breakthrough-voting-initiative.herokuapp.com/
The default branch is the working branch for this application, deployed at: https://bt-voting.herokuapp.com/. We use the Google Civic Data API for polling data and scrape registration data from Vote.org. All FAQ information comes from individual states' Secretary of State sites.


#### Directories:
 * *application.py* - Python code for running the Flask application
 * *util.py* - specific tools to webscrape and submit information for polling locations and registration information
 * *templates/* - html templates for the application
   * *layout.html* - the basic html format
   * *layout_mandarin.html* - basic html format for Mandarin
   * *CA/*
     * *english/*
       * *home.html*
       * *faqs.html*
       * *register.html*
     * *mandarin/*
       * *home.html*
       * *faqs.html*
       * *register.html*
     * *spanish/*
       * *home.html*
       * *faqs.html*
       * *register.html*
   * *FL/*
     * *english/*
       * *home.html*
       * *faqs.html*
       * *register.html*
     * *spanish/*
       * *home.html*
       * *faqs.html*
       * *register.html*
   * *national/*
      * *english/*
        * *poll_form.html* - the page with an address form to fetch polling location
        * *poll_info.html* - the page to display poll information once fetched
        * *registrationForm.html* - the page with a name/address form to check registration
        * *registration.html* - displays registration information once fetched
      * *mandarin/*
        * *poll_form.html* - the page with an address form to fetch polling location
        * *poll_info.html* - the page to display poll information once fetched
        * *registrationForm.html* - the page with a name/address form to check registration
        * *registration.html* - displays registration information once fetched
      * *spanish/*
        * *poll_form.html* - the page with an address form to fetch polling location
        * *poll_info.html* - the page to display poll information once fetched
        * *registrationForm.html* - the page with a name/address form to check registration
        * *registration.html* - displays registration information once fetched
 * *static/*
   * *stylesheets/*
     * *style.css* - CSS styling for all pages
   * *images/*
     * *menu_icon.png* - toggle icon for mobile version
     * *stockImgs/* - images not currently in use
     * *icons/*
       * *english/* - contains homepage icons in English
       * *chinese/* - contains homepage icons in Chinese
       * *spanish/* - contains homepage icons in Spanish
     * *favicon/* - icon for browser
       * *favicon.ico*
       * *favicon-16x16.png*
       * *favicon-32x32.png*
   * *JS/*
     * Javascript scripts
