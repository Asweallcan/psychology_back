from . import api
from ..models import PaperInfo
from ..decorators import login_require
from ..utils import get_user_from_cookie, response_with_status


@api.route("/paper_list")
@login_require
def paper_info():
	user = get_user_from_cookie()
	return response_with_status(0, "Success", [paper.info_to_json(user) for paper in PaperInfo.query.all()])
