from django.contrib import admin
from photo.models import Album, Photo


# 앨범 객체에 연결된 사진 객체를 보여주는 형식을 지정
class PhotoInline(admin.StackedInline):
    model = Photo
    # 이미 존재하는 객체 외에 추가로 입력할 수 있는 Photo 테이블 객체의 수는 2ㅐㄱ입니다.
    extra = 2


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    # 앨범 객체 수정 화면을 보여줄 때 PhotoInline 클래스에서 정의한 사항을 같이 보여줍니다.
    inlines = (PhotoInline,)
    list_display = ('id', 'name', 'description')


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'upload_dt')
