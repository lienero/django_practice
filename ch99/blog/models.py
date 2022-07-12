from pyexpat import model
from tabnanny import verbose
from django.db import models
# reverse() 함수는 url패턴을 만들어주는 장고의 내장 함수다
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(verbose_name='TITLE', max_length=50)
    # allow_unicode 옵션으로 한글 처리가 가능해짐
    slug = models.SlugField('SLUG', unique=True,
                            allow_unicode=True, help_text='one word for title alias.')
    description = models.CharField(
        'DESCRIPTION', max_length=100, blank=True, help_text='simple description text.')
    content = models.TextField('CONTENT')
    # auto_mow_add 속성은 객체가 생성될 떄의 시각을 자동으로 기록하게 한다.
    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_dt = models.DateTimeField('MODIFY DATE', auto_now=True)


class Meta:
    verbose_name = 'post'
    verbose_name_plural = 'posts'
    # 테이블의 이름 지정
    db_table = 'blog_posts'
    # modify_dt를 내림차순으로 정렬
    ordering = ('-modify_dt',)

    def __str__(self):
        return self.title

    # 정의된 객체를 지칭하는 url을 반환
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=(self.slug,))

    def get_previous(self):
        # modify_dt 컬럼을 기준으로 최신 포스트를 반환
        return self.get_previous_by_modify_dt()

    def get_next(self):
        # modify_dt 컬럼을 기준으로 예전 포스트를 반환
        return self.get_next_by_modify_dt()
