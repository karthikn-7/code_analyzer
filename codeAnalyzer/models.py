import mongoengine as me
import datetime

class CodingQuestion(me.Document):
    question = me.StringField(required=True)
    inputs = me.ListField(me.StringField(),required=True)
    expect_outputs = me.ListField(me.StringField(),required=True)
    user_id = me.IntField(required=True)
    meta = {
        'collection':'coding_questions',
        'ordering':["-id"]
    }
    


class CodingResult(me.Document):
    user_id = me.IntField(required=True)
    question_id = me.ReferenceField(CodingQuestion,reverse_delete_rule=2,required=True)
    outputs = me.ListField(me.StringField(),required=True)
    submitted_code = me.StringField(required=True)
    passed_test_cases = me.IntField(default=0)
    total_test_cases = me.IntField(default = 0)
    status = me.StringField(choices=('passed','failed','partial'),required=True)
    submitted_at = me.DateTimeField(default=datetime.datetime.utcnow)
    
    meta = {"collection":"codingResult"}