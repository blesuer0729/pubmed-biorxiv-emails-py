# Virology web scrapers

scraper.py replaces the manual process of gathering author names / author emails of new articles, which are updated frequently on these sites.

Previously, the non-technical end user was copying the names one by one per article.

## Supported sites
# Biorxiv
https://www.biorxiv.org/

## Dependencies

The app requires you install the BeautifulSoup4 python library

## Running

```bash
python3 scraper.py --site <ex: biorxiv> --start <first page> --stop <last page>
```
