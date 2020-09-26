# GMail Sender
This is a utility to send multiple emails through GMail

## Installation Steps
1. Make sure that you have [python](https://www.python.org/) and [pip](https://pypi.org/project/pip/) installed in your machine.   Enure that python is in your system path so that you are able to invoke python from command line
2. Download or clone this repo.  To download, click on the **Code** button at the top and choose **Download ZIP**.  Save it to a folder and unzip
3. Open a terminal and move to the foler where you extracted the zip files.  You should see a file named **send.py**
4. You need to install the required packages.  You can do this by running  `pip install -r requirements.txt` from this folder
5. You can run the application using   `python send.py <arguments>`

## Features
This application is a no frills utility to send mass emails through your personal GMail account.  The following features are supported
- Sending multiple emails from a list provided in a CSV file
- Supports both text and HTML content
- Use a template HTML file for the body of the email.  The HTML file can link to external images
- Provide a Subject for the emails
- Customise the email body for each recipient as provided in the CSV
- Speed up the sending of the emails by sending them in parallel using multiprocessing

**Note the following limitations**
- GMail may rate limit your account if you send too many mails in a rapid burst
- GMail does not provide any error message when the email failed to deliver.  So this utility will return success whether the mail got delivered or not

## Instructions for usage
### Preparing GMail Credentials
Before you can start using this application you need to generate an application specific password for your GMail account.
You can get this by visiting [this](https://support.google.com/mail/answer/185833?hl=en-GB) help article and following the instructions there
Remember the application password which you generate since it can be viewed only once

### Preparing Fiels
You need two files to run the utility
- A CSV which contains the list of recipients
- An HTML or text file containing the body of the email

To prepare the CSV, you can use the *template.csv* file in the root folder.  Copy the file into a new file and add the recipient information.  Make sure that the first row is not altered in any way

To prepare the HTML or text file, first create your template file.  The utility allows you to customise the mail for each recipient by dynamically changing the following
- Title (Mr., Ms., Dr. etc.)
- First name
- Middle name
- Last name
- Full name (If this is provided, the other parts of name will be ignored)
- Suffix (MD, IPS etc.)
To use the customisation, edit your html file to mark the locations which should be dynamically filled
using the information from the CSV.  You can do this by adding the placeholder string according to the 
table below.  Make sure that the curly braces - "{" and "}" are not omitted and there is a space
before and after the curly braces

| Field | Place holder|
|-------- |------------|
| First name | {first_name} |
|  


