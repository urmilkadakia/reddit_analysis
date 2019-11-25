import os
import argparse

from praw_methods import reddit_scarper


def is_valid_path(parser, arg):
    """
    Throws an error if the file does not exists at the given location
    :param parser: Object of argparse class
    :param arg: file path for which the function is going to check whether it exist or not
    :return: Return file path if file exist or throw an error of file not exist
    """
    if not os.path.exists(arg):
        parser.error("The file/folder %s does not exist!" % arg)
    else:
        return arg  # return file path


def main():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # Sub-parsers for reddit_scraper
    reddit_scraper_parser = subparsers.add_parser('reddit_scraper')
    reddit_scraper_parser.add_argument("-i", dest="input_file", required=True,
                                       help="Path to input file", type=lambda x: is_valid_path(parser, x))
    reddit_scraper_parser.add_argument("-o", dest="output_file", required=False,
                                       help="Path to output file")
    reddit_scraper_parser.add_argument("-format", dest="format", required=False, choices=["json", "csv"],
                                       help="Specify the format of the output file. Default format is json.",
                                       default="json", type=str)
    reddit_scraper_parser.add_argument("-cleaned", dest="clean_username_flag", required=False,
                                       help="Specify True if want to store a cleaned list of usernames. Default is "
                                            "False.", default=False, type=bool)
    reddit_scraper_parser.set_defaults(function=call_reddit_scraper)

    args = parser.parse_args()
    args.function(args)


def call_reddit_scraper(args):
    reddit_scarper(args.input_file, args.output_file, args.format, args.clean_username_flag)


if __name__ == "__main__":
    main()
