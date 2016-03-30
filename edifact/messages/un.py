import edifact.configuration
from edifact.messages.base import Message


class MSCONS(Message):
    class Meta:
        spec = 'MSCONS'

edifact.configuration.MESSAGE_CLASSES['MSCONS'] = MSCONS
