# Virology web scrapers

An app that replaces the manual process of gathering author names / author emails of new articles, which are updated frequently on these sites.

Previously, the non-technical end user was copying the names one by one per article.

## Supported sites
Biorxiv (Only tested with the COVID-19 SARS-CoV-2 preprints collection)
https://www.biorxiv.org/

Pubmed (Only tested with the SARS-CoV-2 data collection)
https://pubmed.ncbi.nlm.nih.gov/

## Dependencies

The app uses the requests, BeautifulSoup4, and argparse libraries

## Running

```bash
python3 scraper.py --site <ex: biorxiv> --start <first page> --stop <last page>
```
