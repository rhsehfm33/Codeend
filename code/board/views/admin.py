from utils.api import APIView

from django.db.models import Q
from board.models import Board
from ..serializers import (GetBoardListSerializer, GetBoardSerializer, DeleteBoardSerializer,
                            BoardSerializer, BoardListSerializer)
from account.decorators import super_admin_required
from utils.api import validate_serializer

class BoardAPI(APIView):
    @validate_serializer(GetBoardSerializer)
    @super_admin_required
    def get(self, request):
        board_id = request.GET.get("id")
        if board_id:
            try:
                board = Board.objects.get(id=board_id)
            except Board.DoesNotExist:
                return self.error("Board does not exist")
            return self.success(BoardSerializer(board).data)
        else:
            self.error("\"id\" field is needed!")
    
    @validate_serializer(DeleteBoardSerializer)
    @super_admin_required
    def delete(self, request):
        id = request.GET.get("id")
        try:
            board = Board.objects.get(id=id)
        except Board.DoesNotExist:
            return self.error("Board does not exists")

        board.delete()

class BoardListAPI(APIView):
    @validate_serializer(GetBoardListSerializer)
    @super_admin_required
    def get(self, request):
        if not request.GET.get("limit"):
            return self.error("Limit is needed")

        keyword = request.GET.get("keyword")
        category = request.GET.get("category")

        boards = Board.objects.all().select_related("created_by")
        if keyword:
            boards = boards.filter(Q(title__contains=keyword) |
                                   Q(problem___id__exact=keyword))
        if category:
            boards = boards.filter(category=category)
        return self.success(self.paginate_data(request, boards, BoardListSerializer))
        