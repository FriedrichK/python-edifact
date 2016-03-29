import edifact.configuration
from edifact.messages.base import Message


class MSCONS(Message):
    pass

edifact.configuration.MESSAGE_CLASSES['MSCONS'] = MSCONS
