import sys
import argparse
import logging
from pdb import set_trace

from errors import InvalidArgumentError
from fileops import CSVFileProcessor, TemplateFileProcessor, EventHandlers
from emailops import GmailSender
from mailobjects import Payload

logger = logging.getLogger('Main')

class Arguments:
    '''
    Holder for the command line arguments
    '''
    def __init__(self, filename: str='', 
                        template: str='', 
                        log_level: str='error'):
        self.filename = filename
        self.template = template
        self._log_level = log_level


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

    def __str__(self):
        return '\n'.join("'{}': '{}'".format(key, value) for key, value in self.__dict__.items())


def get_parser() -> None:
    '''
    Returns the parser object
    '''

    parser = argparse.ArgumentParser(description="Send multiple emails with GMail")

    parser.add_argument('-f', '--filename', action='store', required=False,
                        help='CSV file with the the list of recipients')

    parser.add_argument('-t', '--template', action='store', required=False,
                        help='Email template to use', default='')

    parser.add_argument('-v', action='store_const', const='info', dest='level', default='error',
                           help='Verbose output')
    parser.add_argument('-vv', action='store_const', const='debug', dest='level', default='error',
                            help="Very verbose output.  Debug information will be printed")

    return parser


if __name__ == '__main__':
    parser = get_parser()
    parse_results = parser.parse_args()
    arguments = Arguments(parse_results.filename, parse_results.template, 
            parse_results.level)
    logging.basicConfig(level=arguments.log_level)
    logger.debug(str(arguments))

    if arguments.filename:
        csv_handler = CSVFileProcessor()
        valid, total = csv_handler.validate(arguments.filename)
        if valid == total:
            logger.info('CSV File is valid')
        else:
            logger.error("CSV file is not valid - {} / {} rows have errors".format(total-valid, total))
    if arguments.template:
        logger.info("HTML template validation is not supported")

    if not arguments.filename and not arguments.template:
        logger.info("Nothing to validate")
