import argparse
import logging

from .crawl import Crawl

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="show more",
                    action="store_true")

args = parser.parse_args()
if args.verbose:
    logging.basicConfig(level=logging.INFO)


TRANSCRIPT_PAGE = "http://www.kacl780.net/frasier/transcripts/"
c = Crawl(TRANSCRIPT_PAGE)
c.run()