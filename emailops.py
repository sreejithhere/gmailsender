import logging
from multiprocessing import SimpleQueue, Process, Pool
from smtplib import SMTPResponseException,SMTPServerDisconnected,SMTPAuthenticationError
from email.utils import formatdate,make_msgid,getaddresses,parseaddr
import functools
from typing import Callable, Tuple, List
from mailobjects import Recipient, Payload


from gmail import GMail, GMailWorker,GMailHandler,Message

logger = logging.getLogger('GmailSender')



class GmailSender:
    def __init__(self, 
                    username: str,
                    password: str,
                    format: str='html',
                    error_handler: Callable[[Recipient], None]=None,
                    success_handler: Callable[[Recipient], None]=None,
                    background: bool=True,
                    parallel_threads: int=1):
        self.username = username
        self.password = password
        self.gmail = GMail(self.username, self.password)
        self.error_handler = error_handler
        self.success_handler = success_handler
        self.background = background
        self.format = format
        self.is_connected = False

    def prepare(self) -> None:
        if not self.is_connected:
            self.gmail.connect()
        self.is_connected = True

    def _worker_thread(self, payload) -> None:
        self.prepare()
        try:
            self.gmail.send(payload.msg, None)
        except SMTPServerDisconnected:
            if self.error_handler:
                self.error_handler(payload.recipeient)
        except SMTPResponseException:
            if self.error_handler:
                self.error_handler(payload.recipient)
        except KeyboardInterrupt:
            return
        if self.success_handler:
            self.success_handler(payload.recipient)

    def _send_bulk_synchronous(self, payload_list) -> None:
        self.prepare()
        for payload in payload_list:
            self._worker_thread(payload)

    def _send_bulk_async(self, payload_list: Payload) -> None:
        pool = Pool()
        pool.map(self._worker_thread, payload_list)
        pool.close()

    def send_bulk(self, payload_list) -> None:
        if self.background:
            return self._send_bulk_async(payload_list)
        else:
            return self._send_bulk_synchronous(payload_list)

    def send(self, message: str, recipient: Recipient, subject: str, rcpt: str=None) -> None:
        if self.format == 'html':
            msg = Message(subject=subject,
                        to=recipient.email,
                        html=message)
        else:
            msg = Message(subject=subject,
                            to=recipient.email,
                            text=message)

        self.queue.put((msg, recipient, rcpt))

    def close(self) -> None:
        self.gmail.close()
        self.is_connected = False

    def __del__(self):
        self.close()

    def __default_handler(self, recipient: Recipient, *args, **kwargs) -> None:
        logger.error("Error while sending maile to {}".format(recipient.email))
