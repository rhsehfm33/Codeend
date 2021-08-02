from utils.api import APIView

from django.db.models import Q
from board.models import Board
from ..serializers import BoardSerializer, BoardListSerializer
from account.decorators import super_admin_required

class BoardAPI(APIView):
    @super_admin_required
    def get(self, request):
        if not request.GET.get("id"):
            return self.error("\"id\" param is required!")

        id = request.GET.get("id")

        if id:
            try:
                board = Board.objects.get(id=id)
            except Board.DoesNotExist:
                return self.error("Board does not exist")
            return self.success(BoardSerializer(board).data)
        else:
            self.error("\"id\" field is needed!")
    
    @super_admin_required
    def delete(self, request):
        if not request.GET.get("id"):
            return self.error("\"id\" param is required!")

        id = request.GET.get("id")
        try:
            board = Board.objects.get(id=id)
        except Board.DoesNotExist:
            return self.error("Board does not exists")

        board.delete()

class BoardListAPI(APIView):
    @super_admin_required
    def get(self, request):
        if not request.GET.get("limit"):
            return self.error("\"limit\" field is required!")

        keyword = request.GET.get("keyword")
        category = request.GET.get("category")

        boards = Board.objects.all().select_related("created_by")
        if keyword:
            boards = boards.filter(Q(title__contains=keyword) |
                                   Q(created_by__username__exact=keyword) |
                                   Q(problem___id__exact=keyword))
        if category:
            boards = boards.filter(category=category)
            
        return self.success(self.paginate_data(request, boards, BoardListSerializer))
        