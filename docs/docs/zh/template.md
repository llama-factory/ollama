# 模板

Ollama 提供了一个强大的模板引擎，基于 Go 的内置模板引擎来构建大型语言模型的提示。此功能是一个有价值的工具，可帮助你充分利用模型。

## 基本模板结构

一个基本的 Go 模板由三个主要部分组成：

* **布局**：模板的总体结构。
* **变量**：动态数据的占位符，当模板被渲染时将被实际值替换。
* **函数**：可以用于操作模板内容的自定义函数或逻辑。

以下是一个简单的聊天模板示例：

```gotmpl
{{- range .Messages }}
{{ .Role }}: {{ .Content }}
{{- end }}
```

在这个示例中，我们有：

* 一个基本的消息结构（布局）
* 三个变量：`Messages`、`Role` 和 `Content`（变量）
* 一个自定义函数（操作），该函数遍历一个项目数组（`range .Messages`）并显示每个项目

## 为你的模型添加模板

默认情况下，导入到 Ollama 的模型有一个默认模板 `{{ .Prompt }}`，即用户输入会原样发送到 LLM。这对于文本或代码补全模型是合适的，但对于聊天或指令模型则缺乏必要的标记。

在这些模型中省略模板会将正确模板化输入的责任交给用户。添加模板可以让用户轻松地从模型中获得最佳结果。

要在你的模型中添加模板，你需要在 Modelfile 中添加一个 `TEMPLATE` 命令。以下是一个使用 Meta 的 Llama 3 的示例：

```dockerfile
FROM llama3.2

TEMPLATE """{{- if .System }}<|start_header_id|>system<|end_header_id|>

{{ .System }}<|eot_id|>
{{- end }}
{{- range .Messages }}<|start_header_id|>{{ .Role }}<|end_header_id|>

{{ .Content }}<|eot_id|>
{{- end }}<|start_header_id|>assistant<|end_header_id|>

"""
```

## 变量

`System` (字符串): 系统提示

`Prompt` (字符串): 用户提示

`Response` (字符串): 助手响应

`Suffix` (字符串): 插入在助手响应后的文本

`Messages` (列表): 消息列表

`Messages[].Role` (字符串): 角色，可以是 `system`、`user`、`assistant` 或 `tool`

`Messages[].Content` (字符串): 消息内容

`Messages[].ToolCalls` (列表): 模型希望调用的工具列表

`Messages[].ToolCalls[].Function` (对象): 要调用的函数

`Messages[].ToolCalls[].Function.Name` (字符串): 函数名称

`Messages[].ToolCalls[].Function.Arguments` (映射): 参数名称到参数值的映射

`Tools` (列表): 模型可以访问的工具列表

`Tools[].Type` (字符串): 模式类型。`type` 始终为 `function`

`Tools[].Function` (对象): 函数定义

`Tools[].Function.Name` (字符串): 函数名称

`Tools[].Function.Description` (字符串): 函数描述

`Tools[].Function.Parameters` (对象): 函数参数

`Tools[].Function.Parameters.Type` (字符串): 模式类型。`type` 始终为 `object`

`Tools[].Function.Parameters.Required` (列表): 必需属性列表

`Tools[].Function.Parameters.Properties` (映射): 属性名称到属性定义的映射

`Tools[].Function.Parameters.Properties[].Type` (字符串): 属性类型

`Tools[].Function.Parameters.Properties[].Description` (字符串): 属性描述

`Tools[].Function.Parameters.Properties[].Enum` (列表): 有效值列表

## 提示和最佳实践

在使用 Go 模板时，请牢记以下提示和最佳实践：

* **注意点号**: 控制结构如 `range` 和 `with` 会改变 `.` 的值
* **超出范围的变量**: 使用 `$.` 从根开始引用当前不在范围内的变量
* **空白控制**: 使用 `-` 来修剪前导 (`{{-`) 和尾随 (`-}}`) 的空白

## 示例

### 示例消息

#### ChatML

ChatML 是一种流行的模板格式。它可以用于 Databrick's DBRX、Intel's Neural Chat 和 Microsoft's Orca 2 等模型。

```gotmpl
{{- range .Messages }}<|im_start|>{{ .Role }}
{{ .Content }}<|im_end|>
{{ end }}<|im_start|>assistant
```

### 示例工具

可以通过在模板中添加 `{{ .Tools }}` 节点来为模型添加工具支持。此功能对于训练调用外部工具的模型非常有用，可以成为获取实时数据或执行复杂任务的强大工具。

#### Mistral

Mistral v0.3 和 Mixtral 8x22B 支持调用工具。

```gotmpl
{{- range $index, $_ := .Messages }}
{{- if eq .Role "user" }}
{{- if and (le (len (slice $.Messages $index)) 2) $.Tools }}[AVAILABLE_TOOLS] {{ json $.Tools }}[/AVAILABLE_TOOLS]
{{- end }}[INST] {{ if and (eq (len (slice $.Messages $index)) 1) $.System }}{{ $.System }}

{{ end }}{{ .Content }}[/INST]
{{- else if eq .Role "assistant" }}
{{- if .Content }} {{ .Content }}</s>
{{- else if .ToolCalls }}[TOOL_CALLS] [
{{- range .ToolCalls }}{"name": "{{ .Function.Name }}", "arguments": {{ json .Function.Arguments }}}
{{- end }}]</s>
{{- end }}
{{- else if eq .Role "tool" }}[TOOL_RESULTS] {"content": {{ .Content }}}[/TOOL_RESULTS]
{{- end }}
{{- end }}
```

### 示例填空

可以通过在模板中添加一个 `{{ .Suffix }}` 节点来为模型添加填空支持。此功能对于训练生成用户输入中间文本的模型非常有用，例如代码补全模型。

#### CodeLlama

CodeLlama [7B](https://ollama.com/library/codellama:7b-code) 和 [13B](https://ollama.com/library/codellama:13b-code) 代码补全模型支持填空。

```gotmpl
<PRE> {{ .Prompt }} <SUF>{{ .Suffix }} <MID>
```

> [!NOTE]
> CodeLlama 34B 和 70B 代码补全以及所有指令和 Python 微调模型不支持中间填充。

#### Codestral

Codestral [22B](https://ollama.com/library/codestral:22b) 支持中间填充。

```gotmpl
[SUFFIX]{{ .Suffix }}[PREFIX] {{ .Prompt }}
```


