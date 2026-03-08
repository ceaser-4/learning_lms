from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Student,Teacher
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import StudentSerializer,TeacherSerializer


# 定义一个视图集
# ViewSet = View (视图) + Set (集合)，因为它一口气搞定了 5 个接口 (GET列表, POST创建, GET详情, PUT修改, DELETE删除)
class StudentViewSet(viewsets.ModelViewSet):
    # 1. 指定查询集 (QuerySet)
    # 告诉程序：我要去哪里找数据？答：去 Student 表里把所有人都查出来。
    # 这里也是未来做“数据权限控制”的地方（比如只能查自己班的学生）
    queryset = Student.objects.all().order_by("id")

    # 2. 指定序列化器
    # 告诉程序：查出来的数据用哪个翻译官转成 JSON？
    serializer_class = StudentSerializer

    # 添加鉴权校验
    permission_classes = [IsAuthenticated]

    # 新增过滤器（做分页）
    # DjangoFilterBackend = 精确过滤 (例如 ?age=20)
    # filters.SearchFilter = 模糊搜索 (例如 ?search=张)
    # filters.OrderingFilter = 排序 (例如 ?ordering=-age)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # 指定允许精确过滤的字段
    filterset_fields = ['gender', 'age', 'student_id']

    # 指定允许模糊搜索的字段
    # 会在 name 和 student_id 里自动查找
    search_fields = ['name', 'student_id']

    # 指定允许排序的字段
    ordering_fields = ['age', 'student_id']


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer