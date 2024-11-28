# Ollama Windows

欢迎使用 Ollama for Windows。

不再需要 WSL！

Ollama 现在作为原生 Windows 应用程序运行，支持 NVIDIA 和 AMD Radeon GPU。
安装 Ollama for Windows 后，Ollama 将在后台运行，
`ollama` 命令行工具将在 `cmd`、`powershell` 或你最喜欢的终端应用程序中可用。和往常一样，Ollama [API](./api.md) 将在 `http://localhost:11434` 上提供服务。

## 系统要求

* Windows 10 22H2 或更新版本，家庭版或专业版
* 如果你有 NVIDIA 显卡，需要安装 452.39 或更新版本的驱动程序
* 如果你有 Radeon 显卡，需要安装 AMD Radeon 驱动程序 https://www.amd.com/en/support

Ollama 使用 Unicode 字符来显示进度，这在 Windows 10 的一些旧终端字体中可能会显示为未知方块。如果你看到这种情况，尝试更改终端字体设置。

## 文件系统要求

Ollama 安装不需要管理员权限，默认安装在你的用户目录中。你需要至少 4GB 的空间来安装二进制文件。安装 Ollama 后，你还需要额外的空间来存储大型语言模型，这些模型的大小可能从几十 GB 到几百 GB 不等。如果你的用户目录没有足够的空间，你可以更改二进制文件的安装位置和模型的存储位置。

### 更改安装位置

要将 Ollama 应用程序安装在不同于用户目录的位置，请使用以下标志启动安装程序：

```powershell
OllamaSetup.exe /DIR="d:\some\location"
```

### 更改模型存储位置

要更改 Ollama 存储下载模型的位置，而不是使用你的主目录，可以在你的用户账户中设置环境变量 `OLLAMA_MODELS`。

1. 启动设置（Windows 11）或控制面板（Windows 10）应用程序，并搜索 _环境变量_。

2. 点击 _编辑账户环境变量_。

3. 编辑或创建一个新的用户账户变量 `OLLAMA_MODELS`，设置为你希望存储模型的路径。

4. 点击确定/应用以保存。

如果 Ollama 已经在运行，请退出系统托盘中的应用程序，然后从开始菜单或在保存环境变量后启动的新终端中重新启动它。

## API 访问

以下是一个从 `powershell` 访问 API 的快速示例：

```powershell
(Invoke-WebRequest -method POST -Body '{"model":"llama3.2", "prompt":"Why is the sky blue?", "stream": false}' -uri http://localhost:11434/api/generate ).Content | ConvertFrom-json
```

## 故障排除

Ollama 在 Windows 上将文件存储在几个不同的位置。你可以在资源管理器窗口中通过按下 `<cmd>+R` 并输入以下内容来查看：
- `explorer %LOCALAPPDATA%\Ollama` 包含日志和下载的更新
    - *app.log* 包含 GUI 应用程序的最新日志
    - *server.log* 包含服务器的最新日志
    - *upgrade.log* 包含升级的日志输出
- `explorer %LOCALAPPDATA%\Programs\Ollama` 包含二进制文件（安装程序会将其添加到你的用户 PATH 中）
- `explorer %HOMEPATH%\.ollama` 包含模型和配置
- `explorer %TEMP%` 包含临时可执行文件，位于一个或多个 `ollama*` 目录中

## 卸载

Ollama Windows 安装程序注册了一个卸载应用程序。在 Windows 设置中的 `添加或删除程序` 下，你可以卸载 Ollama。

> [!NOTE]
> 如果你已经[更改了 OLLAMA_MODELS 位置](#changing-model-location)，安装程序不会移除你下载的模型

## 独立 CLI

在 Windows 上安装 Ollama 最简单的方法是使用 `OllamaSetup.exe` 安装程序。它会在你的账户中安装，无需管理员权限。我们定期更新 Ollama 以支持最新的模型，这个安装程序将帮助你保持更新。

如果你希望将 Ollama 作为服务安装或集成，可以使用独立的 `ollama-windows-amd64.zip` 压缩文件，其中仅包含 Ollama CLI 和 Nvidia 及 AMD 的 GPU 库依赖项。这允许你将 Ollama 嵌入现有应用程序中，或通过 `ollama serve` 等工具将其作为系统服务运行，例如使用 [NSSM](https://nssm.cc/)。