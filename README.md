# reddit_analysis
A python project to study patterns in identity change as revealed by the edits users make to their online profiles using 
data from Reddit.

## Install instructions

### Creating a Reddit developer account
- You need to have a Reddit account. If you don't have to create one.
- Go to [Reddit preferences](https://www.reddit.com/prefs/apps). 
- If you want to use an **existing app** select one or click on **create app**.
- Fill the application form and click on **create app**.

### PRAW
- **PRAW** is a wrapper around the Reddit API.
- For more information on tweepy visit: [Reddit Documentation](https://www.reddit.com/dev/api/).

### Updating the api_keys.py file
- On the preferences page of Reddit, follow **your developed applications -> edit** and you will find your 
client_secret and personal user script (client id).
- Copy and paste these keys to the respective variables and save the file.

### Downloading and installing dependencies
- To download and install dependencies run the following command:
    ```
    sh install.sh
    ```
  
## Usage
1. **praw_methods.reddit_scraper(input_file, output_file, format, size, clean_userid)**
    - Method to send the api calls to twitter and get the user data in the json format. The method stores all the data 
    in the user specified format(json or csv) in the zip file format to reduce the storage space and also prints out 
    the list of failed user ids.
    - **Parameters**:
        - **input_file_path**: Path to the input file
        - **output_file_path**: Path to the output file
        - **format**: format of output file json or csv
        - **clean_username_flag**: A flag to store the list of user ids for which we get the data without any error. 
        Pass True to store the list as csv file
        
2. **reconstruction_methods.get_user_profile_dict(input_file)**
    - The method read the json file and returns a dictionary where each key is user id and corresponding value is 
    his/her profile data.
    - **Parameters**:
        - **input_file**: Path to input file

3. **reconstruction_methods.reconstruct_data_dictionary( input_file_folder_path, number_of_users, end_date)**
    - This function will reconstruct the a dictionary, where keys are user ids and values are corresponding profile 
    data. It uses the 1st day of the month as the base file and updates/adds the user profiles that have made changes 
    in their descriptions.
    - **Parameters**:
        - **input_file_folder_path**: Path to the folder in which input files are stored
        - **output_file**: Path to the output file
        - **number_of_users**: To identify the input file as they are named based on the number of users
        - **end_date**: Date up to which the function will reconstruct data. Default is today.
        
## Example
- Use the following command to run any function on terminal:
    ```
    python driver.py <function name> <args>
    ```
- Pass `-h` as argument for help menu.
- In similar fashion one can run any other function. To get help 
regarding the function specific arguments run:
    ```
    python driver.py <function name> -h
    ```
- For example, to run the **reddit_scraper** with format as json, clean_username_flag as True, run the following 
command:
    ```
    python driver.py reddit_scraper -i <input file> -o <output file> -format json -cleaned True
    ``` 

## Logs
- All the errors, exceptions and information status generated Reddit API and PRAW during a call to the function  that 
uses them are written in the respected month's log file.
- For more information please refer to the 
[Reddit API status codes](https://www.reddit.com/dev/api) 
and [PRAW error codes](https://praw.readthedocs.io/en/v3.6.0/pages/exceptions.html).

## Crontab
- The crontab runs the given tasks in the background at specific times. We can use the crontab to scrape the user 
profiles daily.
- Follow the below commands to setup the crontab on your system:
  - open terminal
  - Use command `crontab -e` to open or edit the crontab file.
  - If asked to select an editor choose according to your preference. 
  - Use arrow keys to reach to the bottom of the file.
  - Lines in the crontab has the following format:
       ```
       minute(0-59) hour(0-23) day(1-31) month(1-12) weekday(0-6) command
       ```
  - Use * to match any value.
  -   Write the following command in the file to run the 
  **reddit_scraper** daily at 9:59 am:
       ```
       59 9 * * * cd <path to reddit_analysis folder> && /usr/bin/python <path to driver.py> reddit_scarper -i <input file> -o <output file folder path> -format <json|csv> -cleaned <True|False> -
       ```
  - The location or the name of the python interpreter may vary.

### License
Apache