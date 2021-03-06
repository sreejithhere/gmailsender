import sys
import argparse
import logging
from pdb import set_trace
import datetime

from errors import InvalidArgumentError
from fileops import CSVFileProcessor, TemplateFileProcessor, EventHandlers
from emailops import GmailSender
from mailobjects import Payload

logger = logging.getLogger('Main')


class Arguments:
    '''
    Holder for the command line arguments
    '''
    def __init__(self, username: str, 
                        password: str,
                        filename: str, 
                        template: str, 
                        subject: str,
                        error_file: str,
                        log_level: str='error',
                        format: str='html',
                        background: bool=False,
                        log_file: str=''):
        self.username = username
        self.password = password
        self.filename = filename
        self.template = template
        self.subject = subject
        self.error_file = error_file
        self._log_level = log_level
        self.format = format
        self.background=background
        self.log_file = log_file


    @property
    def log_level(self):
        '''
        Return the logging module compatible log level from the human friendly
        level
        '''
        if self._log_level == 'debug':
            return logging.DEBUG
        elif self._log_level == 'info':
            return logging.INFO
        else:
            return logging.ERROR

    def validate(self) -> None:
        def __empty_check(val):
            if not val:
                raise InvalidArgumentError('username')

        __empty_check(self.username)
        __empty_check(self.password)
        __empty_check(self.filename)

    def __str__(self):
        return '\n'.join("'{}': '{}'".format(key, value) for key, value in self.__dict__.items())


def get_parser() -> None:
    '''
    Returns the parser object
    '''

    parser = argparse.ArgumentParser(description="Send multiple emails with GMail")

    parser.add_argument('-u', '--username', action='store', required=True,
                        help='Username to use to send the emails')

    parser.add_argument('-p', '--password', action='store', required=True,
                        help='Application password.  Get from https://support.google.com/accounts/answer/185833?hl=en')

    parser.add_argument('-f', '--filename', action='store', required=True,
                        help='CSV file with the the list of recipients')

    parser.add_argument('-t', '--template', action='store', required=False,
                        help='Email template to use', default='template.html')
    parser.add_argument('-s', '--subject', action='store', required=True,
                            help="Subject of the email")

    parser.add_argument('-e', '--error_file', action='store', required=False,
                        help='File to store recipients which failed', default='failed.csv')
    parser.add_argument('--format', action='store', required=False, default='html',
                            help='Format of the email.  Should be either "html" or "text"')
    parser.add_argument('-v', action='store_const', const='info', dest='level', default='error',
                           help='Verbose output')
    parser.add_argument('-vv', action='store_const', const='debug', dest='level', default='error',
                            help="Very verbose output.  Debug information will be printed")

    parser.add_argument('-b', '--background', action='store_const', const=True, dest='background', default=False,
                            help="Set this flag to send multiple messages parallely")
    parser.add_argument('-l', '--log', action='store', dest='log_file', default='debug.log',
                            help="Log file to which successful recipients will be added")

    return parser


if __name__ == '__main__':
    parser = get_parser()
    parse_results = parser.parse_args()
    arguments = Arguments(parse_results.username, parse_results.password,
    parse_results.filename, parse_results.template, parse_results.subject,
                parse_results.error_file, parse_results.level, parse_results.format, parse_results.background,
                parse_results.log_file)
    arguments.validate()
    logging.basicConfig(level=arguments.log_level)
    logger.debug(str(arguments))

    # Parse the csv file and get the recipients
    csv_handler = CSVFileProcessor()
    recipients = csv_handler.parse(arguments.filename)
    total = len(recipients)
    logger.info("Sending emails to {} recipients".format(len(recipients)))
    template_handler = TemplateFileProcessor(arguments.template)

    # Update the logs
    with open('./error.log', 'a') as ef:
        ef.write("--------------------- {} ---------------------\n".format(datetime.datetime.now().strftime("%D %H%T")))

    with open('./success.log', 'a') as ef:
        ef.write("--------------------- {} ---------------------\n".format(datetime.datetime.now().strftime("%D %H%T")))
    handler = EventHandlers(failed_log_file='./error.log', success_log_file='./success.log')
    gs = GmailSender(arguments.username, arguments.password, background=arguments.background,
    error_handler=handler.handle_error, success_handler=handler.handle_success)
    payload_list = [Payload(r, arguments.subject, template_handler.generate_message(r)) \
                       for r in recipients]
    gs.send_bulk(payload_list)
    
