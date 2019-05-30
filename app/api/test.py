from . import api
from ..decorators import login_require
from ..utils import response_with_status, auto_commit_db
from ..models import Paper, User, Grade
from ..db import db
from flask import request, copy_current_request_context
from collections import Counter
import threading
import numpy as np


@api.route("/test/<int:id>", methods=["GET", "POST"])
def test(id):
    if request.method == "GET":
        return get_test_paper(id)
    elif request.method == "POST":
        return upload_answers(id)


@login_require
def get_test_paper(id):
    return response_with_status(0, "Success", Paper.query.filter_by(id=id).first().to_json())


@login_require
def upload_answers(id):
    data = request.json
    paper = Paper.query.filter_by(id=id).first()
    user = User.get_user_from_cookie()
    grade = Grade.query.filter_by(user_id=user.id, paper_id=paper.id).first()
    if not grade:
        grade = Grade(user_id=user.id, paper_id=paper.id)
        user.papers.append(paper)
        user.grades.append(grade)
        paper.grades.append(grade)
    answers = data["answers"]
    answers = "@".join(map(lambda x: str(x) if x else "", answers))
    grade.answers = answers
    grade.finished = data["finished"]
    with auto_commit_db():
        db.session.add_all([paper, user, grade])
    if data["finished"]:
        @copy_current_request_context
        def analyze_wrapper(id):
            analyze(id)

        t = threading.Thread(target=analyze_wrapper, args=(id,))
        t.start()
    return response_with_status(0, "Success")


def analyze(id):
    """
    进行试卷答案的分析
    :param id: 试卷的id
    """
    data = request.json
    paper = Paper.query.filter_by(id=id).first()
    user = User.get_user_from_cookie()
    grade = Grade.query.filter_by(user_id=user.id, paper_id=paper.id).first()
    answers = map(lambda x: map(int, list(str(x))) if x > 10 else x, data["answers"])
    # 分析个人的试卷得分
    attrs = paper.score_attrs.split("@")
    attrs_score = [0 for i in range(len(attrs))]
    answers_score = paper.answers_score.split("@")
    for index, answer in enumerate(answers):
        print(index, answer)
        if type(answer) != int:
            for answer_i in answer:
                scores = answers_score[index].split("/")[int(answer_i) - 1]
                print("multiple:", scores)
                for index_i, score in enumerate(map(int, scores.split("#"))):
                    attrs_score[index_i] += score
        else:
            scores = answers_score[index].split("/")[answer - 1]
            print("not multiple:", scores)
            for index_i, score in enumerate(map(int, scores.split("#"))):
                attrs_score[index_i] += score
    grade.score = "@".join(map(str, attrs_score))
    print(grade.score)
    grade.total_score = sum(attrs_score)
    ## 分析根据管理员设定的得分等级
    level = -1
    for index, condition in enumerate(paper.comments_condition.split("@")):
        flag = True
        for index_i, condition_i in enumerate(condition.split("/")):
            if len(condition_i) < 1:
                continue
            score = attrs_score[index_i]
            scores = list(map(int, condition_i.split("#")))
            if not (scores[1] > score > scores[0]):
                flag = False
                break
        if flag:
            level = str(index + 1)
            break
    grade.level = level
    # 计算试卷的平均分
    grades = paper.grades.filter_by(finished=True).all()
    scores = np.array([list(map(int, grade.score.split("@"))) for grade in grades])
    score_sum = np.sum(scores, axis=0)
    finished_count = len(grades)
    paper.average = "@".join(map(str, map(lambda x: round(x, 2), score_sum / finished_count)))
    # 更新试卷中每个问题的最多人选的选项
    choices = np.array([grade.answers.split("@") for grade in grades]).T
    paper.most_choice = "@".join(map(lambda x: Counter(x).most_common(1)[0][0], choices))
    # 更新成绩在所有成绩中的百分比
    attendance_count = paper.grades.count()
    attrs_above = [0 for i in range(len(attrs_score))]
    all_grades = np.array([list(map(int, grade.score.split("@"))) for grade in grades]).T
    for grade in grades:
        for index, score in enumerate(map(int, grade.score.split("@"))):
            attrs_above[index] = round(np.sum(all_grades[index] < score) / (attendance_count), 3)
        grade.above_percent = "@".join(map(str, attrs_above))
    # 记录数据库
    grade.analyzed = True
    db.session.execute(
        "UPDATE grades SET score='{score}',level='{level}',above_percent='{above_percent}',analyzed={analyzed},total_score={total_score} WHERE id={id}".format(
            score=grade.score, level=grade.level, above_percent=grade.above_percent, analyzed=grade.analyzed,
            total_score=grade.total_score, id=grade.id
        ))
    db.session.execute("UPDATE papers SET average='{average}',most_choice='{most_choice}' WHERE id={id}".format(
        average=paper.average, most_choice=paper.most_choice, id=paper.id))
    db.session.commit()
