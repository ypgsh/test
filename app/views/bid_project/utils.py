
import math
import itertools
from typing import Optional

from sqlalchemy.orm.attributes import flag_modified

from app.models.project import BidProject, BidProjectSchema
from app.models.base_data import ValveProducts, ValveProducts58, ValveProductSchema, ValveProduct58Schema

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
        template = {
            "basic_info": ['name', 'status', 'desc'],
            "turbine_unit_info": ['design_press', 'design_temp', 'design_flow', 'velocity_range'],
            "valve_info": ['series_id', 'model_id', 'model_version']
        }
        obj = BidProject.get(project_id)
        data = BidProjectSchema().dump(obj).data
        result = dict(basic_info=data,
                      turbine_unit_info=dict([(key, obj.data.get(key)) for key in template['turbine_unit_info']]),
                      valve_info=dict(series_id=obj.data.get('series_id'),
                                      model_id=obj.data.get('recommend_model_id').rsplit('-',1)[0],
                                      model_version=obj.data.get('recommend_model_id').rsplit('-',1)[1])
                      )
        return ReturnCode.SUCCESS, result

    @classmethod
    def modify_project_data(cls, project_id, **kwargs):
        obj = BidProject.get(project_id)
        obj.data.update(kwargs)
        flag_modified(obj, 'data')
        obj.save()
        return ReturnCode.SUCCESS, ''

    @classmethod
    def get_project_data(cls, project_id):
        obj = BidProject.get(project_id)
        return ReturnCode.SUCCESS, obj.data

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




    def get_matches(self):
        flow_calc_model = self._get_flow_calc_model()

        velocity_range_min, velocity_range_max = self._data['velocity_range']
        if flow_calc_model == "单个调门流量": # series 1 2 3 4

            gov_throat_diam_max = FuncCollections.equiv_diam(self._data['design_temp'],
                                                    self._data['design_press'],
                                                    self._data['design_flow'],
                                                    velocity_range_min)
            gov_throat_diam_min = FuncCollections.equiv_diam(self._data['design_temp'],
                                                             self._data['design_press'],
                                                             self._data['design_flow'],
                                                             velocity_range_max)
            gov_throat_diam_min, gov_throat_diam_max = gov_throat_diam_min*0.95, gov_throat_diam_max * 1.05
            # if self._data['series_id'] not in [5, 8]:
            product_objs = ValveProducts.query\
                                            .filter(ValveProducts.gov_throat_diam
                                                    .between(gov_throat_diam_min, gov_throat_diam_max),
                                                    ValveProducts.series_id==self._data['series_id']
                                                    )\
                                            .all()
            # else:
            #     product_objs = ValveProducts58.query \
            #         .filter(ValveProducts58.equiv_diam
            #                 .between(gov_throat_diam_min, gov_throat_diam_max),
            #                 ValveProducts58.series_id == self._data['series_id']
            #                 ) \
            #         .all()
            if not product_objs:
                return ReturnCode.FAILURE, 'not suitable gov_throat_diam'

            _ = [setattr(obj, 'press_loss', FuncCollections.press_loss(
                                                            self._data['design_temp'],
                                                            self._data['design_press'],
                                                            self._data['design_flow'],
                                                            obj.stop_throat_diam,
                                                            obj.gov_throat_diam,
                                                            (self._data['series_id'])))
                 for obj in product_objs]
            # 压损范围筛选
            in_press_loss_range_products = [obj for obj in product_objs
                                            if obj.press_loss > self._data['press_loss_range'][0]
                                                and obj.press_loss < self._data['press_loss_range'][1]
                                            ]
            if not in_press_loss_range_products:
                return ReturnCode.FAILURE, 'not suitable stop_throat_diam'

            # 计算平均流速
            _ = [setattr(obj, 'single_velocity', FuncCollections.single_velocity(
                self._data['design_temp'],
                self._data['design_press'],
                self._data['design_flow'],
                obj.gov_throat_diam,  # 5 8 系列的话就没有
            ))
                 for obj in in_press_loss_range_products]

            # 计算平均流速
            _ = [setattr(obj, 'single_velocity', FuncCollections.single_velocity(
                self._data['design_temp'],
                self._data['design_press'],
                self._data['design_flow'],
                obj.gov_throat_diam,  # 5 8 系列的话就没有
            ))
                 for obj in in_press_loss_range_products]

            data = ValveProductSchema().dump(in_press_loss_range_products, many=True)
            return ReturnCode.SUCCESS, data
        else: # series 58
            equiv_diam_max = FuncCollections.equiv_diam(self._data['design_temp'],
                                                         self._data['design_press'],
                                                         self._data['design_flow'],
                                                         velocity_range_min)

            equiv_diam_min = FuncCollections.equiv_diam(self._data['design_temp'],
                                                        self._data['design_press'],
                                                        self._data['design_flow'],
                                                        velocity_range_max)
            equiv_diam_min, equiv_diam_max = equiv_diam_min * 0.95, equiv_diam_max * 1.05

            # if self._data['series_id'] not in [5, 8]:
            #     product_objs = ValveProducts.query\
            #                                     .filter(ValveProducts.gov_throat_diam
            #                                             .between(equiv_diam_min, equiv_diam_max),
            #                                             ValveProducts.series_id==self._data['series_id']
            #                                             )\
            #                                     .all()
            # else:
            product_objs = ValveProducts58.query \
                .filter(ValveProducts58.equiv_diam
                        .between(equiv_diam_min, equiv_diam_max),
                        ValveProducts58.series_id == self._data['series_id']
                        ) \
                .all()

            if not product_objs:
                return ReturnCode.FAILURE, 'not suitable gov_throat_diam'

            if self._data['gov_mode'] == '喷嘴调节':
                # compose with series 9
                product_objs_9 = ValveProducts.query.filter_by(series_id=9).all()
                products_compose = itertools.product(product_objs, product_objs_9)

                ComposeProduct = ClassFactory.compose_product_class()
                compose_products = [ComposeProduct(*compose) for compose in products_compose]
                # 计算压损
                _ = [setattr(obj, 'press_loss', FuncCollections.press_loss(
                    self._data['design_temp'],
                    self._data['design_press'],
                    self._data['design_flow'],
                    obj.stop_product.stop_throat_diam,  # 5 8 系列的话就没有
                    obj.gov_product.equiv_diam,
                    (self._data['series_id'], 9)))
                     for obj in compose_products]
                # 压损筛选
                in_press_loss_range_products = [obj for obj in product_objs
                                                if obj.press_loss > self._data['press_loss_range'][0]
                                                and obj.press_loss < self._data['press_loss_range'][1]
                                                ]

                # 计算平均流速
                _ = [setattr(obj, 'average_velocity', FuncCollections.average_velocity(
                    self._data['design_temp'],
                    self._data['design_press'],
                    self._data['design_flow'],
                    obj.gov_product.equiv_diam,
                ))
                     for obj in in_press_loss_range_products]

                data = [ValveProduct58Schema().dump(obj.gov_product).update(ValveProductSchema().dump(obj.stop_product))
                        for obj in in_press_loss_range_products]
                return ReturnCode.SUCCESS, data
            else: # 8 series only
                # 计算压损
                _ = [setattr(obj, 'press_loss', FuncCollections.press_loss(
                                                self._data['design_temp'],
                                                self._data['design_press'],
                                                self._data['design_flow'],
                                                None,
                                                obj.equiv_diam,  # 5 8 系列的话就没有
                                                (self._data['series_id'])))
                     for obj in product_objs]
                # 压损筛选
                in_press_loss_range_products = [obj for obj in product_objs
                                                if obj.press_loss > self._data['press_loss_range'][0]
                                                and obj.press_loss < self._data['press_loss_range'][1]
                                                ]
                if not in_press_loss_range_products:
                    return ReturnCode.FAILURE, 'not suitable stop_throat_diam'

                # 计算平均流速
                _ = [setattr(obj, 'average_velocity', FuncCollections.average_velocity(
                    self._data['design_temp'],
                    self._data['design_press'],
                    self._data['design_flow'],
                    obj.equiv_diam,
                    ))
                     for obj in in_press_loss_range_products]
                data = ValveProduct58Schema().dump(in_press_loss_range_products, many=True)
                return ReturnCode.SUCCESS, data



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
    def specific_enthalphy(cls, temperature: float, pressure: float) -> float:
        """
        比焓
        :param temperature:
        :param pressure:
        :return:
        """
        from iapws import IAPWS97
        steam = IAPWS97(T=temperature + 273.15, P=pressure)
        return steam.h

    # equiv_diam == gov_diam
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
    def stop_throat_press_loss(cls,
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
    def press_loss(cls,
                       design_temp: float,
                       design_press: float,
                       design_flow: float,
                       stop_throat_diam: Optional[float],
                       gov_throat_diam: float,
                       series_compose: tuple
                       ):
        def _stop_press_loss():
            flow_coeff = cls.flow_coeff(design_press, design_flow, stop_throat_diam, specific_volume)
            if series_compose == (8, 9):
                factor = 0.0130212516287
            else:
                factor = 0.01500212516287
            return -0.91246315 * math.pow(flow_coeff, 3) \
                   + 1.200006159 * math.pow(flow_coeff, 2) \
                   - 0.0179715162 * flow_coeff \
                   + factor

        def _gov_press_loss():
            flow_coeff = cls.flow_coeff(design_press, design_flow, gov_throat_diam, specific_volume)
            if series_compose == (8, 9):
                return 0.0486201 * math.pow(flow_coeff, 3) \
                       - 0.00904913 * math.pow(flow_coeff, 2) \
                       + 0.110968943 * flow_coeff \
                       - 0.000207105545
            elif series_compose == (5, 9):

                specific_enthalphy = cls.specific_enthalphy(design_press, design_temp)
                stop_after_specific_volumne = cls.specific_volume(design_press*(1-0.015), specific_enthalphy)
                gov_limit_flow = 0.667 \
                                 * (math.pi / 4 * math.pow(gov_throat_diam / 1000, 2)) \
                                 * math.sqrt(design_press*(1-0.015) * 1000000 / stop_after_specific_volumne)
                gov_front_after_press_specific = min(20.678743 * math.pow(design_flow / 3600 / gov_limit_flow, 6)
                                                     - 53.426156 * math.pow(design_flow / 3600 / gov_limit_flow, 5)
                                                     + 55.151147 * math.pow(design_flow / 3600 / gov_limit_flow, 4)
                                                     - 28.7361 * math.pow(design_flow / 3600 / gov_limit_flow, 3)
                                                     + 7.713955 * math.pow(design_flow / 3600 / gov_limit_flow, 2)
                                                     - 1.029198 * (design_flow / 3600 / gov_limit_flow) + 1.050701
                                                     , 1)

                return (design_press*(1-0.015) - (gov_front_after_press_specific*design_press*(1-0.015))) / design_press*(1-0.015)

            else:
                assert len(series_compose) == 1
                if series_compose[0] in [1, 2]:
                    return 0.0486201 * math.pow(flow_coeff, 3)\
                           - 0.00904913 * math.pow(flow_coeff, 2)\
                           + 0.110968943 * flow_coeff\
                           - 0.000207105545
                elif series_compose[0] == 3:
                    return 0.055735 * math.pow(flow_coeff, 3)\
                           + 0.046289 * math.pow(flow_coeff, 2)\
                           + 0.106104 * flow_coeff\
                           - 0.0000682354
                elif series_compose[0] == 4:  # ?? 需要算吗
                    return 2.46741453 * math.pow(flow_coeff, 3) \
                           - 1.23069257 * math.pow(flow_coeff, 2) \
                           + 0.47302889 * flow_coeff \
                           - 0.002228355
                else:
                    raise Exception('any thing missing?')

        specific_volume = cls.specific_volume(design_temp, design_press)
        if stop_throat_diam is None:  # 8 series only
            return _gov_press_loss()
        else:
            return _stop_press_loss() + _gov_press_loss()

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

    @classmethod
    def stop_flow(cls):
        pass


class ClassFactory:

    @classmethod
    def compose_product_class(cls):
        def __init(self, gov_product, stop_product):
            self.gov_product = gov_product
            self.stop_product = stop_product
        return type('ComposeProduct', (), {'__init__': __init})