# WebScraping_Heroku

This code will allow you to scrape a page automatically, process it and email it to you based on a user defined schedule. 
This snippet of code will allow you to deploy your python script to Heroku and run a scheduler. This is meant for free account that do not have a credit card on file. You would need to download add-ons but to do so you need a credit card on file. This code allows you to run a scheduler without a credit card on file. 

## Instructions
1) Clone the repo
2) Get your API key from sendgrid to send emails
3) Update apikey.py with your API key, to and from email addresses
4) Ensure you keep the Procfile and requirements.txt in the main file
5) Edit scraper.py to the schedule you would like to use (near bottom)

## Deployment to Heroku Instructions (Heroku Git)
1) Sign up for a free heroku account if you havent already done so
2) Type heroku login --> This will take you to a web based login page
3) cd to your directory on your local drive
4) Type 'git init'
5) Type 'heroku git:remote -a [Name of Your APP]'
6) Type 'git add .'
7) Type ' git commit -am "version 1"'
8) Type 'git push heroku master'
9) Now you need to allocate a dyno to do the work. Type 'heroku ps:scale worker=1'
10) If you want to check to logs to make sure its working type 'heroku logs --tail'

Now your code will continue to run until you stop the dyno. To stop it scale it down using the command 'heroku ps:scale worker=0'
