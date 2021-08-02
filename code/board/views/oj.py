from utils.api import APIView

from django.db.models import Q

from board.models import Board
from problem.models import Problem
from ..serializers import (CreateBoardSerializer, BoardSerializer,
                            EditBoardSerializer, BoardListSerializer)
from account.decorators import login_required
from utils.api import validate_serializer

class BoardAPI(APIView):
    @validate_serializer(CreateBoardSerializer)
    @login_required
    def post(self, request):
        data = request.data
        if data["problem_id"]:
            try:
                problem = Problem.objects.get(_id=data["problem_id"])
            except Problem.DoesNotExist:
                return self.error("Problem does not exist")

        del data["problem_id"]
        data["created_by"] = request.user
        data["problem"] = problem
        board = Board.objects.create(**data)
        
        return self.success(BoardSerializer(board).data)
        
    def get(self, request):
        if not request.GET.get("id"):
            return self.error("\"id\" param is required!")

        id = request.GET.get("id")
        try:
            board = Board.objects.get(id=id)
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

        if data["problem_id"]:
            try:
                data["problem"] = Problem.objects.get(_id=data["problem_id"])
            except Problem.DoesNotExist:
                return self.error("Problem does not exist")

        del data["problem_id"]
        for k, v in data.items():
            setattr(board, k, v)
        board.save()
        return self.success(BoardSerializer(board).data)
    
    @login_required
    def delete(self, request):
        if not request.GET.get("id"):
            return self.error("\"id\" param is required!")

        user = request.user
        id = request.GET.get("id")
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
        