from django.contrib import admin
from blog.models import Post


# == admin.site.register()
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'modify_dt')
    # ,이 없으면 에러가 남
    list_filter = ('modify_dt',)
    search_fields = ('title', 'content')
    # slug 필드는 title 필드를 사용해 미리 채워지도록 합니다.
    prepopulated_fields = {'slug': ('title',)}
