
import math

from sqlalchemy.orm.attributes import flag_modified

from app.models.project import BidProject, BidProjectSchema
from app.models.base_data import ValveProducts, ValveProducts58

from app.views.utils import ReturnCode

from app.views.forms.utils import FormManager

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

    @classmethod
    def get_form_data(cls, project_id: int, form_id: int):
        _, form_attrs = FormManager.get_form_brief_attrs(form_id)
        attr_names = [o['name'] for o in form_attrs]
        project_obj = BidProject.get(project_id)
        project_data = project_obj.data
        result = dict([(name, project_data.get(name)) for name in attr_names])
        return ReturnCode.SUCCESS, result
    @classmethod
    def if_need_series_compose(cls, project_id) -> True:
        project_obj = BidProject.get(project_id)
        project_data = project_obj.data
        if project_data.get('gov_mode') == '喷嘴调节' and project_data.get('series_id') in [5, 8]:
            return True
        return False

    @classmethod
    def get_matches(cls, project_id: int) -> tuple:
        project_matcher = BidProjectMatcher(project_id)
        return project_matcher.get_matches()


from collections import namedtuple
FlowCalcModelConfig = namedtuple('FlowCalcModel', 'flow_calc_model series_ids')

class BidProjectMatcher:
    def __init__(self, project_id: int):
        self._data = self._get_project_data(project_id)

        self._FLOW_CALC_MODEL_CONFIGS =[
            FlowCalcModelConfig('单个调门流量', [1, 2, 3, 4]),
            FlowCalcModelConfig('阀门总流量', [5, 8])]

    def _get_project_data(self, project_id: int):
        return BidProject.get_project_data(project_id)

    def _get_flow_calc_model(self):
        series_id = self._data.get('series_id')
        if series_id is None:
            raise Exception('series id is empty')
        for config in self._FLOW_CALC_MODEL_CONFIGS:
            if series_id in config.series_ids:
                return config.flow_calc_model
        raise Exception('unsupported series id: {}'.format(series_id))

    def _get_recommend_velocity(self) -> float:
        pass

    def get_matches(self):
        flow_calc_model = self._get_flow_calc_model()
        recommend_velocity = self._get_recommend_velocity()
        if flow_calc_model == "单个调门流量":
            gov_throat_diam = FuncCollections.equiv_diam(self._data['design_temp'],
                                                    self._data['design_press'],
                                                    self._data['design_flow'],
                                                    recommend_velocity)
            gov_throat_diam_min, gov_throat_diam_max = gov_throat_diam*0.95, gov_throat_diam * 1.05
            product_objs = ValveProducts.query\
                                            .filter(ValveProducts.gov_throat_diam
                                                    .between(gov_throat_diam_min, gov_throat_diam_max)
                                                    )\
                                            .all()
            if not product_objs:
                return ReturnCode.FAILURE, 'not suitable gov_throat_diam'

            _ = [setattr(obj, 'press_loss', FuncCollections.press_loss(
                                                            self._data['design_temp'],
                                                            self._data['design_press'],
                                                            self._data['design_flow'],
                                                            obj.stop_throat_diam,
                                                            (self._data['series_id'])))
                 for obj in product_objs]

            in_press_loss_range_products = [obj for obj in product_objs
                                            if obj.press_loss > self._data['press_loss_range'][0]
                                                and obj.press_loss < self._data['press_loss_range'][1]
                                            ]
            if not in_press_loss_range_products:
                return ReturnCode.FAILURE, 'not suitable stop_throat_diam'
            return ReturnCode.SUCCESS, in_press_loss_range_products
        else:
            equiv_diam = FuncCollections.equiv_diam(self._data['design_temp'],
                                                         self._data['design_press'],
                                                         self._data['design_flow'],
                                                         recommend_velocity)
            equiv_diam_min, equiv_diam_max = equiv_diam * 0.95, equiv_diam * 1.05
            product_objs58 = ValveProducts58.query \
                .filter(ValveProducts.stop_throat_diam
                        .between(equiv_diam_min, equiv_diam_min)
                        ) \
                .all()


            if not product_objs58:
                return ReturnCode.FAILURE, 'not suitable gov_throat_diam'
            if self._data['gov_mode'] == '喷嘴调节':
                product_objs_9 = ValveProducts.query \
                    .filter(ValveProducts.gov_throat_diam
                            .between(equiv_diam_min, equiv_diam_min)
                            ) \
                    .all()
                pass
            else:
                _ = [setattr(obj, 'press_loss', FuncCollections.press_loss(
                                                self._data['design_temp'],
                                                self._data['design_press'],
                                                self._data['design_flow'],
                                                obj.stop_throat_diam,
                                                (self._data['series_id'])))
                     for obj in product_objs58]

                in_press_loss_range_products = [obj for obj in product_objs58
                                                if obj.press_loss > self._data['press_loss_range'][0]
                                                and obj.press_loss < self._data['press_loss_range'][1]
                                                ]
                if not in_press_loss_range_products:
                    return ReturnCode.FAILURE, 'not suitable stop_throat_diam'
                return ReturnCode.SUCCESS, in_press_loss_range_products


class FuncCollections:
    # TODO: REFACTOR
    @classmethod
    def specific_volume(cls, temperature: float, pressure: float) -> float:
        """
        比容
        :param temperature:
        :param pressure:
        :return:
        """
        from iapws import IAPWS97
        steam = IAPWS97(T=temperature + 273.15, P=pressure)
        return steam.v

    @classmethod
    def equiv_diam(cls, design_temp: float,
                   design_press: float,
                   design_flow: float,
                   recommend_velocity: float):
        # TODO: where recommend velocity come from?
        specific_volume = cls.specific_volume(design_temp, design_press)
        return math.sqrt(
                         (design_flow * 4 * 3600 * specific_volume)
                         /recommend_velocity
                         /math.pi) \
                        * 1000

    @classmethod
    def press_loss(cls,
                   design_temp: float,
                   design_press: float,
                   design_flow: float,
                   throat_diam: float,
                   series_compose: tuple
                   ):
        specific_volume = cls.specific_volume(design_temp, design_press)
        flow_coeff = cls.flow_coeff(design_press,design_flow,throat_diam, specific_volume)
        if series_compose == (8, 9):
            factor = 0.0130212516287
        else:
            factor = 0.01500212516287
        return -0.91246315 * math.pow(flow_coeff, 3) \
               + 1.200006159*math.pow(flow_coeff, 2) \
               - 0.0179715162*flow_coeff \
               + factor

    @classmethod
    def flow_coeff(cls,
                   design_press: float,
                   design_flow: float,
                   throat_diam: float,
                   specific_volume: float):
        return (design_flow/3600) \
               * math.sqrt(design_press * 1000000 * specific_volume) \
               / (math.pi * math.pow(throat_diam, 2)/4/100000) \
               / (design_press * 1000000)

    # 平均调门流速
    @classmethod
    def average_velocity(cls,
                         design_temp: float,
                         design_press: float,
                         design_total_flow: float,
                         equiv_diam: float):
        specific_volume = cls.specific_volume(design_temp, design_press)
        return math.sqrt(design_total_flow*4*3600*specific_volume/(equiv_diam/1000)/math.pi)

    #单个调门流速
    @classmethod
    def single_velocity(cls,
                         design_temp: float,
                         design_press: float,
                         design_single_flow: float,
                         gov_diam: float):
        specific_volume = cls.specific_volume(design_temp, design_press)
        return math.sqrt(design_single_flow * 4 * 3600 * specific_volume / (gov_diam / 1000) / math.pi)

    # 主门流速
    @classmethod
    def stop_velocity(cls,
                         design_temp: float,
                         design_press: float,
                         stop_flow: float,
                         stop_diam: float):
        specific_volume = cls.specific_volume(design_temp, design_press)
        return math.sqrt(stop_flow * 4 * 3600 * specific_volume / (stop_diam / 1000) / math.pi)