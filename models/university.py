from mongoengine.document import Document
from mongoengine.fields import ListField, StringField, EmbeddedDocumentField, DateTimeField, IntField, DecimalField
from models.comments import Comment


class University(Document):

    id
    # University rank for 2022.
    r2022 = IntField()
    # University rank for 2021.
    r2021 = IntField()
    # Overall score for university.
    score = DecimalField()
    # Percentage of students satisfied with their course.
    course = DecimalField()
    # Percentage of students happy with their teachers.
    teaching = DecimalField()
    # Percentage of students satisfied with the feedback they have recieved.
    feedback = DecimalField()
    # Number of students to teachers.
    ratio = DecimalField()
    # Expenditure per student as a score out of 10.
    spend = DecimalField()
    # Average UCAS tariff needed for students to enter the institution.
    tariff = IntField()
    # Percentage of students who get a job within 15 months of graduation.
    career = IntField()
    # Percentage of first year students passing and proceeding to 2nd year.
    continuation = IntField()
    # Name of university.
    institution = StringField()
    # Comments provided by users.
    comments = ListField(EmbeddedDocumentField(Comment))
    # Time document was created.
    crtdTimestamp = DateTimeField()
    # Time document was last updated.
    uptdTimestamp = DateTimeField()
