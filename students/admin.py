from django.contrib import admin
# 从当前目录(.)的 models 文件里导入 Student 类
from .models import Student


# 装饰器写法 (这是 Python 高级语法，等同于 admin.site.register(Student))
# 作用：告诉 Django Admin，请在后台帮我管理 Student 这个表
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # list_display 控制在后台列表页显示哪些列
    # 如果不写这个，列表页只会显示 __str__ 返回的名字
    list_display = ('student_id', 'name', 'gender', 'age')

    # search_fields 控制搜索框能搜哪些字段
    # 方便你在后台快速找人
    search_fields = ('name', 'student_id')