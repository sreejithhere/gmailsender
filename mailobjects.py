from nameparser import HumanName
from gmail import Message


class Recipient:
    '''
    Reprsents a single recipient of the email
    '''
    def __init__(self, 
                    index: int,
                    first_name: str='',
                    last_name: str='',
                    middle_name: str='',
                    full_name: str='',
                    name_prefix: str='',
                    name_suffix: str='',
                    email=''):
        self.index = index
        self._first_name = first_name
        self._last_name = last_name
        self._middle_name = middle_name
        self._full_name = full_name
        self._name_prefix = name_prefix
        self._name_suffix=name_suffix
        self._email = email

        if self._full_name:
            self._human_name = HumanName(self._full_name)
        else:
            self._human_name = HumanName()
            self._human_name.first = first_name
            self._human_name.last = last_name
            self._human_name.title = name_prefix
            self._human_name.suffix = name_suffix
            self._human_name.middle = middle_name

    @property
    def first_name(self):
        return self._human_name.first

    @property 
    def last_name(self):
        return self._human_name.last

    @property
    def middle_name(self):
        return self._human_name.middle

    @property
    def full_name(self):
        return self._human_name.full_name
    
    @property
    def name_prefix(self):
        return self._human_name.title

    @property
    def name_suffix(self):
        return self._human_name.suffix

    @property
    def email(self):
        return self._email

    def __str__(self):
        return "Recipient: {} - {}".format(self.index, self.full_name)

    def to_dict(self) -> dict:
        return {
            'name_prefix': self.name_prefix,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'name_suffix': self.name_suffix,
            'email': self._email
        }

class Payload:
    def __init__(self, recipient: Recipient, subject: str, message: str, format: str='html'):
        self.recipient = recipient
        self.subject = subject
        self.message = message
        if format =='html': 
            self.msg = Message(subject=self.subject,
                to=self.recipient.email,
                html=message
                )
        else:
            self.msg = Message(subject=self.subject, to=self.recipient.email, text=message)
