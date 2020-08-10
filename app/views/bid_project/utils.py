
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
        objs = BidProject.query.filter_by(**kwargs).all()
        return ReturnCode.SUCCESS, BidProjectSchema().dump(objs, many=True)
