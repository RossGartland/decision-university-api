from mongoengine.document import Document
from mongoengine.fields import ListField, StringField, ObjectIdField, \
    EmbeddedDocumentField, DateTimeField, EmailField, BooleanField, BinaryField
from models.comments import Comment


class User(Document):

    id
    isAdmin = BooleanField(default=False)
    username = StringField()
    email = EmailField()
    forename = StringField()
    surname = StringField()
    password = BinaryField()
    crtdTimestamp = DateTimeField()
    uptdTimestamp = DateTimeField()
