from utils.api import APIView

from django.db.models import Q, Count

from ..models import Study, StudyTag, StudyStatusCategory
from account.decorators import login_required
from ..serializers import (CreateStudySerializer, StudentStudySerializer,
                            EditStudySerializers, StudyListSerializer,
                            TeacherStudySerializer, StudentStudySerializer,
                            StudyTagSerializer)
from utils.api import validate_serializer

class StudyTagAPI(APIView):
    def get(self, request):
        qs = StudyTag.objects
        keyword = request.GET.get("keyword")
        if keyword:
            qs = StudyTag.objects.filter(name__icontains=keyword)
        tags = qs.annotate(study_count=Count("study")).filter(study_count__gt=0)
        return self.success(StudyTagSerializer(tags, many=True).data)

class StudyAPI(APIView):
    @validate_serializer(CreateStudySerializer)
    @login_required
    def post(self, request):
        data = request.data

        tags = data.pop("tags")
        data["created_by"] = request.user
        study = Study.objects.create(**data)

        for tag in tags:
            try:
                tag = StudyTag.objects.get(name=tag)
            except StudyTag.DoesNotExist:
                tag = StudyTag.objects.create(name=tag)
            study.tags.add(tag)
        
        return self.success(TeacherStudySerializer(study).data)
        
    def get(self, request):
        id = request.GET.get("id")
        teacher = request.GET.get("teacher")
        if not id:
            return self.error("\"id\" param is required!")
        if not teacher:
            return self.error("\"teacher\" param is required!")

        try:
            study = Study.objects.get(id=id)
        except Study.DoesNotExist:
            return self.error("Study does not exist")

        if teacher:
            if request.user != study.created_by:
                return self.error("You are not the teacher of this study")
            else:
                return self.success(TeacherStudySerializer(study).data)

        return self.success(StudentStudySerializer(study).data)
    
    @validate_serializer(EditStudySerializers)
    @login_required
    def put(self, request):
        data = request.data
        try:
            study = Study.objects.get(id=data["id"])
        except Study.DoesNotExist:
            return self.error("Study does not exist")
        
        if request.user != study.created_by:
            return self.error("You are not the teacher of this study")

        tags = data.pop("tags")
        
        for k, v in data.items():
            setattr(study, k, v)
        study.save()

        study.tags.remove(*study.tags.all())
        for tag in tags:
            try:
                tag = StudyTag.objects.get(name=tag)
            except StudyTag.DoesNotExist:
                tag = StudyTag.objects.create(name=tag)
            study.tags.add(tag)
        
        return self.success(TeacherStudySerializer(study).data)
    
    @login_required
    def delete(self, request):
        if not request.GET.get("id"):
            return self.error("\"id\" param is required!")

        id = request.GET.get("id")
        try:
            study = Study.objects.get(id=id)
        except Study.DoesNotExist:
            return self.error("Study does not exist")

        if request.user != study.created_by:
            return self.error("You are not the teacher of this study")

        study.delete()
        return self.success("Study has successfully deleted")

class StudyListAPI(APIView):
    def get(self, request):
        if not request.GET.get("limit"):
            return self.error("\"limit\" field is required!")

        keyword = request.GET.get("keyword")
        tag = request.GET.get("tag")
        status = request.GET.get("status")

        studys = Study.objects.all()
        if keyword:
            studys = studys.filter(Q(title__contains=keyword) | Q(created_by__username__exact=keyword))
        if tag:
            studys = studys.filter(tags__name=tag)
        if status:
            if status not in StudyStatusCategory.choices():
                return self.error("Wrong study status given: ", status)
            else:
                studys = studys.filter(status__exact=status)
        return self.success(self.paginate_data(request, studys, StudyListSerializer))
        