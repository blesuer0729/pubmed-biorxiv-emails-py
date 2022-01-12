# Virology email collector

A script that can collect author emails and/or names from sites related to virology. Using the BS4 python library the authors are gathered into a .txt file that can be pasted into Constant Contact for import

## Supported sites

Biorxiv (Only tested with the COVID-19 SARS-CoV-2 preprints collection)
<https://www.biorxiv.org/>

Pubmed (Only tested with the SARS-CoV-2 data collection)
<https://pubmed.ncbi.nlm.nih.gov/>

## Running

```bash
python3 scraper.py --site <ex: biorxiv> --start <first page> --stop <last page>
```
