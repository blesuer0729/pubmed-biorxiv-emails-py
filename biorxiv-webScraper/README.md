# Content to scrape 
url - https://connect.biorxiv.org/relate/content/181 

### scraping pages (1-849)
url and loop x - https://connect.biorxiv.org/relate/content/181?page=x

### accessing links from the list
href original content link from main page (ex: http://medrxiv.org/cgi/content/short/2020.09.04.20188532)
the link is transformed when you visit the page
content page new link (ex: https://www.medrxiv.org/content/10.1101/2020.09.04.20188532v1.article-info)

### author info
span class is em-addr for corresponding author email
(ex: <span class="em-addr">test.test{at}fsa.uac.bj</span>)

span class is name for corresponding author first and last
(ex: <span class="name"> Sayak Roy </span>)

### accessing emails when script is finished
emails are printed line by line in output.txt
after having the @ symbol replaced in the string
emails will be ready for CC import

### Tracking progress

printProgressBar(0, 1, prefix="Progress:", suffix="Scrape Complete.", length=50)

printProgressBar(x + 1, 1, prefix="Progress:", suffix="Scrape Complete.", length=50)