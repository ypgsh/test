
import math

from sqlalchemy.orm.attributes import flag_modified

from app.models.project import BidProject, BidProjectSchema

from app.views.utils import ReturnCode


PROJECT_BRIEF_INFO_KEYS = ['name', "status", "director", "update_time"]

class BidProjectManager:

    @classmethod
    def create_project(cls,**kwargs):
        obj = BidProject(data=kwargs).save()
        return ReturnCode.SUCCESS, obj.id

    @classmethod
    def get_projects(cls, **kwargs):
        page, per_page = kwargs.pop('page', None), kwargs.pop('per_page', None)

        total_objs = BidProject.query.filter_by(**kwargs).all()
        if page and per_page:
            page, per_page = int(page), int(per_page)
            task_objs = BidProject.query.filter_by(**kwargs).paginate(page, per_page).items
        else:
            task_objs = total_objs
        total_num = len(total_objs)
        pages = math.ceil(total_num / per_page) if per_page else 1
        data = BidProjectSchema().dump(task_objs, many=True).data
        return ReturnCode.SUCCESS, dict(projects=data,
                                        total_num=total_num,
                                        pages=pages
                                        )

    @classmethod
    def get_project_brief(cls, project_id: int):

        obj = BidProject.get(project_id)
        data = BidProjectSchema().dump(obj).data
        return ReturnCode.SUCCESS, data

    @classmethod
    def modify_project_data(cls, project_id, **kwargs):
        obj = BidProject.get(project_id)
        obj.data.update(kwargs)
        flag_modified(obj, 'data')
        obj.save()
        return ReturnCode.SUCCESS, ''

