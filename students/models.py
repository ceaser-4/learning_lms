from django.db import models

class Student(models.Model):
    # 选项配置：性别选择
    GENDER_CHOICES = (
        (1, '男'),
        (2, '女'),
    )

    # 定义字段
    name = models.CharField(max_length=50, verbose_name="姓名")
    student_id = models.CharField(max_length=20, unique=True, verbose_name="学号")
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=1, verbose_name="性别")
    age = models.IntegerField(default=18, verbose_name="年龄")

    # 这是为了让后台显示更好看，打印对象时直接显示名字
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "学生信息"
        verbose_name_plural = verbose_name