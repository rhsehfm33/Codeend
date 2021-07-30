from utils.api import APIView

from board.models import Board, BoardCategory
from ..serializers import (CreateBoardSerializer, BoardSerializer, EditBoardSerializer,
                            BoardListSerializer)
from account.decorators import login_required
from utils.api import validate_serializer


class BoardBase(APIView):
    def common_checks(self, request):
        data = request.data
        if data["category"] not in BoardCategory.choices():
            return "Invalid category"
        if not data["content"]:
            return "Empty content"

class BoardAPI(BoardBase):
    @validate_serializer(CreateBoardSerializer)
    @login_required
    def post(self, request):
        error_info = self.common_checks(request)
        if error_info:
            return self.error(error_info)
        data = request.data
        data["created_by"] = request.user
        board = Board.objects.create(**data)
        return self.success(BoardSerializer(board).data)
        
    def get(self, request):
        board_id = request.GET.get("id")
        if (board_id):
            try:
                board = Board.objects.get(id=board_id)
            except Board.DoesNotExist:
                return self.error("Board does not exist")
            board.views += 1
            board.save(update_fields=["views"])
            return self.success(BoardSerializer(board).data)
    
    @validate_serializer(EditBoardSerializer)
    @login_required
    def put(self, request):
        data = request.data
        
        try:
            board = Board.objects.get(id=data["id"])
        except Board.DoesNotExist:
            return self.error("Board does not exist")

        for k, v in data.items():
            setattr(board, k, v)
        board.save()
        return self.success(BoardSerializer(board).data)
    
    @login_required
    def delete(self, request):
        user = request.user
        id = request.GET.get("id")
        if not id:
            return self.error("Invalid parameter, id is required")
        try:
            board = Board.objects.get(id=id)
        except Board.DoesNotExist:
            return self.error("Board does not exists")

        if board.created_by == user:
            board.delete()
            return self.success("Board has successfully deleted")
        else:
            return self.error("You are not the writer of this board")

class BoardListAPI(APIView):
    def get(self, request):
        if not request.GET.get("limit"):
            return self.error("Limit is needed")

        keyword = request.GET.get("keyword")
        category = request.GET.get("category")

        boards = Board.objects.all().select_related("created_by")
        if keyword:
            boards = boards.filter(title__contains=keyword)
        if category:
            boards = boards.filter(category=category)
        return self.success(self.paginate_data(request, boards, BoardListSerializer))
        