from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator

class Author(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='必填。150个字符或更少。仅允许字母、数字和@/./+/-/_符号。',
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': "已经存在该用户名。",
        },
    )
    # 完整的 API URL 作为 Author 的唯一标识符
    fqid = models.URLField(unique=True, blank=True, null=True)

    # 作者类型字段
    type = models.CharField(max_length=10, default="author")

    # 作者显示的名称 (使用 AbstractUser 的 username 代替 displayName)
    displayName = models.CharField(max_length=100)

    # 作者所在节点的 API URL
    host = models.URLField()

    # 作者的 GitHub URL
    github = models.URLField(blank=True, null=True)

    # 作者的个人图片 URL
    profileImage = models.URLField(blank=True, null=True)

    # 用户 HTML 个人主页的 URL
    page = models.URLField(blank=True, null=True)

    # 关注者列表 (其他作者关注了该作者)
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False, blank=True)

    # 朋友列表 (互相关注的作者)
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)

    def save(self, *args, **kwargs):
        # 第一次保存对象时，pk 尚未生成，因此先保存对象
        if not self.pk:
            super().save(*args, **kwargs)

        # 生成 fqid URL，确保使用 self.pk 创建唯一的 URL
        if not self.fqid:
            self.fqid = f"{self.host}authors/{self.pk}"

            # 保存 fqid 更新后的对象
            super().save(update_fields=['fqid'])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username  # 使用 AbstractUser 的 username 作为字符串表示

    def add_follower(self, author):
        """ 添加一个新的关注者 """
        if author != self:
            self.followers.add(author)

    def remove_follower(self, author):
        """ 移除一个关注者 """
        self.followers.remove(author)

    def is_friend(self, author):
        """ 检查某个作者是否是朋友 """
        return author in self.friends

    def add_friend(self, author):
        """ 当双方互相关注时，将对方设为朋友 """
        if author != self and author in self.followers and self in author.followers:
            self.friends.add(author)
            author.friends.add(self)

    def remove_friend(self, author):
        """ 移除朋友关系（互相取消关注）"""
        self.friends.remove(author)
        author.friends.remove(self)