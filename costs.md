## Estimated Costs

### Overview
- To have a functioning site, we need a domain name (ie. the site address) and also a hosting service (to connect the content to our specific address)
- If we want interaction (eg. a built-in poll-finder or registration check), the site will require some backend code, which is a little more complicated/expensive to host
- **Cheapest option** $0/yr : IF:
  - We have access to the hosting details of the curent site and editing access
  - Breakthrough is willing to have this voting resource guide as a subpage of their existing site
  - The voting site is static (ie. no complex interaction)
- **High-end option** ~$200-300/yr for:
  - A separate domain
  - A separate hosting service 
  - An interactive web application

### Domain Options
- Option 1: Buy a domain for ~$10-30/yr (GoDaddy or HostGator, etc)
    (eg. www.breakthroughvotes.org is $20.99/yr)
- Option 2: Use Breakthrough's existing domain. I don't know how the current site is hosted, but one option is to make the voting initiative a subpage of the existing site (likely at no additional cost). 
    (eg. https://www.breakthroughcollaborative.org/vote)
    
### Hosting Options
- Option 1: Host a separate *static* site on HostGator or with a similar *shared web hosting* service (approx. $3-6/month = $36-72/yr)
- Option 2: Host the page as a subpage of the existing site (possibly no cost to host, but would require coordination with the team that built/maintains the original site)
- Option 3: Host a full-stack web application (with the ability to fetch registration and poll information) on Amazon Web Services (AWS) or Heroku (approx. $10-20/month depending on webiste traffic = $120-240/yr)

### Possible Additional Costs
- **Paid Election Data APIs** If we choose to pursue an interactive site with custom voting details, we can use an API to access a database of voter information. Google has a free API with this information (Google Civic API), which is pretty good. There are also other, more comprehensive APIs with voter information such as Democracy Works (https://www.democracy.works/elections-api). Ballotpedia also has a paid API with detailed election/candidate data (https://ballotpedia.org/API-documentation).
- **Google Maps API** One possible feature of the website is a map from their home to their polling place. There is a free plan for using the Google Maps API with limited features, and there is also a paid option with pricing based on website traffic.
- **Database Storage** Another option we discussed is doing a voter pledge. If we want to store voter information and/or send reminders, we probably want a SQL database stored in the cloud. We can do this relatively cheaply on AWS or Heroku.
- **Texting Reminders** If we want to text reminders to vote and/or register to vote, we will need to purchase credits or otherwise pay a service like *Sinch* or *way2sms*. The cost is about $1 for every 100 messages.
