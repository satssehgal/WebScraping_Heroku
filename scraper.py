from bs4 import BeautifulSoup as bs4
import requests
import pandas as pd
import base64
import os.path
from apikey import *
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition, ContentId)
import schedule
import time
from datetime import datetime
import pytz

def job():
    prices=[]
    stars=[]
    titles=[]
    urlss=[]

    pages_to_scrape=10
    pages=[('http://books.toscrape.com/catalogue/page-{}.html').format(i) for i in range(1,pages_to_scrape+1)]

    for item in pages:
        page = requests.get(item)
        soup = bs4(page.text, 'html.parser')
        for i in soup.findAll('h3'):
            titles.append(i.getText())
        for j in soup.findAll('p', class_='price_color'):
            prices.append(j.getText())
        for s in soup.findAll('p', class_='star-rating'):
            for k,v in s.attrs.items():
                stars.append(v[1])
        divs =soup.findAll('div', class_='image_container')
        for thumbs in divs:
            tgs=thumbs.find('img',class_='thumbnail')
            urls='http://books.toscrape.com/'+str(tgs['src'])
            newurls=urls.replace("../","")
            urlss.append(newurls)
    data={'Title': titles, 'Prices': prices, 'Stars':stars, "URLs":urlss}
    df=pd.DataFrame(data=data)
    df.index+=1
    directory = os.path.dirname(os.path.realpath(__file__))
    filename = "scrapedfile.csv"
    file_path = os.path.join(directory,'csvfiles/', filename)
    df.to_csv(file_path)

    with open(file_path, 'rb') as f:
        data = f.read()
        f.close()

    encoded = base64.b64encode(data).decode()
    message = Mail(
    from_email=FROM_EMAIL,
    to_emails=TO_EMAIL,
    subject='Your File is Ready',
    html_content='<strong>Attached is Your Scraped File</strong>')
    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_type = FileType('text/csv')
    attachment.file_name = FileName('scraped.csv')
    attachment.disposition = Disposition('attachment')
    attachment.content_id = ContentId('Example Content ID')
    message.attachment = attachment
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
         print(e)



# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
schedule.every().day.at('13:58').do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1) # wait one minute