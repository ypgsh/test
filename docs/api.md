*-* 说明:  
> 1 返回内容　

按照约定, 返回内容包含api_standard, 本版本固定为1.0(特殊情况除外)　


> 2 code

| 值 | 说明 |
| ---- | ---- |
| 0   | SUCCESS |
| 1 | FAILURE  |
| 1001 | USERNAME_OR_PASSWORD_ERROR  |
| 1002 | GET_USER_INFO_ERROR  |
| 1003 | NOT_LOGIN  |
| 1004 | FORBIDDEN  |


# 一、投标项目

## 1.1 创建项目

创建任务

```
url: /api/sec_valve/v1/bid_project
method: POST
```

- 请求参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 是否必填   | 示例   |
| ------------ | ------- | ---------------------------------- | ------ | ------ |
| name   | string | 项目名称 | 是    | 董家湾 | 

*-* 示例

```
{
    "name": "董家湾"
}
```

- 返回参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 示例   |
| ------------ | ------- | ---------------------------------- | ------ |
| code   | number | 操作结果 |      |
| data | string  | 项目id                           |  |

*-* 示例

```json
{
    "api_standard": "1.0",
    "code":0,
    "data": {"id": 1}
}
```

## 1.2  修改项目信息


```
url: /api/sec_value/v1/bid_projects/<int:project_id>
method: PATCH		
```

- 请求参数：

*-* 说明

| 名称         | 类型    | 说明                               | 是否必填   | 示例   |
| ------------ | ------- | ---------------------------------- | ------ | ------ |
| name   | string | 项目名称 | 是    | 李家湾 | 

*-* 示例

```json
{
    "name": "李家湾"
}
```

- 返回参数：

*-* 说明：

| 名称 | 类型    | 说明       | 示例 |
| ---- | ------- | ---------- | ---- |
| code   | number | 操作结果 |      |
| data | object  | 任务信息           |  |

*-* 示例

```json
{
    "api_standard": "1.0",
    "code":0
}
```

## 1.3  获取项目列表


```
url: /api/sec_valve/v1/bid_projects
method: GET	
```

- 请求参数：

*-* 说明


| 名称         | 类型    | 说明                               | 是否必填   | 示例   |
| ------------ | ------- | ---------------------------------- | ------ | ------ |
| page       | number | 第几页                                                     |  是 |
| per_page | number  | 每页几行                                                     |    是    |

*-* 示例

```json
{
    "page": 1,
    "per_page": 10
}
```
 
- 返回参数：

*-* 说明：

| 名称 | 类型    | 说明       | 示例 |
| ---- | ------- | ---------- | ---- |
| code   | number | 操作结果 |      |
| data | obj  | 项目信息列表           |  |


*-* 示例

```json
{
    "api_standard": "1.0",
    "code":0,
    "data": { 
            "projects":[
                        {
                        "name": "延长室友榆神能化动力站",
                        "status":"投标中", 
                        "director": "张三",
                        "update_time": "2019-11-21T08:05:09.504299+00:00"
                    }],
            "total": 20
            }
}
```

## 1.3  获取某项目简介

```
url: /api/sec_valve/v1/bid_projects/<int:project_id>/brief
method: GET	
```

- 请求参数：

*-* 说明

 NA
 
*-* 示例
 
 NA

- 返回参数：

*-* 说明：

| 名称 | 类型    | 说明       | 示例 |
| ---- | ------- | ---------- | ---- |
| code   | number | 操作结果 |      |
| data | object  | 项目信息           |  |

*-* 示例

```json
{
    "api_standard": "1.0",
    "code":0,
    "data": {
                "type": "投标选型",
                "name":"项目名称", 
                "design_temp":"530",
                "director": "张三"
            }
}
```
## 1.4 获取表单渲染信息
```
url: /api/sec_valve/v1/form_render
method: GET
```

- 请求参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 是否必填   | 示例   |
| ------------ | ------- | ---------------------------------- | ------ | ------ |
| module_name   | string | 函数描述 | 是    | bid | 
| page_name   | string | 输入参数列表 | 是    |  |

*-* 示例

```json
{
    "module_name": "bid",
    "page_name":"bid_data"
}
```

- 返回参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 示例   |
| ------------ | ------- | ---------------------------------- | ------ |
| code   | number | 操作结果 |      |
| data | object | 该也配置的表格信息                         |  |

*-* 示例

```json
{
    "api_standard": "1.0",
    "code":0,
    "data": [
        {
        "id": 1,
        "cn_name": "阀门参数",
        "name": "valve_args",
        "attrs":[
                {
                 "id":5,
                 "cn_name": "配气方式",
                 "name": "gov_mode",
                 "symbol": "P",
                 "unit":"m",
                 "value_type":"string",
                 "input":{
                        "input_from": "table", 
                        "table_name":"abc", 
                        "display_fields":["abc"], 
                        "select_field":"abc", 
                        "addition_attr":{
                                        "name":"def", 
                                        "select_field": "def"}
                        },
                "performance":{
                                "hide" : true, 
                                "widget":  "drop_list",
                                "editable": true 
                                },
                "affect_attrs": ["other"]
            },
            {
                 "id":10,
                 "cn_name": "阀门系列",
                 "name": "valve_series",
                 "symbol": "",
                 "unit":"",
                 "value_type":"integer",
                 "input":{
                        "input_from": "func", 
                        "funcn_name":"func123"
                        },
                "performance":{
                                "hide" : true, 
                                "widget":  "drop_list",
                                "editable": true 
                                },
                "affect_attrs": ["other"]
            }
        ]
    }
    ]
 }
```

## 1.5 获取表单渲染数据信息
```
url: /api/sec_valve/v1/form_data
method: GET
```

- 请求参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 是否必填   | 示例   |
| ------------ | ------- | ---------------------------------- | ------ | ------ |
| form_id   | integer | form_id | 是    | 1 | 
| project_id   | integer | 项目id | 是    | 2 |

*-* 示例

```json
{
    "form_id": 1,
    "project_id": 2
}
```

- 返回参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 示例   |
| ------------ | ------- | ---------------------------------- | ------ |
| code   | number | 操作结果 |      |
| data | object | 该也配置的表格信息                         |  |

*-* 示例

```
{
    "api_standard": "1.0",
    "code":0,
    "data": {
             
             "gov_mode": "全周进气",
             "series_id": 1,
             "supply_series_id": 9, # 配套阀门系列,
             "flow_calc_mode": "单调门流量"
        }
}
```

## 1.5 保存修改项目数据
```
url: /api/sec_valve/v1/bid_projects/<int:project_id>/data
method: POST
```

- 请求参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 是否必填   | 示例   |
| ------------ | ------- | ---------------------------------- | ------ | ------ |
| series_id   | integer | 阀门系列 | 否    | 1 |

*-* 示例

```json
{
    "series_id": 1,
    "gov_mode": "喷嘴调节"
}
```

- 返回参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 示例   |
| ------------ | ------- | ---------------------------------- | ------ |
| code   | number | 操作结果 |      |

*-* 示例

```json
{
    "api_standard": "1.0",
    "code":0
}
```

## 1.6 获取适用的阀门信息列表
```
url: /api/sec_valve/v1/bid_project/<int:project_id>/matches
method: GET
```

- 请求参数：

  NA

- 返回参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 示例   |
| ------------ | ------- | ---------------------------------- | ------ |
| code   | number | 操作结果 |      |
| data | array | 查询到匹配该项目的阀门数据                          |  |

*-* 示例

```
{
    "api_standard": "1.0",
    "code":0,
    "data": [
         {
            "model_id": "VSL-165-130-12-05-50",
            "model_version": "00",
            "stop_throat_diam": 60,  # 主门口径
            "gov_throat_diam": 60, # 调门口径
            "press_loss": 2.1  #阀门压损
            "press_level": 110 # 压力等级
            "temp_level": 110 # 温度等级
            "series_id": 2 # 阀门系列
            "design_press": 5 # 设计压力
            "design_temp": 500 # 设计温度
            "casing_mat_name": "2G15CR" # 阀壳材料
            "stem_mat_name": "22cR12N" # 阀杆材料
            "total_weight": 20 # 总重
            "stop_throat_speed": 13 # 主门流速
            "gov_throat_speed": 14 # 调门流速
            "speed_mode": "阀门平均流速"
         }
    ]
}
或 (5,8系列配套9场景)
{
    "api_standard": "1.0",
    "code":0,
    "data": [
         {
            "model_id": "VSL-165-130-12-05-50-00", # 主门型号        
            "gov_model_id": "VSL-165-130-12-05-50-00", # 调门型号    
            "stop_throat_diam": 60,  # 主门口径
            "equiv_throat_diam": 60,  # 当量口径
            "press_loss": 2.1  #阀门压损
            "press_level": 110 # 压力等级
            "temp_level": 110 # 温度等级
            "series_id": 2 # 阀门系列
            "design_press": 5 # 设计压力
            "design_temp": 500 # 设计温度
            "casing_mat_name": "2G15CR" # 阀壳材料
            "stem_mat_name": "22cR12N" # 阀杆材料
            "total_weight": 20 # 总重
            "stop_throat_speed": 13 # 主门流速
            "gov_throat_speed": 14 # 调门流速
            "supply_model_info": {
                    "series_id": 9 # 阀门系列
                    "model_id": "VSL-165-130-12-05-50-00", # 调门型号
                    "design_press": 5 # 设计压力
                    "design_temp": 500 # 设计温度
                    "casing_mat_name": "2G15CR" # 阀壳材料
                    "stem_mat_name": "22cR12N" # 阀杆材料
                    "total_weight": "22cR12N" # 总重
                }
         }
    ]
}
或 (5,8系列不配套9场景)
{
    "api_standard": "1.0",
    "code":0,
    "data": [
         {
            "model_id": "VSL-165-130-12-05-50-00",
            "equiv_throat_diam": 60,  # 当量口径
            "press_loss": 2.1  #阀门压损
            "press_level": 110 # 压力等级
            "temp_level": 110 # 温度等级
            "series_id": 2 # 阀门系列
            "design_press": 5 # 设计压力
            "design_temp": 500 # 设计温度
            "casing_mat_name": "2G15CR" # 阀壳材料
            "stem_mat_name": "22cR12N" # 阀杆材料
            "total_weight": 20 # 总重
            "stop_throat_speed": 13 # 主门流速
            "gov_throat_speed": 14 # 调门流速
         }
    ]
}
```

## 1.6 保存预选型号/保存推荐型号
```
url: /api/sec_valve/v1/bid_project/<int:project_id>/result
method: POST
```

- 请求参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 是否必填   | 示例   |
| ------------ | ------- | ---------------------------------- | ------ | ------ |
| candidate_model_ids   | array | 选中的推荐型号 | 是    | ["sxl-1"] |
| recomend_model_id   | string | 推荐型号 | 是    | "sxl-1" |

*-* 示例

```json
{
    "candidate_model_ids":  ["VSL-165-130-12-05-50-00"]
}
```

```json
{
    "recomend_model_id":"VSL-165-130-12-05-50-00"
}
```

- 返回参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 示例   |
| ------------ | ------- | ---------------------------------- | ------ |
| code   | number | 操作结果 |      |

*-* 示例

```
{
    "api_standard": "1.0",
    "code":0
}
```

## 1.6 获取推荐型号选型数据
```
url: /api/sec_valve/v1/bid_project/<int:project_id>/data
method: GET
```

- 请求参数：

  NA

- 返回参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 示例   |
| ------------ | ------- | ---------------------------------- | ------ |
| code   | number | 操作结果 |      |
| data   | object | 操作结果 |      |

*-* 示例

```
{
    "api_standard": "1.0",
    "code":0,
    "data": {
            "design_temp": 500,
            "gov_mode": "",
            ...    
    
    }
    
}
```


# 二 表格相关
## 2.1 配置表格
```
url: /api/sec_valve/v1/form
method: POST	
```
- 请求参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 是否必填   | 示例   |
| ------------ | ------- | ---------------------------------- | ------ | ------ |
| cn_name   | string | 表格名称 | 是    | 阀门参数 | 
| name   | string | 变量名 | 是    | valve_args | 
| module_name   | string | 函数描述 | 是    | bid | 
| page_name   | string | 输入参数列表 | bid_data    |  |

*-* 示例

```json
{
    "cn_name": "阀门参数",
    "name": "valve_args",
    "module_name": "bid",
    "page_name":"bid_data"
}
```

- 返回参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 示例   |
| ------------ | ------- | ---------------------------------- | ------ |
| code   | number | 操作结果 |      |
| data   | number | form id |      |

*-* 示例

```json
{
    "api_standard": "1.0",
    "code":0,
    "data": {"id": 1}
}
```

## 2.2 配置属性
```
url: /api/sec_valve/v1/attr
method: POST	
```
- 请求参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 是否必填   | 示例   |
| ------------ | ------- | ---------------------------------- | ------ | ------ |
| name   | integer | 参数名 |  是   | 配气方式 | 
| name   | string | 参数变量 | 是    | gov_mode | 
| symbol   | string | 符号 | 否    | P | 
| unit   | string | 单位 | 否    |  |
| value_type   | string | 值类型 | 是 | integer |

*-* 示例

```json
{
    "cn_name": "配气方式",
    "name": "gov_mode",
    "symbol": "P",
    "unit":"m",
    "value_type":"integer"
}
```

- 返回参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 示例   |
| ------------ | ------- | ---------------------------------- | ------ |
| code   | number | 操作结果 |      |
| data   | number | attr id |      |

*-* 示例

```json
{
    "api_standard": "1.0",
    "code":0,
    "data": {"id": 1}
}
```

## 2.3 获取已有属性列表
```
url: /api/sec_valve/v1/attrs
method: GET	
```
- 请求参数：

  NA

- 返回参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 示例   |
| ------------ | ------- | ---------------------------------- | ------ |
| code   | number | 操作结果 |      |
| data   | number | attr id |      |

*-* 示例
```json
{
    "api_standard": "1.0",
    "code":0,
    "data": [
            {   
                "id": 1,
                "cn_name": "配气方式",
                "name": "gov_mode",
                "symbol": "P",
                "unit":"m",
                "value_type":"string"
            },
            {
                "id": 2,
                "cn_name": "阀门系列",
                "name": "valve_series",
                "symbol": "",
                "unit": "",
                "value_type": "integer"
            }
    ]
}
```

## 2.3 配置表单属性
```
url: /api/sec_valve/v1/forms/<int:form_id>/attr
method: POST	
```
- 请求参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 是否必填   | 示例   |
| ------------ | ------- | ---------------------------------- | ------ | ------ |
| attr_id   | integer | 属性id |  是   | 1 |
| input   | object | 输入方式等信息 |  是   |  |
| performance   |  object| 页面行为 |  是   |  |
| depend_attrs  | array | 依赖参数 | 否    |  |
| comments  | object | 备注 | 否    |  |

input解释
```
- 数据表
{
  "input_from": "table",
  "table_name": "abc",  
  "display_fields":["abc"], # 展示那些字段 
  "select_field":"abc",    # 选中时取那一列的值
  "addition_attr":{"name": "def",  # 选中时,同时记录那些数据
                  "cn_name"; "呵呵"
                 "select_field": "def"}
  }
  
- 函数计算
{
    "input_from": "function",
    "function_name": "calc_len"
}

- 表达式计算
{
    "input_from": "expression",
    "expression_content": "3.14 * {abc}"
}

- 用户直接输入
{
    "input_from": "user_input"
}

- 值已经有了, 不需要填也不需要算,直接呈现
{
    "input_from": "auto_fill"
}
```

performance解释
```
{
    "hide": True, # 可见
    "widget": "drop_list",   # drop_list / input /PopupWindow控件
    "editable": True, # 状态
    "update_trigger" = "user_click" # auto/user_click 更新触发
    "validate":{          #验证
                "constrain"": {min:0, max: 120}, # 验证条件 
                "alert": "PopupWindow"  # 提醒方式
                }
}
            
```

comments解释
```
{
    "has_comments": True,
    "source": "internal" #备注来源, 内部的提供变量名, 外部的直接数输入字符串
    "relate_val_name": "gov_mode" # 内部变量名
}
```

*-* 示例

```json
{
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
                    "hide" : true, 
                    "widget":  "drop_list",
                    "editable": true 
                    },
    "depend_attrs": ["gov_mode1"]
}
```

- 返回参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 示例   |
| ------------ | ------- | ---------------------------------- | ------ |
| code   | number | 操作结果 |      |
| data   | number | form_attr_id |      |

*-* 示例

```json
{
    "api_standard": "1.0",
    "code":0,
    "data": {"id": 1}
}
```
## 2.4
获取某page的表单列表
```
url: /api/sec_valve/v1/forms
method: GET	
```
- 请求参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 是否必填   | 示例   |
| ------------ | ------- | ---------------------------------- | ------ | ------ |
| module_name   | string | 函数描述 | 是    | bid | 
| page_name   | string | 输入参数列表 | bid_data    |  |

*-* 示例

```json
{ 
    "module_name": "bid",
    "page_name":"bid_data"
}
```

- 返回参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 示例   |
| ------------ | ------- | ---------------------------------- | ------ |
| code   | number | 操作结果 |      |
| data   | array | form 列表 |      |

*-* 示例

```json
{
    "api_standard": "1.0",
    "code":0,
    "data": [
                {
                    "id": 1,
                    "cn_name": "阀门参数",
                    "name": "valve_args"
                },
                {
                    "id": 2,
                    "cn_name": "机组参数",
                    "name": "unit_args"
                }
    ]
}
```

## 2.4
获取某表单属性列表
```
url: /api/sec_valve/v1/forms/<int:form_id>/attrs
method: GET	
```
- 请求参数：

  NA

- 返回参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 示例   |
| ------------ | ------- | ---------------------------------- | ------ |
| code   | number | 操作结果 |      |
| data   | array | form的属性列表 |      |

*-* 示例

```json
{
    "api_standard": "1.0",
    "code":0,
    "data": [
                {
                    "id": 1,
                    "cn_name": "配器方式",
                    "name": "gov_mod"
                },
                {
                    "id": 2,
                    "cn_name": "阀门系列",
                    "name": "valve_series"
                }
    ]
}
```

## 2.5
获取某表单某属性内容
```
url: /api/sec_valve/v1/form/<int:form_id>/attrs/<int:form_attr_id>
method: GET	
```
- 请求参数：

  NA

- 返回参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 示例   |
| ------------ | ------- | ---------------------------------- | ------ |
| code   | number | 操作结果 |      |
| data   | object | form的属性详细内容 |      |

*-* 示例

```json
 {  "api_standard": "1.0",
    "code":0,
    "data":{
    "form_id":1,
    "attr_id":1,
    "input":{
            "input_from": "table", 
            "table_name":"abc", 
            "display_fields":["abc"], 
            "select_field":"abc", 
            "addition_attr":{
                            "name":"def", 
                            "select_field": "def"}
            },
    "performance":{
                    "hide" : true, 
                    "widget":  "drop_list",
                    "editable": true 
                    },
    "depend_attrs": ["gov_mode1"]
  }
}

```

## 2.6
获取修改参数属性
```
url: /api/sec_valve/v1/attrs/<int:attr_id>
method: PATCH	
```
- 请求参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 是否必填   | 示例   |
| ------------ | ------- | ---------------------------------- | ------ | ------ |
| name   | integer | 参数名 |  是   | 配气方式 |
| symbol   | string | 符号 | 否    | P | 
| unit   | string | 单位 | 否    |  |
| value_type   | string | 值类型 | 是 | integer |

*-* 示例

```json
{
    "cn_name": "配气方式",
    "symbol": "P",
    "unit":"m",
    "value_type":"integer"
}
```

- 返回参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 示例   |
| ------------ | ------- | ---------------------------------- | ------ |
| code   | number | 操作结果 |      |
*-* 示例

```json
{  "api_standard": "1.0",
    "code": 0
}

```

# 三 自定义函数相关
## 3.1 创建函数
```
url: /api/sec_valve/v1/function
method: POST	
```
- 请求参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 是否必填   | 示例   |
| ------------ | ------- | ---------------------------------- | ------ | ------ |
| name   | string | 函数名称 | 是    |  | 
| desc   | string | 函数描述 | 否    |  | 
| input_args   | array | 输入参数列表 | 是    |  | 
| code_content   | string | 函数体 | 是    |  | 

*-* 示例

```json
{
    "name": "calc_len",
    "desc": "计算长度",
    "input_args": ["dim", "length"],
    "code_content":"def run(dim, length):\n    return dim * length"
}
```

- 返回参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 示例   |
| ------------ | ------- | ---------------------------------- | ------ |
| code   | number | 操作结果 |      |

*-* 示例

```json
{
    "api_standard": "1.0",
    "code":0
}
```
## 3.2 测试函数
```
url: /api/sec_valve/v1/function/test
method: POST	
```
- 请求参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 是否必填   | 示例   |
| ------------ | ------- | ---------------------------------- | ------ | ------ |
| name   | string | 函数名称 | 是    |  | 
| input_args   | object | 输入参数值 | 是    |  |

*-* 示例

```json
{
    "name": "calc_len",
    "input_args": {"dim":12, "length":10 }
}
```

- 返回参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 示例   |
| ------------ | ------- | ---------------------------------- | ------ |
| code   | number | 操作结果 |      |
| data | string or other? | 结果返回值                           |  |

*-* 示例

```json
{
    "api_standard": "1.0",
    "code":0,
    "data": 12
}
```
## 3.3 修改函数
```
url: /api/sec_valve/v1/functions/<funcn_name>
method: PATCH	
```
- 请求参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 是否必填   | 示例   |
| ------------ | ------- | ---------------------------------- | ------ | ------ |
| desc   | string | 函数描述 | 否    |  | 
| input_args   | array | 输入参数列表 | 否    |  | 
| code_content   | string | 函数体, input_args变了此处一定要变 | 否    |  | 

*-* 示例

```json
{   
    "desc": "计算长度",
    "input_args": ["dim", "length"],
    "code_content":"def run(dim, length):\n    return dim * length"
}
```

- 返回参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 示例   |
| ------------ | ------- | ---------------------------------- | ------ |
| code   | number | 操作结果 |      |

*-* 示例

```json
{
    "api_standard": "1.0",
    "code":0
}
```
## 3.4 函数列表
```
url: /api/sec_valve/v1/functions
method: GET	
```
- 请求参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 是否必填   | 示例   |
| ------------ | ------- | ---------------------------------- | ------ | ------ |
| return_infos   | array | 返回值包含信息(name, input_args, desc, code_content) | 否    | 默认都包含 | 

*-* 示例

```json
{   
    "return_infos": ["name", "desc"]
}
```

- 返回参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 示例   |
| ------------ | ------- | ---------------------------------- | ------ |
| code   | number | 操作结果 |      |
| data   | array | 返回信息 |      |

*-* 示例

```json
{
    "api_standard": "1.0",
    "code":0,
    "data":[
             {
              "name":"funct1",
              "desc": "desc1"
              },
             {
             "name":"funct2",
             "desc": "desc2"
             }     
    ]
}
```
## 3.5 具体函数信息
```
url: /api/sec_valve/v1/functions/<funcn_name>
method: GET	
```
- 请求参数：

  NA

- 返回参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 示例   |
| ------------ | ------- | ---------------------------------- | ------ |
| code   | number | 操作结果 |      |
| data   | object | 函数信息 |      |

*-* 示例

```json
{
    "api_standard": "1.0",
    "code":0,
    "data": {
            "name": "calc_len",
            "desc": "计算长度",
            "input_args": ["dim", "length"],
            "code_content":"def run(dim, length):\n    return dim * length"
        }
}
```

## 3.6 调用函数计算值
```
url: /api/sec_valve/v1/function/compute
method: GET	
```
- 请求参数：

*-* 说明：

| 名称         | 类型    | 说明                               |  是否必填  |  示例  |
| ------------ | ------- | ---------------------------------- | ------ | ---- |
| fn   | string | 函数名称 |    是  |
| project_id   | integer | 项目id |   是   |


*-* 示例

```json
{   
    "fn": "calc_len",
    "project_id": 1
}
```

- 返回参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 示例   |
| ------------ | ------- | ---------------------------------- | ------ |
| fn   | string | 函数名称 |      |
| data   |   | 返回值 |      |

*-* 示例

```json
{
    "api_standard": "1.0",
    "code":0,
    "data": ""
}
```

# 四 基础数据相关
## 4.1 基础数据表列表
```
url: /api/sec_valve/v1/base_dbs
method: GET	
```
- 请求参数：

  NA

- 返回参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 示例   |
| ------------ | ------- | ---------------------------------- | ------ |
| code   | number | 操作结果 |      |
| data   | array | 返回信息 |      |

*-* 示例

```json
{
    "api_standard": "1.0",
    "code":0,
    "data":[{
            "cn_name": "阀门产品库",
            "value":"valve_products_table"
            },
            {
            "cn_name": "流速表",
            "value": "speed_range_table"
            }  
    ]
}
```

## 4.2 获取某基础数据表数据
```
url: /api/sec_valve/v1/base_dbs/<string:tablename>
method: GET	
```
- 请求参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 是否必填   | 示例   |
| ------------ | ------- | ---------------------------------- | ------ | ------ |
| fields   | array | 包含信息(name, input_args,等根据具体情况看) | 否    | 默认都包含 | 

*-* 示例

```json
{   
    "fields": ["name", "pressure"]
}
```


- 返回参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 示例   |
| ------------ | ------- | ---------------------------------- | ------ |
| code   | number | 操作结果 |      |
| data   | object | 返回信息 |      |

*-* 示例

```json
{
    "api_standard": "1.0",
    "code":0,
    
    "data":{
      "header":[
                {
                  "cn_name": "机组运行方式",
                  "name": "hh"
                  },
                {
                  "cn_name": "阀门压损范围", 
                  "name": "aa"
                  }
              ],
      "body":[
              {                
                "hh": 222,
                "aa": 111
            },
            {
                "hh": 333,
                "aa": 444
            }  
    ]
    }
}
```

## 4.3 阀门某系列简介
```
url: /api/sec_valve/v1/base_dbs/valve_series/<int:series_id>/brief
method: GET	
```
- 请求参数：

  NA

- 返回参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 示例   |
| ------------ | ------- | ---------------------------------- | ------ |
| code   | number | 操作结果 |      |
| data   | object | 阀门系列信息 |      |

*-* 示例

```json
{
    "api_standard": "1.0",
    "code":0,
    "data":{
            "structure": "提升式",
            "use_scene": "适用于全周进气",
            "typical_turbine_units": ["196中压", "169高中压"],
            "sketch": "data:image/jpeg;base64,exETFEdeD1RE..."
    }
}
```

# 五 获取表达式计算值
## 5.1 获取表达式计算值
```
url: /api/sec_valve/v1/expression/compute
method: GET	
```
- 请求参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 是否必填   |  示例 |
| ------------ | ------- | ---------------------------------- | ------ |--- |
| project_id   | integer | 项目id |    是  | |
| expression   | string | 表达式 |  是    | |


*-* 示例

```json
{   
    "expression": "3.14 * 1.2",
    "project_id": 1
}
```

- 返回参数：

*-* 说明：

| 名称         | 类型    | 说明                               | 示例   |
| ------------ | ------- | ---------------------------------- | ------ |
| data   |   | 返回值 |      |

*-* 示例

```json
{
    "api_standard": "1.0",
    "code":0,
    "data": ""
}
```