import argparse
import pubmed
import biorxiv

# argparse library for getting page range
parser = argparse.ArgumentParser()
parser.add_argument("--site", type=str, help="The site that the scraper will run the page range on")
parser.add_argument("--start", type=int, help="Where to start grabbing emails from in the page list")
parser.add_argument("--stop", type=int, help="The page that the scraper will finish on")
args = parser.parse_args()

# determine which site the user wanted to scrape first
def main():
    # email_list.txt is the final file shipped for import
    biorxiv_email_list = open("biorxiv_email_list.txt", "w+")
    pubmed_email_list = open("pubmed_email_list.txt", "w+")

    if (args.site == "biorxiv"):
        biorxiv.controller(biorxiv_email_list, args.start, args.stop)
    elif(args.site == "pubmed"):
        pubmed.controller(pubmed_email_list, args.start, args.stop)
    else:
        print("The site " + args.site + " is not yet supported by the scraper.")

    biorxiv_email_list.close()
    pubmed_email_list.close()
    print("\nrun command 'cat " + args.site + "_email_list.txt' to see results")

if __name__ == "__main__":
    main()