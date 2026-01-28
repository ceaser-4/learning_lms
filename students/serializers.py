from rest_framework import serializers

from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        # '__all__' 表示所有字段都翻译。
        # 如果只想返回姓名和学号，可以写 fields = ['name', 'student_id']
        # 测试点：如果你在这里少写了一个字段，你的测试用例去断言那个字段时就会报错 keyError
        fields = '__all__'