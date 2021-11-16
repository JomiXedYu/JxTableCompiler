# JxTableCompiler
使用Excel表格，生成编程语言数据结构，生成数据源。

## 如何使用
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
第一个参数file为必选，需要传入xlsx后缀的文件，或者用换行分割储存xlsx文件列表的txt文件。  
可选参数：  
`--model`，选择一个结构生成器，具体参考[model生成器](#model生成器)。  
`--model_out`，结构输出目录，使用`--model`时必选。  
`--combine_model`，是否合并结构（需要结构的支持），True为合并。  
`--data`，选择一个数据源生成器，具体参考[data生成器](#data生成器)  
`--data_out`，数据源输出目录，使用`--data`时必选。  
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


## 快速脚本
为了方便的使用该程序，提供windows批处理脚本`compile.bat`：  
> 如下载的是Release中的可执行文件版本，则在压缩包内寻找。  

目录结构：  
```
ProjectRoot:
  |-DataTable
    |-JxTableCompiler
      |-Main.py
      |-...
    |-compile.bat
    |-a.xlsx
    |-b.xlsx
    |-....xlsx
```
可以手动设置的参数在USER VARIABLE中：
- ProjectRoot 项目根目录
- JxTableCompilerPath 本程序所在目录
- JxTableCompilerFilename 本程序名（有可能是py或者为打包的可执行程序）
- DataTableOutFolder 数据表输出文件夹
- ModelOutFolder 结构输出文件夹
- ModelGenerator 结构生成器
- DataCompiler 数据生成器
```bat
@echo off
set AppPath=%~dp0
cd /d %~dp0
cd ..

::=====USER VARIABLE=====
set ProjectRoot=%cd%
set JxTableCompilerPath=%AppPath%\JxTableCompiler
set JxTableCompilerFilename=Main.py
set DataTableOutFolder=%ProjectRoot%\Assets\Resources\DataTable
set ModelOutFolder=%ProjectRoot%\Assets\Scripts\DataTable
set ModelGenerator=csharp
set DataCompiler=json
::=======================

set JxTableCompilerExec=%JxTableCompilerPath%\%JxTableCompilerFilename%

echo -----------config-----------
echo JxTableCompilerExec = %JxTableCompilerExec%
echo DataTableOutFolder = %DataTableOutFolder%
echo ModelOutFolder = %ModelOutFolder%
echo ModelGenerator = %ModelGenerator%
echo DataCompiler = %DataCompiler%
echo ----------------------------

echo build_list...

cd /d %AppPath%

set listname=%AppPath%_table_list.txt

echo outlist: %listname%

echo. > %listname%
for /f "delims=" %%i in ('"dir /a/s/b/on *.xlsx"') do (
    echo %%i >> %listname%
)

echo build list complete.

title JxTableCompiler

cd /d %JxTableCompilerPath%
%JxTableCompilerExec% %listname% --model %ModelGenerator% --model_out %ModelOutFolder% --combine_model True --data %DataCompiler% --data_out %DataTableOutFolder%

echo compile complete.

pause
```

## 第三方
- openpyxl