# Content to scrape 
url - https://journals.asm.org/content/covid-19
on the articles main page the list is stored under <ul class="journal-list"> for each page

### scraping pages (1-849)
The first page is the topic, for example:
https://journals.asm.org/content/covid-19

Page two is always 'recent', for example:
https://journals.asm.org/content/covid-19/recent/

from then on page three is recent_page2, etc, for example:
https://journals.asm.org/content/covid-19/recent_page2 (page 3)
https://journals.asm.org/content/covid-19/recent_page3 (page 4)

### accessing links from the list
The link does not transform between the article list and the content page for this site
You can grab the URL for the hyperlink straight from the aricle list
no splitting and rebuilding strings :)

### author info
You will have to build a string to get the email from each article page however by adding /article/info, for example:
https://jvi.asm.org/content/93/2/e00875-18/article-info
The email is under <span class="em-addr">

### accessing emails when script is finished
emails are printed line by line in email_list.txt
after having the @ symbol injected into the string
emails will be ready for CC import

### Tracking progress ????????????

printProgressBar(0, 1, prefix="Progress:", suffix="Scrape Complete.", length=50)

printProgressBar(x + 1, 1, prefix="Progress:", suffix="Scrape Complete.", length=50)