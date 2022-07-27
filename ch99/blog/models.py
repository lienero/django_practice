from django.db import models
# reverse() 함수는 url패턴을 만들어주는 장고의 내장 함수다
from django.urls import reverse
# 태그 패키지
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
# slug 필드를 자동으로 채우기 위해 slugify() 함수를 임포트합니다.
# slugify() 함수는 원래 단어를 알파벳 소문자, 숫자, 밑줄, 하이픈으로만 구성된 단어로 만들어주는 함수다.
from django.utils.text import slugify


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
    tags = TaggableManager(blank=True)
    # verbose_name : 모델의 필드명을 지정
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='OWNER', blank=True, null=True)

    # 필드 속성 외에 필요한 파라미터가 있으면 Meta 내부 클래스로 정의합니다.

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

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        # 부모 클래스의 save() 메소드를 호출해 객체의 내용을 테이블에 반영하는 save() 메소드의 원래 기능을 수행합니다.
        super().save(*args, **kwargs)
