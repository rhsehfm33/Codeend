from account.decorators import super_admin_required
from judge.tasks import judge_task
# from judge.dispatcher import JudgeDispatcher
from utils.api import APIView
from ..models import Submission


class SubmissionRejudgeAPI(APIView):
    @super_admin_required
    def get(self, request):
        id = request.GET.get("id")
        if not id:
            return self.error("매개 변수 오류, ID는 필수입니다.")
        try:
            submission = Submission.objects.select_related("problem").get(id=id, contest_id__isnull=True)
        except Submission.DoesNotExist:
            return self.error("제출한 문제가 없습니다.")
        submission.statistic_info = {}
        submission.save()

        judge_task.send(submission.id, submission.problem.id)
        return self.success()
