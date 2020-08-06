
import os
import json
import shutil
import logging
from typing import Optional

from flask import current_app

from app.views.utils import ReturnCode
from app.models.function import Functions, FunctionsSchema


class FunctionUseManager:

    def __init__(self, package_route: str = None):
        package_route = 'app.views.functions.package' if package_route is None else package_route
        self._import_package(package_route)


    def _import_package(self, package_route: str):

        function_names = Functions.get_function_names()
        import_expressions_list = [f'from {package_route}.{name} import {name}' for name in function_names]
        import_expressions = '\n'.join(import_expressions_list)
        exec(
            import_expressions,
            globals()
        )

    def function_calc(self, name, **kwargs):
        funct_obj = Functions.get(name)
        input_args = funct_obj.input_args
        expression_string = name + f"({','.join(input_args)})"
        result = self.expression_calc(expression_string, **kwargs)
        return result

    def expression_calc(self, calc_expression: str, **kwargs):
        exec_string = 'EXEC_VAL=' + calc_expression
        exec(exec_string, globals(), kwargs)
        result = kwargs.get('EXEC_VAL')
        return result


class FunctionCodeManager:
    def __init__(self):
        self._package_dir = os.path.join(current_app.config.get('MAIN_DIR'), 'app', 'views', 'functions', 'package')


    def _default_backup_file_name(self, name: str) -> str:
        return f'{name}_-_backup.py'

    def _create_py_file(self, name: str, code_content: str) -> None:
        file_path = os.path.join(self._package_dir, f'{name}.py')
        assert not os.path.exists(file_path)
        with open(file_path, 'w') as f:
            f.write(code_content)

    def _modify_py_file(self, name: str, code_content: str) -> None:
        file_path = os.path.join(self._package_dir, f'{name}.py')
        assert os.path.exists(file_path)
        with open(file_path, 'w') as f:
            f.write(code_content)

    def _backup_py_file(self, name: str, backup_name: Optional[str] = None):
        if backup_name is None:
            backup_name = self._default_backup_file_name(name)
        file_path = os.path.join(self._package_dir, f'{name}.py')
        assert os.path.exists(file_path)
        bk_file_path = os.path.join(self._package_dir, f'{backup_name}.py')
        assert not os.path.exists(file_path)
        shutil.copy(file_path, bk_file_path)

    def _recover_py_file(self, name: str, backup_name: Optional[str] = None):
        if backup_name is None:
            backup_name = self._default_backup_file_name(name)
        file_path = os.path.join(self._package_dir, f'{name}.py')
        assert os.path.exists(file_path)
        bk_file_path = os.path.join(self._package_dir, f'{backup_name}.py')
        assert os.path.exists(file_path)
        shutil.copy(bk_file_path, file_path)
        os.remove(bk_file_path)

    def _delete_py_file(self, name: str):
        file_path = os.path.join(self._package_dir, f'{name}.py')
        if os.path.exists(file_path):
            os.remove(file_path)


    def add_function(self,
                     name: str,
                     input_args: list,
                     code_content: str,
                     desc: str
                     ) -> tuple:
        try:
            self._create_py_file(name, code_content)
            _ = Functions.add_record(name, input_args, code_content, desc)
            return ReturnCode.SUCCESS, ''
        except Exception as e:
            logging.error(e)
            self._delete_py_file(name)
            return ReturnCode.FAILURE, e.args


    def modify_function(self,
                         name: str,
                        **kwargs
                         ) -> None:
        try:
            if 'code_content' in kwargs:
                self._backup_py_file(name)
                self._modify_py_file(name, kwargs['code_content'])

            _ = Functions.update_record(name, **kwargs)
        except Exception as e:
            logging.error(e)
            if 'code_content' in kwargs:
                self._recover_py_file(name)
                self._delete_py_file(self._default_backup_file_name(name))


    def get_function_info(self, name: str):
        function_obj = Functions.get(name)
        return FunctionsSchema().dumps(function_obj).data

    def get_function_list(self, **kwargs):

        if 'page' in kwargs and 'per_page' in kwargs:
            page, per_page = kwargs.pop('page'), kwargs.pop('per_page')
            function_objs = Functions.query.filter_by(**kwargs).paginate(page, per_page).items
        else:
            function_objs = Functions.query.all()

        return FunctionsSchema().dump(function_objs, many=True).data

    def delete_function(self, name):
        self._delete_py_file(name)
        Functions.get(name).delete()

