from django import forms


class PostSearchForm(forms.Form):
    # 변수 search_word는 name 속성이 되어 사용자가 입력한 값을 저장하는 데 사용됩니다.
    # <input type-"text">를 하나 만든 것이다.
    search_word = forms.CharField(label='Search Word')
