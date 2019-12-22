import os
import logging
from datetime import datetime as dt
import json
import csv
import zipfile
import praw
import time
import re
import prawcore
import praw.exceptions

from api_keys import client_secret, client_id, client_username
from logger import log_reddit_error
from reconstruction_methods import reconstruct_data_dictionary

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

filename = os.path.join(os.getcwd(), 'logs/praw_methods_' + dt.now().strftime("%m_%Y") + '.log')

if not os.path.exists(filename):
    open(filename, 'w+').close()

file_handler = logging.FileHandler(filename)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def _flatten_json(y):
    """
    Method to convert the multilayer JSON to 1 dimension row vector
    :return: flatten json dictionary
    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        else:
            out[name[:-1]] = x

    # Recursively call itself with the child dictionary
    flatten(y)
    return out


def reddit_scarper(input_file_path, output_file_path, format=json, clean_username_flag=False):
    """
    Method to send the api calls to reddit and get the user data in the json format. The method stores all the
    data in the user specified format(json or csv) in the zip file format to reduce the storage space and also
    prints out the list of failed user ids.
    :param input_file_path: User input for path to the input file
    :param output_file_path: User input for path to the output folder
    :param format: format of output file json or csv
    :param clean_username_flag: a flag to store the list of usernames for which we get the data without any error.
    Pass True to store the list as csv file.
    """

    try:
        # praw OAuthHandler object
        reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent='my reddit_analysis agent',
                             username=client_username, password="")
        # This generates exception if the credentials are wrong
        reddit.auth.scopes()
    except prawcore.exceptions.PrawcoreException as e:
        log_reddit_error(logger, e)
        del reddit
        exit(1)

    input_file = open(input_file_path, 'r')
    number_of_users = len(input_file.readlines())
    time_str = dt.now().strftime("%Y_%m_%d")

    if format == 'csv':
        output_file_name = time_str + '_reddit_profiles_' + str(number_of_users) + '.csv'
        output_file = open(output_file_path + output_file_name, "w+")
        output_file_csv = csv.writer(output_file)
    else:
        output_file_name = time_str + '_reddit_profiles_' + str(number_of_users) + '.txt'
        output_file = open(output_file_path + output_file_name, "w+")

    if clean_username_flag:
        clean_username_file_name = time_str + '_reddit_userid_list_' + str(number_of_users) + '.csv'
        clean_username_file = csv.writer(open(output_file_path + clean_username_file_name, "w+"))

    zip_file_name = time_str + '_reddit_profiles_' + str(number_of_users) + '.zip'

    # username_failed contains a list of user IDs that fail to extracted
    username_failed = []
    data_list = []

    inputfile = open(input_file_path, 'r')
    for line in inputfile:
        username = line.strip()
        # Retry 3 times if there is a Twitter overfull/internal error
        retry_count = 3
        while True:
            try:
                user_about = reddit.redditor(name=username)._fetch_data()
                if clean_username_flag:
                    clean_username_file.writerow([username])
            except prawcore.exceptions.PrawcoreException as e:
                # Extending the list of failed usernames after each call to api
                http_exception_code = int(re.findall(r'[0-9]+\sHTTP', str(e))[0].split(" ")[0])
                if retry_count > 0 and http_exception_code in {500, 502, 503, 504}:
                    time.sleep(60)
                    retry_count -= 1
                    continue
                username_failed.append(username)
            break

        # Store the converted user profile data in the output file
        if format == "json":
            data_list.append(user_about)
        # If defined format is csv then the following code snippet will store the user status
        # data into csv format in the output file
        else:
            # Function will return the 1 dimensional row vector for the given profile
            status = _flatten_json(user_about)
            data_list.append(status)
    # Convert the original file to zip file to reduce the storage space
    if format == 'json':
        # retrieve updated records only
        if time_str.split('_')[-1] != '01':
            data_list = _generate_longitudinal_data(output_file_path, number_of_users, data_list)

        output_file.write(json.dumps(data_list))
    else:
        # If we are writing the first line of the output file then following code will
        # write the headers of each column in the output file
        output_file_csv.writerow(data_list[0].keys())
        if data_list:
            for row in data_list:
                output_file_csv.writerow(row.values())
    output_file.close()
    os.chdir(output_file_path)
    zipf = zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED)
    zipf.write(output_file_name)
    zipf.close()
    os.remove(output_file_name)

    logger.info('Number of successful ID:' + str(number_of_users - len(username_failed)) + ' and '
                + 'Number of failed ID:' + str(len(username_failed)))


def _generate_longitudinal_data(output_file_path, number_of_users, data_list):
    """
    This function will take the array of all the profiles and return an array of profiles that have made changes in
    their descriptions.
    :param output_file_path: User input for path to the output folder
    :param number_of_users: To identify the input file as they are named based on the number of users
    :param data_list: An array of all the profiles
    :return: an array of profiles that have made changes in their descriptions
    """
    user_profiles = reconstruct_data_dictionary(output_file_path, number_of_users)
    print(user_profiles)

    # When no base file found
    if not user_profiles:
        return data_list

    updated_user_profiles = []
    for profile in data_list:
        if profile['data']['name'] in user_profiles and \
                profile['data']['subreddit']['public_description'] == \
                user_profiles[profile['data']['name']]['data']['subreddit']['public_description']:
            continue
        updated_user_profiles.append(profile)

    return updated_user_profiles
