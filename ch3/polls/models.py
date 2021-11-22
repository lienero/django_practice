from django.db import models

# Create your models here.


class Question(models.Model):  # 테이블 정의
    # 장고의 필드 클래스 models.CharField(max_length=200) == varchar(200)
    question_text = models.CharField(max_length=200)
    # 장고의 필드 클래스 models.DateTimeField('date published') == datetime
    pud_date = models.DateTimeField('date published')

    # __str__() 메소드는 객체를 문자열로 표현할 때 사용하는 함수입니다.
    # __str__() 메소드를 정의하지 않으면 테이블명이 제대로 표시되지 않음
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    # PK는 클래스에 지정해주지 않아도, 장고는 항상 PK에 대한 속성을 Not Null 및 Autoincrement로, 이름은 id로 해서 자동으로 만들어줍니다.
    # FK는 항상 다른 테이블의 PK에 연결되므로, Question 클래스의 id 변수까지 지정할 필요없이 클래스만 지정하면 됩니다.
    # FK는 지정된 컬럼은 _id 접미사가 붙는다. (question_id)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    # 장고의 필드 클래스 models.IntegerField(default=0) == integer(default=0)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
