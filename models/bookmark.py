from mongoengine.fields import StringField, EmbeddedDocument, DateTimeField


class Bookmark(EmbeddedDocument):

    id
    institution = StringField()
    institutionID = StringField()
    crtdDateTime = DateTimeField()
