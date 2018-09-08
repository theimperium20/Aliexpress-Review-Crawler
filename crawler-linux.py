import requests
from bs4 import BeautifulSoup
import csv
import random

firstName = []
lastName = []

firstnamefile = open('first.csv', 'r',encoding='utf-8')
reader = csv.reader(firstnamefile)

for row in reader:
    firstName.append(row[0])
    
lastnamefile = open('last.csv', 'r',encoding='utf-8')
reader = csv.reader(lastnamefile)

for row in reader:
    lastName.append(row[0])

def AliexpressCrawler(pages=1000,URL="",product_handle="Default",filename="new.csv"):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
    # Output  product_handle,state,rating,title,seller,contact,
    #         location,buyerReview,sellerReply,buyerReviewDate,sellerReviewDate
    
    state = 'published'
    rating = 0
    title = ""
    seller = ""
    contact = "null@null.com"
    location = ""
    httpRef = "http:"
    
    r = requests.get(URL,headers=header)
    soup = BeautifulSoup(r.content, "lxml")
    feedbackURL = ""
    
    file = open(filename, 'w+')
    file.close()
    
    csv_file = open(filename,'w', newline='', encoding='utf-8' )
    writer = csv.writer(csv_file)
    writer.writerow(['product_handle','state','rating','title','seller','contact','location','author','body','reply','created_at','replied_at'])
    
    if r.status_code == 200: # Checks Internet connection
        with requests.Session() as s:
            html = r.content
            rating = ( soup.find('div',{'class':'product-star-order util-clearfix'}) ).find('span' , {'class' , 'percent-num' }).text  #AVERAGE PRODUCT RATING
            title = (soup.find('title').getText()).rsplit("-",1)[0]
            seller = (soup.find('div',{'class':'store-info-wrap'})).find('a', {'class':'store-lnk'}).text
            # contact = httpRef+((soup.find('div',{'class','ui-box contact-seller-email'})).find('a')).get('href')
                                        # Contact only works if you are logged in Aliexpress
            tempLocation = (soup.find('div',{'class':'store-summary'})).find('span',{'class':'store-location'}).text
            location = (tempLocation.strip()).replace(' ','')  #Fetches location of Seller
        
            #Fetching feedback of product
            feedbackURL = httpRef+(soup.find('div',{'class':'main-content'})).find('iframe').get('thesrc')
            print(feedbackURL)
            r = requests.get(feedbackURL,headers=header)
            soup = BeautifulSoup(r.content, "lxml")
        #    html = r.content
        #    print(html)
            
            page = (soup.find_all('div', {'class' , 'feedback-list-wrap' } ))[0]
            
            countryArray = []
            buyerCountryList = page.find_all('div',{'class':'user-country'})
            for each in buyerCountryList:
                countryArray.append( (each.find('b')).getText() )
                       
            indepth = page.find_all('div' , {'class':'f-content'})  
            
            ratingArray = []
            rating = (page.find_all('div',{'class':'f-rate-info'}))
            for each in rating:
                each.find_all('span',{'class':'star-view'})
                eachRating = (((each.find('span') ).find('span')).get('style') ).split(":")[-1][:-1]
                eachRating = (5*(int(eachRating)/100))
                ratingArray.append(eachRating)
            
            counter = -1
            for item in indepth:
                try:
                    sellerReply =  (((item.find('dl',{'class':'seller-reply'}))).find('dd',{'class':'r-fulltxt'})).text
                    sellerReviewDate =  (((item.find('dl',{'class':'seller-reply'}))).find('dd',{'class':'r-time'})).text
                except:
                    sellerReply = ""
                    sellerReviewDate = ""
                    
                try:
                    buyerPicArray = ""
                    buyerPictures = (item.find('dd',{'class':'r-photo-list'})).find_all('li',{'class':'pic-view-item'})
                    for image in buyerPictures:
                        buyerPicArray = buyerPicArray + "{" +(image.find('img').get('src')) + "};"
                except:
                    buyerPicArray = ""
                    pass
                
                buyerReviewDate =  (item.find('dd',{'class':'r-time'})).text 
                buyerReview = ((item.find('dt')).getText()).strip()
                name = random.choice(firstName) + " "+ random.choice(lastName)
                
                counter = counter + 1
                
                templist = [product_handle,state,ratingArray[counter],title,seller,contact,countryArray[counter],name,buyerReview.strip() + " "+ buyerPicArray ,sellerReply,buyerReviewDate,sellerReviewDate]
                writer.writerow(templist)
                print("Review Added")
                
                print('buyerReviewDate' ,  buyerReviewDate)
                print('buyerReview' , buyerReview)
                print('sellerReviewDate ' , sellerReviewDate)
                print('sellerReply ' , sellerReply)
                print('Rating ',ratingArray[counter])
                print('buyerPicArray',buyerPicArray)
                print('countryArray' , countryArray[counter])
                print('--------------------')
                
    from selenium import webdriver
    driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
    driver.get(feedbackURL)
    
    for page in range(2,pages+1):
        print("Page "+str(page))
        containers = driver.find_elements_by_xpath('//div[@class="ui-pagination-navi util-left"]')
        for item in containers:
            name = item.find_element_by_xpath('//a[@class="ui-goto-page" and @pageno= "'+str(page)+'"]')
                                            #If throws Error reviews are finished 
        name.click()
        
        html = driver.page_source            
        soup = BeautifulSoup(html, "lxml")
        
        html = (soup.find_all('div', {'class' , 'feedback-list-wrap' } ))[0]
        
        countryArray = []
        buyerCountryList = html.find_all('div',{'class':'user-country'})
        for each in buyerCountryList:
            countryArray.append( (each.find('b')).getText() )
        
        indepth = html.find_all('div' , {'class':'f-content'})  
        
        ratingArray = []
        rating = (html.find_all('div',{'class':'f-rate-info'}))
        for each in rating:
            each.find_all('span',{'class':'star-view'})
            eachRating = (((each.find('span') ).find('span')).get('style') ).split(":")[-1][:-1]
            eachRating = (5*(int(eachRating)/100))
            ratingArray.append(eachRating)
        
        counter = -1
        for item in indepth:
            try:
                sellerReply =  (((item.find('dl',{'class':'seller-reply'}))).find('dd',{'class':'r-fulltxt'})).text
                sellerReviewDate =  (((item.find('dl',{'class':'seller-reply'}))).find('dd',{'class':'r-time'})).text
            except:
                sellerReply = ""
                sellerReviewDate = ""
                
            try:
                buyerPicArray = ""
                buyerPictures = (item.find('dd',{'class':'r-photo-list'})).find_all('li',{'class':'pic-view-item'})
                for image in buyerPictures:
                    buyerPicArray = buyerPicArray + "@" + "{" + (image.find('img').get('src'))+ "};"
            except:
                buyerPicArray = ""
                pass
                    
            buyerReviewDate =  (item.find('dd',{'class':'r-time'})).text 
            buyerReview = (item.find('dt')).getText() 
            name = random.choice(firstName) + " "+ random.choice(lastName)
            counter = counter + 1
            templist = [product_handle,state,ratingArray[counter],title,seller,contact,countryArray[counter],name,buyerReview.strip() + " "+ buyerPicArray ,sellerReply,buyerReviewDate,sellerReviewDate]
            writer.writerow(templist)
            
            print("Review Added")
            print('buyerReviewDate' ,  buyerReviewDate)
            print('buyerReview' , buyerReview)
            print('sellerReviewDate ' , sellerReviewDate)
            print('sellerReply ' , sellerReply)
            print('Rating ',ratingArray[counter])
            print('buyerPicArray',buyerPicArray)
            print('countryArray' , countryArray[counter])
            print('--------------------')
    
    csv_file.close()


URL = "ALIEXPRESS PRODUCT URL HERE"
product_handle = 'PRODUCT HANDLE'
pages = 500
filename = "NAMEYOURFILE.csv"

AliexpressCrawler(pages,URL,product_handle,filename)

    

