from mongoengine.fields import StringField, EmbeddedDocument, DateTimeField, BooleanField, IntField, ListField


class Comment(EmbeddedDocument):

    id
    username = StringField()
    user_id = StringField()
    text = StringField()
    sentDateTime = DateTimeField()
    uptdTimestamp = DateTimeField()
    isEdited = BooleanField(default=False)
    likeReactions = ListField(username)
    laughReactions = IntField()
    angryReactions = IntField()
