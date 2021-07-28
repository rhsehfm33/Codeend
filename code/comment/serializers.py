from .models import Comment
from utils.api import UsernameSerializer, serializers
from utils.serializers import LanguageNameChoiceField

class CommentSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'content', 'create_time', 'created_by')

class CreateCommentSerializer(serializers.Serializer):
    content = serializers.CharField()
    board_id = serializers.IntegerField()

class UpdateCommentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    content = serializers.CharField()