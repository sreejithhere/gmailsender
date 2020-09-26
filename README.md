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
Before you can start using this application you need to generate an application specific password for your GMail account.
You can get this by visiting [this](https://support.google.com/mail/answer/185833?hl=en-GB) help article and following the instructions there
