from django.contrib import admin
from django.db.models.query_utils import Q
# models 파일에서 정의한 테이블로 Admin 사이트에 보이도록 등록한다.
from polls.models import Question, Choice

# Register your models here.
# admin.site.register() 함수를 사용하여 임포트한 클래스를 Admin 사이트에 등록해주면 됩니다.
admin.site.register(Question)
admin.site.register(Choice)
