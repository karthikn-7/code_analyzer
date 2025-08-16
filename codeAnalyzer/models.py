import mongoengine as me
import datetime

class CodingQuestion(me.Document):
    question = me.StringField()
    user_id = me.IntField(required=True)
    meta = {
        'collection':'coding_questions',
        'ordering':["-id"]
    }
    


class CodingResult(me.Document):
    user_id = me.IntField(required=True)
    question_id = me.ReferenceField(CodingQuestion,reverse_delete_rule=2,required=True)
    submitted_code = me.StringField()
    report = me.StringField(required=True)
    submitted_at = me.DateTimeField(default=datetime.datetime.utcnow)
    
    meta = {"collection":"codingResult"}