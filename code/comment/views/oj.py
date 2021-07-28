from utils.api import APIView

from comment.models import Comment
from board.models import Board
from ..serializers import CommentSerializer, CreateCommentSerializer, UpdateCommentSerializer
from account.decorators import login_required
from utils.api import validate_serializer

class CommentAPI(APIView):
    @validate_serializer(CreateCommentSerializer)
    @login_required
    def post(self, request):
        data = request.data
        data["board"] = Board.objects.get(id=data["board_id"])
        data["created_by"] = request.user
        
        comment = Comment.objects.create(**data)
        return self.success(CommentSerializer(comment).data)
    
    @validate_serializer(UpdateCommentSerializer)
    @login_required
    def put(self, request):
        data = request.data
        comment = Comment.objects.get(id=data["id"])
        comment.content = request.data["content"]
        comment.save(update_fields=["content"])
        return self.success(CommentSerializer(comment).data)

    @login_required
    def delete(self, request):
        id = request.GET.get("id")
        if not id:
            return self.error("Invalid parameter, id is required")
        try:
            comment = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            return self.error("Comment does not exists")

        if comment.created_by == request.user:
            comment.delete()
            return self.success("Comment has successfully deleted")
        else:
            return self.error("You are not the writer of this comment")
