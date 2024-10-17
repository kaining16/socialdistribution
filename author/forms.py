from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Author

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Author

class CustomAuthorCreationForm(UserCreationForm):
    class Meta:
        model = Author  # 使用自定义的 Author 模型
        fields = ("username", "password1", "password2")  # 只保留用户名和密码字段

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # 从 kwargs 中获取 request 对象
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        # 只保存用户名和密码
        author = super().save(commit=False)
        author.host = f"http://{self.request.get_host()}/api/"  # 设置 host 为当前主机
        if commit:
            author.save()
        return author