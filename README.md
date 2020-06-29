## Breakthrough Voting Initiative Repository

### Katrina Wheelan
### June 29, 2010

#### Directories:

* *StaticSite/* - A basic site with external voting resources
  * *index.html* - homepage of static site with exclusively external links
  * *contact.html* - contact us page
  * *style.css* - CSS styling code
	
* *webApp0/* - A first attempt to use the Google Civic API and scrape other polling data
  * *application.py* - Python code for a Flask application
  * *forms.py* - generic Python script to webscrape forms from a site and submit a HTTP post request
  * *formTools.py* - specific tools to webscrape and submit information for polling locations
  * *parse_address.py* - a module to parse addresses into form submission data
  * *templates/* - html templates for the application
    * *layout.html* - the basic html format
    * *index.html* - the homepage with an address form
    * *info.html* - the page containing polling location info
	
* *webApp1/* - Combining the styled static site with the web application
  * *application.py* - Python code for a Flask application
  * *formTools.py* - specific tools to webscrape and submit information for polling locations
  * *templates/* - html templates for the application
    * *layout.html* - the basic html format
    * *index.html* - the homepage
    * *info.html* - **temp**
    * *contact.html* - html page with contact information
    * *poll_form.html* - the page with an address form to fetch polling location
    * *poll_info.html* - the page to display poll information once fetched
    * *registrationForm.html* - the page with a name/address form to check registration
    * *registration.html* - displays registration information once fetched
    * *progress.html* - **TEMP** displays "page still in progress" notice
  * *static/*
     * *stylesheets/*
       * *style.css* - CSS styling for all pages

#### TO DO:

- clean up errors
  -badly formatted address
  -better message for poll finder if no upcoming election
	
- get states from a drop down menu

- post info from registered to poll finder

- do FAQs

- reminders? look into text updates

- check mobile formatting

- proof against website changes (for registration checker)

- add official links to check

- add reasons registration may not be correct (disclaimer)

- sign up on heroku to host web app

