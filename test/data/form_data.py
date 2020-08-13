
CREATE_FORM={
    "style": 'one-dim',
    "cn_name": "阀门参数",
    "name": "valve_args",
    "module_name": "bid",
    "page_name":"bid_data"
}

CREATE_ATTR={
    "cn_name": "配气方式",
    "name": "gov_mode",
    "symbol": "P",
    "unit":"m",
    "value_type":"integer"
}

CREATE_FORM_ATTR={
    "attr_id":1,
    "input":{
            "input_from": "table",
            "table_name":"abc",
            "display_fields":["abc"],
            "select_field":"abc",
            "addition_value":{
                            "name":"def",
                            "select_field": "def"}
            },
    "performance":{
                    "hide" : True,
                    "widget":  "drop_list",
                    "editable": True
                    },
    "dependent_attrs": ["gov_model"]
}

GET_PAGE_FORMS_ARGS={
    "module_name": "bid",
    "page_name":"bid_data"
}

