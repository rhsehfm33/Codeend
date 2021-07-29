from .models import Board, BoardCategory
from comment.models import Comment
from comment.serializers import CommentSerializer
from utils.api import UsernameSerializer, serializers
from utils.serializers import LanguageNameChoiceField


class CreateBoardSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    category = serializers.ChoiceField(choices=(BoardCategory.Free, BoardCategory.Question))
    content = serializers.CharField(max_length=1024 * 1024)

class EditBoardSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    category = serializers.ChoiceField(choices=(BoardCategory.Free, BoardCategory.Question))
    content = serializers.CharField(max_length=1024 * 1024)

class BoardSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()
    comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = "__all__"

class BoardListSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()
    
    class Meta:
        model = Board
        exclude = ("content",)