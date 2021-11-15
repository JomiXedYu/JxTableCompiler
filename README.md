# JxTableCompiler
使用Excel表格，生成编程语言数据结构，生成数据源。

### 如何使用
首先使用Excel编辑，仅支持后缀为.xlsx的表格  

- 第一行为注释，会根据支持情况生成至结构或数据中
- 第二行为数据类型，如果为空则默认string，可以查看[支持的数据类型](#支持的数据类型)
- 第三行字段名
- 三行以下为数据


| 编号  | 内容    |
| ----- | ------- |
| int32 | string  |
| Id    | Content |
| 1     | 内容1   |
| 2     | 内容2   |

使用命令行执行`Main.py`：  
可以使用`py Main.py -h`来查询指令  

```
positional arguments:
  file                  excel.xlsx or paths.txt

optional arguments:
  -h, --help            show this help message and exit
  --model MODEL         model generator
  --model_out MODEL_OUT
                        model output folder
  --combine_model COMBINE_MODEL
                        bool
  --data DATA           data compiler
  --data_out DATA_OUT   data output folder
  --combine_data COMBINE_DATA
                        bool
```
第一个参数file为必选，需要传入以xlsx结尾的表格，或者用换行分割储存xlsx文件列表的txt文件。  
可选参数：  
`--model`，选择一个结构生成器，具体参考[model生成器](#model生成器)  
`--model_out`，结构输出目录  
`--combine_model`，是否合并结构（需要结构的支持），True为合并  
`--data`，选择一个数据源生成器，具体参考[data生成器](#data生成器)  
`--data_out`，数据源输出目录  
`--combine_data`，是否合并数据源（需要数据源的支持），True为合并。


例生成的C#代码：
```csharp
public class 表名
{
    /// <summary>
    /// 编号
    /// </summary>
    public int Id;
    /// <summary>
    /// 内容
    /// </summary>
    public string Content;
}
```
例生成的Json：
```json
{
    {
        "Id": 1,
        "Content": "内容1"
    },
    {
        "Id": 2,
        "Content": "内容2"
    }
}
```

## 支持的数据类型
当前支持
- int16
- int32
- int64
- float
- double
- bool
- string

## Model生成器
当前支持
- csharp
- cpp
- java
- lua
- go

## Data生成器
当前支持
- json
- sqlite
- xml