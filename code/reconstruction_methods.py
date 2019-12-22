import os
import zipfile
import json
from datetime import datetime as dt
import datetime


def get_user_profile_dict(input_file):
    """
    The method read the json file and generates dictionary where each key is username and corresponding value is his/her
    profile data.
    :param input_file: Path to input file
    :return: Return a dictionary where username is key and his/her reddit profile data is its value.
    """
    user_profiles = {}

    with zipfile.ZipFile(input_file, 'r') as z:
        for filename in z.namelist():
            if z.getinfo(filename).file_size == 0:
                return user_profiles
            with z.open(filename) as f:
                json_list = json.load(f)

    for user in json_list:
        user_profiles[user['data']['name']] = user

    return user_profiles


def reconstruct_data_dictionary(input_file_folder_path, number_of_users, end_date=dt.strftime(dt.now(), '%Y_%m_%d')):
    """
    This function will reconstruct the a dictionary, where keys are usernames and values are corresponding
    profile data. It uses the 1st day of the month as the base file and updates/adds the user profiles that have
    made changes in their descriptions.
    :param input_file_folder_path: Path to the folder in which input files are stored
    :param number_of_users: To identify the input file as they are named based on the number of users
    :param end_date: date up to which the function will reconstruct the description dictionary
    :return: A dictionary, where keys are usernames and values are corresponding profile data.
    """

    first_flag = 1
    users_profiles = {}
    end_date = dt.strptime(end_date, '%Y_%m_%d')
    curr_date = str(end_date.year) + '_' + str(end_date.month) + '_01'
    end_date = dt.strftime(end_date, '%Y_%m_%d')

    while curr_date != end_date:
        input_f = os.path.join(input_file_folder_path, curr_date + '_reddit_profiles_' + str(number_of_users) + '.zip')
        if os.path.exists(input_f):
            if first_flag:
                users_profiles = get_user_profile_dict(input_f)
                first_flag = 0
                continue
            temp_user_profiles = get_user_profile_dict(input_f)

            for user in temp_user_profiles:
                users_profiles[user] = temp_user_profiles[user]

        curr_date = dt.strptime(curr_date, '%Y_%m_%d')
        curr_date += datetime.timedelta(days=1)
        curr_date = dt.strftime(curr_date, '%Y_%m_%d')

    return users_profiles
