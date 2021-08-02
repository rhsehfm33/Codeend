from django.db.models import fields
from .models import Study, StudyTag, StudyStatusCategory
from utils.api import UsernameSerializer, serializers

class StudyTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyTag
        fields = "__all__"

class TeacherStudySerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(many=True, slug_field="name", read_only=True)
    class Meta:
        model = Study
        fields = "__all__"

class StudentStudySerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(many=True, slug_field="name", read_only=True)
    class Meta:
        model = Study
        exclude = ("students",)

class CreateStudySerializer(serializers.ModelSerializer):
    subject = serializers.CharField(max_length=64)
    status = serializers.ChoiceField(choices=(StudyStatusCategory.Recruiting, StudyStatusCategory.Recruited))
    tags = serializers.ListField(child=serializers.CharField(max_length=32), allow_empty=False)

    class Meta:
        model = Study
        exclude = ("students", "created_by")

class GetStudySerializers(serializers.Serializer):
    id = serializers.IntegerField()
    teacher = serializers.BooleanField()
        
class EditStudySerializers(serializers.ModelSerializer):
    subject = serializers.CharField(max_length=64)
    status = serializers.ChoiceField(choices=(StudyStatusCategory.Recruiting, StudyStatusCategory.Recruited))
    tags = serializers.ListField(child=serializers.CharField(max_length=32), allow_empty=False)

    class Meta:
        model = Study
        exclude = ("students", "created_by")

class DeleteStudySerializers(serializers.Serializer):
    id = serializers.IntegerField()

class GetStudyListSerializer(serializers.ModelSerializer):
    limit = serializers.IntegerField()

class StudyListSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()
    total_students = serializers.SerializerMethodField()
    tags = serializers.ListField(child=serializers.CharField(max_length=32), allow_empty=False)
    
    class Meta:
        model = Study
        fields = ("id", "title", "price", "tags", "status", "subject", "max_students")

    def get_total_students(self, obj):
        return obj.students.count()