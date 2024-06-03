from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.fields import ReadOnlyField


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name')

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return {'user': user}
        raise serializers.ValidationError('Incorrect Credentials')


class TeacherSerializer(serializers.ModelSerializer):
    #image unrequired
    image = serializers.ImageField(required=False)
    subject = serializers.CharField(required=False)
    subject_id = serializers.IntegerField(write_only=True, required=False)
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ('id', 'user', 'middle_name', 'image', 'subject', 'subject_id')
        read_only_fields = ('user',)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['user']['username'],
            password=validated_data['user']['password'],
            first_name=validated_data['user']['first_name'],
            last_name=validated_data['user']['last_name'],
        )
        user.set_password(validated_data['user']['password'])
        if 'image' in validated_data:
            teacher = Teacher.objects.create(
                user=user,
                middle_name=validated_data['middle_name'],
                image=validated_data['image'],
            )
        else:
            teacher = Teacher.objects.create(
                user=user,
                middle_name=validated_data['middle_name'],
            )
        if 'subject_id' in validated_data:
            try:
                subject = Subject.objects.get(id=validated_data['subject_id'])
            except Subject.DoesNotExist:
                raise serializers.ValidationError('Subject does not exist')
            
            teacher.subject = subject
        teacher.save()
        return teacher
    
    def get_token(self, obj):
        try:
            token = Token.objects.get(user=obj.user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=obj.user)
        return token.key
    
    def update(self, instance, validated_data):
        if 'subject_id' in validated_data:
            try:
                subject = Subject.objects.get(id=validated_data['subject_id'])
            except Subject.DoesNotExist:
                raise serializers.ValidationError('Subject does not exist')
            
            instance.subject = subject

            
        instance.middle_name = validated_data.get('middle_name', instance.middle_name)
        instance.image = validated_data.get('image', instance.image)
        if 'user' in validated_data:
            instance.user.username = validated_data['user'].get('username', instance.user.username)
            instance.user.set_password(validated_data['user'].get('password', instance.user.password))
            instance.user.first_name = validated_data['user'].get('first_name', instance.user.first_name)
            instance.user.last_name = validated_data['user'].get('last_name', instance.user.last_name)
            instance.user.save()

        instance.save()
        return instance

class Class_nameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class_name
        fields = ('id', 'name')

class StudentSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    user = UserSerializer()
    group = Class_nameSerializer(read_only=True)
    group_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Student
        fields = ('id', 'user', 'middle_name', 'image', 'group', 'group_id')
        read_only_fields = ('user',)
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['user']['username'],
            password=validated_data['user']['password'],
            first_name=validated_data['user']['first_name'],
            last_name=validated_data['user']['last_name'],
        )
        user.set_password(validated_data['user']['password'])
        if 'image' in validated_data:
            student = Student.objects.create(
                user=user,
                middle_name=validated_data['middle_name'],
                image=validated_data['image'],
            )
        else:
            student = Student.objects.create(
                user=user,
                middle_name=validated_data['middle_name'],
            )
        if 'group_id' in validated_data:
            try:
                group = Class_name.objects.get(id=validated_data['group_id'])
            except Class_name.DoesNotExist:
                raise serializers.ValidationError('Class_name does not exist')
            
            student.group = group
        student.save()
        return student
    
    def get_token(self, obj):
        try:
            token = Token.objects.get(user=obj.user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=obj.user)
        return token.key
    
    def update(self, instance, validated_data):
        instance.middle_name = validated_data.get('middle_name', instance.middle_name)
        instance.image = validated_data.get('image', instance.image)
        if 'group_id' in validated_data:
            try:
                group = Class_name.objects.get(id=validated_data['group_id'])
            except Class_name.DoesNotExist:
                raise serializers.ValidationError('Class_name does not exist')
            
            instance.group = group

        if 'user' in validated_data:
            instance.user.username = validated_data['user'].get('username', instance.user.username)
            instance.user.set_password(validated_data['user'].get('password', instance.user.password))
            instance.user.first_name = validated_data['user'].get('first_name', instance.user.first_name)
            instance.user.last_name = validated_data['user'].get('last_name', instance.user.last_name)
            instance.user.save()

        instance.save()
        return instance
    
class ParentSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Parent
        fields = ('id', 'student', 'name', 'phone_number', 'student_id')
        read_only_fields = ('student',)

    def create(self, validated_data):
        try:
            student = Student.objects.get(id=validated_data['student_id'])
        except Student.DoesNotExist:
            raise serializers.ValidationError('Student does not exist')
        parent = Parent.objects.create(
            student=student,
            name=validated_data['name'],
            phone_number=validated_data['phone_number'],
        )
        return parent
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        if 'student_id' in validated_data:
            try:
                student = Student.objects.get(id=validated_data['student_id'])
            except Student.DoesNotExist:
                raise serializers.ValidationError('Student does not exist')
            instance.student = student

        instance.save()
        return instance


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'name')

class LessonSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    subject_id = serializers.IntegerField(write_only=True, required=False)

    group = Class_nameSerializer(read_only=True)
    group_id = serializers.IntegerField(write_only=True, required=False)
    class Meta:
        model = Lesson
        fields = ('id', 'name', 'subject', 'is_added', 'date', 'status', 'group', 'subject_id', 'group_id')
        read_only_fields = ('subject', 'group')

    def create(self, validated_data):
        try:
            subject = Subject.objects.get(id=validated_data['subject_id'])
        except Subject.DoesNotExist:
            raise serializers.ValidationError('Subject does not exist')
        try:
            group = Class_name.objects.get(id=validated_data['group_id'])
        except Class_name.DoesNotExist:
            raise serializers.ValidationError('Class_name does not exist')
        lesson = Lesson.objects.create(
            name=validated_data['name'],
            subject=subject,
            group=group,
            date=validated_data['date'],
        )
        return lesson
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.is_added = validated_data.get('is_added', instance.is_added)
        instance.date = validated_data.get('date', instance.date)
        instance.status = validated_data.get('status', instance.status)
        if 'subject_id' in validated_data:
            try:
                subject = Subject.objects.get(id=validated_data['subject_id'])
            except Subject.DoesNotExist:
                raise serializers.ValidationError('Subject does not exist')
            instance.subject = subject
        if 'group_id' in validated_data:
            try:
                group = Class_name.objects.get(id=validated_data['group_id'])
            except Class_name.DoesNotExist:
                raise serializers.ValidationError('Class_name does not exist')
            instance.group = group

        instance.save()
        return instance
    

    

class MarkSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True, required=False)
    subject_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Mark
        fields = ('id', 'student', 'subject', 'mark', 'date', 'student_id', 'subject_id')
        read_only_fields = ('student', 'subject')
    
    def create(self, validated_data):
        try:
            student = Student.objects.get(id=validated_data['student_id'])
        except Student.DoesNotExist:
            raise serializers.ValidationError('Student does not exist')
        try:
            subject = Subject.objects.get(id=validated_data['subject_id'])
        except Subject.DoesNotExist:
            raise serializers.ValidationError('Subject does not exist')
        mark = Mark.objects.create(
            student=student,
            subject=subject,
            mark=validated_data['mark'],
        )
        return mark

    def update(self, instance, validated_data):
        instance.mark = validated_data.get('mark', instance.mark)
        if 'student_id' in validated_data:
            try:
                student = Student.objects.get(id=validated_data['student_id'])
            except Student.DoesNotExist:
                raise serializers.ValidationError('Student does not exist')
            instance.student = student
        if 'subject_id' in validated_data:
            try:
                subject = Subject.objects.get(id=validated_data['subject_id'])
            except Subject.DoesNotExist:
                raise serializers.ValidationError('Subject does not exist')
            instance.subject = subject

        instance.save()
        return instance
    
class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    send_to = UserSerializer(many=True, read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    send_to_id = serializers.ListField(write_only=True, required=False)
    
    class Meta:
        model = Notification
        fields = ('id', 'title', 'text', 'user', 'send_to', 'date', 'user_id', 'send_to_id')
        read_only_fields = ('user', 'send_to')
    
    def create(self, validated_data):
        try:
            user = User.objects.get(id=validated_data['user_id'])
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exist')
        notification = Notification.objects.create(
            title=validated_data['title'],
            text=validated_data['text'],
            user=user,
        )
        if 'send_to_id' in validated_data:
            for user_id in validated_data['send_to_id']:
                try:
                    send_to = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    raise serializers.ValidationError('User does not exist')
                notification.send_to.add(send_to)
        return notification
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        if 'user_id' in validated_data:
            try:
                user = User.objects.get(id=validated_data['user_id'])
            except User.DoesNotExist:
                raise serializers.ValidationError('User does not exist')
            instance.user = user
        if 'send_to_id' in validated_data:
            for user_id in validated_data['send_to_id']:
                try:
                    send_to = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    raise serializers.ValidationError('User does not exist')
                instance.send_to.add(send_to)

        instance.save()
        return instance
    
class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True, required=False)
    lesson_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Attendance
        fields = ('id', 'student', 'lesson', 'status', 'date', 'student_id', 'lesson_id')
        read_only_fields = ('student', 'lesson')
    
    def create(self, validated_data):
        try:
            student = Student.objects.get(id=validated_data['student_id'])
        except Student.DoesNotExist:
            raise serializers.ValidationError('Student does not exist')
        try:
            lesson = Lesson.objects.get(id=validated_data['lesson_id'])
        except Lesson.DoesNotExist:
            raise serializers.ValidationError('Lesson does not exist')
        attendance = Attendance.objects.create(
            student=student,
            lesson=lesson,
            status=validated_data['status'],
        )
        return attendance

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        if 'student_id' in validated_data:
            try:
                student = Student.objects.get(id=validated_data['student_id'])
            except Student.DoesNotExist:
                raise serializers.ValidationError('Student does not exist')
            instance.student = student
        if 'lesson_id' in validated_data:
            try:
                lesson = Lesson.objects.get(id=validated_data['lesson_id'])
            except Lesson.DoesNotExist:
                raise serializers.ValidationError('Lesson does not exist')
            instance.lesson = lesson

        instance.save()
        return instance
    