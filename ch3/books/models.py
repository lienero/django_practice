from django.db import models

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=100)
    # ManyToManyField : 다대다 관계를 의미하며 Foregin key와 동일하게 작동한다.
    authors = models.ManyToManyField('Author')
    # ForeignKey : 테이블의 관계를 N:1로 정의하고 있다.
    # ForeignKey를 정의할 때는 on_delete를 필수로 지정해야 한다.
    # CASCADE : ForeignKeyField를 포함하는 모델 인스턴스(row)도 같이 삭제한다.
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE)
    publication_date = models.DateField()

    # __str__() 메소드는 객체를 문자열로 표현할 때 사용하는 함수입니다.
    # __str__() 메소드를 정의하지 않으면 테이블명이 제대로 표시되지 않음
    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=50)
    salutation = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    website = models.URLField()

    def __str__(self):
        return self.name
