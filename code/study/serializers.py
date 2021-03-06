from django.db.models import fields
from .models import Study, StudyTag, StudyStatusCategory
from utils.api import UsernameSerializer, serializers

class StudyTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyTag
        fields = "__all__"

class TeacherStudySerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()
    tags = serializers.SlugRelatedField(many=True, slug_field="name", read_only=True)

    class Meta:
        model = Study
        fields = "__all__"

class StudentStudySerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()
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

class EditStudySerializers(serializers.ModelSerializer):
    id = serializers.IntegerField()
    subject = serializers.CharField(max_length=64)
    status = serializers.ChoiceField(choices=(StudyStatusCategory.Recruiting, StudyStatusCategory.Recruited))
    tags = serializers.ListField(child=serializers.CharField(max_length=32), allow_empty=False)

    class Meta:
        model = Study
        exclude = ("students", "created_by")

class GetStudyListSerializer(serializers.Serializer):
    limit = serializers.IntegerField()

class StudyListSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()
    total_students = serializers.SerializerMethodField()
    tags = serializers.SlugRelatedField(many=True, slug_field="name", read_only=True)
    
    class Meta:
        model = Study
        fields = ("id", "title", "price", "tags", "status", "subject", "max_students", "created_by", "total_students")

    def get_total_students(self, obj):
        return obj.students.count()