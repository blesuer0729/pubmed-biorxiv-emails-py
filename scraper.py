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
    if (args.site == "biorxiv"):
        biorxiv_email_list = open("biorxiv_email_list.txt", "w+")
        biorxiv.controller(biorxiv_email_list, args.start, args.stop)
        biorxiv_email_list.close()
    elif(args.site == "pubmed"):
        pubmed_email_list = open("pubmed_email_list.txt", "w+")
        pubmed.controller(pubmed_email_list, args.start, args.stop)
        pubmed_email_list.close()
    else:
        print("The site " + args.site + " is not yet supported by the scraper.")

    print("\nrun command 'cat " + args.site + "_email_list.txt' to see results")

if __name__ == "__main__":
    main()