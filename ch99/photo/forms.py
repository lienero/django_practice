# inlineformset_factory() : 임라인 폼셋을 반환하는 함수
from django.forms import inlineformset_factory
from photo.models import Album, Photo

# 1:N 관계인 Album과 Photo 테이블을 이용해 사진 인라인 폼셋을 만듭니다.
PhotoInlineFormSet = inlineformset_factory(
    # Photo 모델에서 폼셋에 사용하는 필드를 지정
    Album, Photo, fields=['image', 'title', 'description'], extra=2)
