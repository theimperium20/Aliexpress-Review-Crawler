# Aliexpress-Review-Crawler
A Python script to scrape all reviews from the given aliexpress product url. The CSV is formatted such that it supports the **Woocommerce Plugins** to import reviews from **CSV**.
The script also fetches the URL of the image attachements in the reviews and seller replies to reviews.
Aliexpress does not display the names of the buyers. So the script creates random names from the files first.csv and last.csv.

### How to run the program?
- Clone the repo by running `git clone https://https://github.com/theimperium20/Aliexpress-Review-Crawler.git` or by the clicking the green `Clone or download` button
- Install all the requirements by running `pip3 install -r requirements.txt` or `pip install -r requirements.txt`.
- Use **crawler_linux.py** if you use **linux** or **crawler_windows.py** if you **windows** operating systems.
- Head over to Aliexpress Product Page and copy the **URL** of the product you want to scrape the reviews for.
- Replace the **"ALIEXPRESS PRODUCT URL HERE"** placed holder text with the URL you just copied on the **crawler script** based on the operating system you are running.
- Replace the **'PRODUCT HANDLE'** placeholder with the product handle of your **Woocomerce Product**
- Specify the number of pages of reviews to scraped in the **pages** placedholder of the crawler script.
- Replace the **"NAMEYOURFILE.csv"** placeholder with the desired name for your output csv file. 
- You can change the **state** of the review by changing the **state = Published** placeholder
- After making the required changes run the program wait for the program to finish.
- The ouput csv file is generated in your present working directory with the name you provided.

>**Note:** Aliexpress does not display the names of the reviewers, so this script **randomly generates names** from the names in the files **first.csv** and **last.csv**. As the name suggests, first names are generated from the first.csv and last name are generated from last.csv. If you want to add your own names, you can edit the csv file.

### Breaking down the CSV

![Image of CSV](https://github.com/theimperium20/Aliexpress-Review-Crawler/blob/master/csv.PNG)

- `product_handle` is your woocommerce product handle
- `state` describes the state of the review, the value of this depends on the plugin you use. Usually it is `Published` or `Not Published`.
- `rating` the number of start ratings the reviewer has left for the product
- `title` is the heading of the review
- `seller` is the store that sold the product
- `contact` stores the email of the reviewer if he has given one.
- `location` is the country code of the reviewer
- `author` is the fake name created randomly from the names in the first.csv and last.csv
- `body` contains the actual review text. If there are any attachments in the review, the url is contained with `@({})`. `**Example :** The product is just amazing. 5 starts.{https://urlofthecontent.here}`
- `reply` contains the reply if any made by the seller. 
- `created_at` has the timestamp of the review
- `replied_at` is the timestamp of the seller reply
>**Note :** The csv follows a format that most reviews import plugins on Woocommerce support. However, some plugins might expect a different format. Use a plugin that let's you map column headers to manually select the map the columns to woocommerce fields.
