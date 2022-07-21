from django.contrib import admin
from blog.models import Post


# == admin.site.register()
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # TaggableManger클래스는 list_display항목에 직접 등록할 수 없으므로 별도로 tag_list항목을 메소드로 정의
    list_display = ('id', 'title', 'modify_dt', 'tag_list')
    # ,이 없으면 에러가 남
    list_filter = ('modify_dt',)
    search_fields = ('title', 'content')
    # slug 필드는 title 필드를 사용해 미리 채워지도록 합니다.
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        # N:N의 관계에서 퀴리 횟수를 줄여 성능을 높이고자 할 때 prefetch_related() 메소드 사용
        return super().get_queryset(request).prefetch_related('tags')

    # '구분자'.join(리스트) : 문자열을 구분자를 기준으로 합침
    def tag_list(self, obj):
        return ', '.join(o.name for o in obj.tags.all())
