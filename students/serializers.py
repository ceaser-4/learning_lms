from rest_framework import serializers

from .models import Student, Teacher

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        # '__all__' 表示所有字段都翻译。
        # 如果只想返回姓名和学号，可以写 fields = ['name', 'student_id']
        # 测试点：如果你在这里少写了一个字段，你的测试用例去断言那个字段时就会报错 keyError
        fields = '__all__'

    def validate_student_id(self, value):
        """
        单字段验证：校验学号格式
        value 就是前端传来的 student_id
        """
        if not value.startswith("STU"):
            raise serializers.ValidationError("学号必须以 'STU' 开头")

        # 验证通过，必须把值返回去
        return value


# ... (你原来的 StudentSerializer 保持不变)

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'