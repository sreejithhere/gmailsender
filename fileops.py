import os
import csv
import logging
from typing import List

from mailobjects import Recipient
from errors import FileNotFoundException, FileWriteError, InvalidArgumentError

recipient_info = ['name_prefix', 'name_suffix', 'first_name', 'last_name', 'full_name', 'email']
Recipients = List[Recipient]

logger = logging.getLogger('fileops')

class CSVFileProcessor:
    def __init__(self):
        pass

    def parse(self, filename: str) -> Recipients:
        '''
        Parses the CSV file containing the details of the email recipients
        and returns the list of recipients
        '''
        if not os.path.isfile(filename):
            raise FileNotFoundException(filename)
        
        recipients = []
        with open(filename, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                recipient = Recipient(row.get('first_name', ''),
                row.get('last_name', ''),
                row.get('middle_name', ''),
                row.get('full_name', ''),
                row.get('name_prefix', ''),
                row.get('name_suffix', ''),
                row.get('email', ''))
                recipients.append(recipient)
        return recipients

    def get_template(self, filename: str=None) -> str:
        '''
        Get a CSV template tile which can be filled and passed to the parse() function.
        If a filename is passed as argument, the template will be written to the file
        '''
        template_string = ','.join(recipient_info)
        if filename:
            with open(filename, 'w') as f:
                f.write(template_string)
        return template_string

    def write(self, filename: str, append: bool=True, recipients: Recipients=[]) -> None:
        '''
        Writes the list of recipients into the standar CSV. 
        If append is provided, then the file will be appended if it already exists
        '''
        open_type = 'a' if append else 'w'
        # If the does not exist or is being overwritten, we have to write the header
        need_header = open_type == 'w' or not os.path.exists(filename)
        try:
            with open(filename, open_type) as f:
                writer = csv.DictWriter(f, fieldnames=recipient_info)
                if need_header:
                    writer.writeheader()
                writer.writerows(r.to_dict() for r in recipients)
        except PermissionError as ex:
            raise FileWriteError(filename, str(ex))


class TemplateFileProcessor:
    '''
    Process the template email file to return the message
    '''
    def __init__(self, template_file: str):
        self.template_file = template_file
        if not os.path.isfile(template_file):
            raise FileNotFoundException(template_file)

        with open(self.template_file, 'r') as f:
            self._template_message = f.read()

    def generate_message(self, recipient: Recipient) -> str:
        '''
        Replaces the place holders in the message with the recipient information
        '''
        msg = self._template_message.format(name_prefix=recipient.name_prefix,
        first_name=recipient.first_name,
        middle_name=recipient.middle_name,
        last_name=recipient.last_name,
        full_name=recipient.full_name,
        name_suffix=recipient.name_suffix)
        return msg


class EventHandlers:
    def __init__(self,
                 log_failure: bool=True,
                 log_success: bool=True,
                 log_failed_to_file: bool= True,
                 error_file: str='',
                 ):
        self.log_failure = log_failure
        self.log_success = log_success
        self.log_failed_to_file = log_failure and log_failed_to_file
        self.error_file = error_file
        if self.log_failure and not self.error_file:
            raise InvalidArgumentError('errro_file', '')
    
    def handle_error(self, recipient: Recipient) -> None:
        logger.error("Error while sending email to {}".format(recipient.email))
        if self.log_failed_to_file:
            writer = CSVFileProcessor()
            writer.write(self.error_file, True, [recipient])
        
    def handle_success(self, recipient: Recipient) -> None:
        logger.info("Successfully sent mail to {}".format(recipient.email))
