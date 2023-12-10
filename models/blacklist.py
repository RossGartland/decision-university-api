from mongoengine.document import Document
from mongoengine.fields import BinaryField


class Blacklist(Document):

    id
    token = BinaryField(default=False)
