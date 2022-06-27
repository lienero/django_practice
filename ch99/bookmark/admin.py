from django.contrib import admin
from bookmark.models import Bookmark


# 테이블을 새로 만들 때에는 models.py와 admin.py 두개의 파일을 함꼐 수정해야한다.
@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'url')
# Register your models here.
