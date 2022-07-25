import imp
import os
# 파이썬 이미지 처리 라이브러리 PIL.Image를 임포트
from PIL import Image
from django.db.models.fields.files import ImageField, ImageFieldFile


# ImageFieldFile 클래스는 파일 시스템에 직접 파일을 쓰고 지우는 작업을 합니다.
class ThumbnailImageFieldFile(ImageFieldFile):
    # 이 메소드는 기존 이미지 파일명을 기준으로 썸네일 이미지 파일명을 만들어 준다.
    # 참고서의 오류, 모든 인스턴스 메서드가 사용자 정의에 따라 self라고 부르는 첫 번째 인수를 기대하기에 s외에 self 인수가 필요
    def _add_thumbs(self, s):
        parts = s.split(".")
        parts.insert(-1, "thumb")
        # 이미지 확장자가 jpeg 가 아닐 경우
        if parts[-1].lower() not in ['jpeg', 'jpg']:
            parts[-1] = 'jpg'
        return ".".join(parts)

    # @property 데코레이터를 사용하면, 메소드를 멤버변수처럼 사용할 수 있다.
    @property
    # 이미지는 처리하는 필드는 파일의 경로(path)와 URL(url) 속성을 제공해얗 하므로,
    # 원본 파일의 경로인 path 속성을 추가해 thump_path 속성을 만든다.
    def thumb_path(self):
        return self._add_thumbs(self.path)

    # 원본 파일의 url인 url 속성을 추가해 thump_url 속성을 만든다.
    @property
    def thumb_url(self):
        return self._add_thumbs(self.url)

    def save(self, name, content, save=True):
        # 부모 ImageFieldFile 클래스의 save() 메소드를 호출해 원본 이미지를 저장한다.
        super().save(name, content, save)

        img = Image.open(self.path)
        size = (self.field.thumb_width, self.field.thumb_height)
        # PIL 라이브러리의Image.thumbnail()함수를 이용해 썸네일을 생성
        img.thumbnail(size)
        background = Image.new('RGB', size, (255, 255, 255))
        box = (int((size[0] - img.size[0]) / 2),
               int((size[1] - img.size[1]) / 2))
        # 썸네일과 백그라운드 이미지를 합쳐서 정사각형 모양의 썸네일 이미지를 생성
        # 이미지 붙이기(추가할 이미지 , 붙일 위치(가로, 세로))
        background.paste(img, box)
        # JPEG 형식으로 파일 시스템의 thumb_path 경로에 저장
        background.save(self.thumb_path, 'JPEG')

    # delet() 메소드 호출 시 원본 이미지 뿐만이 아니라 썸네일 이미지도 같이 삭제되도록 설정
    def delete(self, save=True):
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)
        super().delete(save)


class ThumbnailImageField(ImageField):
    # 새로운 FileField클래스를 정의할 때는 그에 상응하는 File 처리 클래스를 attr_class 속성에 지정하는 것이 필수입니다.
    attr_class = ThumbnailImageFieldFile

    def __init__(self, verbose_name=None, thumb_width=128, thumb_height=128, **kwargs):
        self.thumb_width, self.thumb_height = thumb_width, thumb_height
        super().__init__(verbose_name, **kwargs)
