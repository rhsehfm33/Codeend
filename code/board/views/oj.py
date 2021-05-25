from utils.api import APIView

from board.models import Board, BoardCategory
from ..serializers import CreateBoardSerializer, BoardSerializer
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
            return self.success(BoardSerializer(board).data)
        
