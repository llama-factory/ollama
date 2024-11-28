# 开发

安装所需工具：

- go 版本 1.22 或更高
- gcc 版本 11.4.0 或更高


### MacOS

[下载 Go](https://go.dev/dl/)

可选地启用调试和更详细的日志记录：

```bash
# At build time
export CGO_CFLAGS="-g"

# At runtime
export OLLAMA_DEBUG=1
```

获取所需的库并构建原生 LLM 代码：（根据你的处理器数量调整作业数以加快构建速度）

```bash
make -j 5
```

然后构建 ollama:

```bash
go build .
```

现在你可以运行 `ollama`：

```bash
./ollama
```

#### Xcode 15 警告

如果你使用的是 Xcode 14 之后的版本，在执行 `go build` 时可能会看到关于 `ld: warning: ignoring duplicate libraries: '-lobjc'` 的警告。这是由于 Golang 问题 https://github.com/golang/go/issues/67799 ，可以安全地忽略。你可以通过 `export CGO_LDFLAGS="-Wl,-no_warn_duplicate_libraries"` 来抑制该警告。

### Linux

#### Linux CUDA (NVIDIA)

_你的操作系统发行版可能已经包含了 NVIDIA CUDA 的包。发行版的包通常是首选，但具体指令因发行版而异。如果有可用的发行版特定文档，请查阅以获取依赖项信息！_

安装 `make`、`gcc` 和 `golang` 以及 [NVIDIA CUDA](https://developer.nvidia.com/cuda-downloads) 开发和运行时包。

通常构建脚本会自动检测 CUDA，但是如果你的 Linux 发行版或安装方法使用了非标准路径，可以通过设置环境变量 `CUDA_LIB_DIR` 指定共享库的位置，以及 `CUDACXX` 指定 nvcc 编译器的位置。你还可以通过设置 `CMAKE_CUDA_ARCHITECTURES`（例如 "50;60;70"）来定制一组目标 CUDA 架构。

然后生成依赖项：（根据你的处理器数量调整作业数以加快构建速度）

```
make -j 5
```

然后构建二进制文件：

```
go build .
```

#### Linux ROCm (AMD)

_你的操作系统发行版可能已经包含了 AMD ROCm 和 CLBlast 的软件包。发行版的软件包通常是首选，但安装步骤因发行版而异。如果有可用的发行版特定文档，请查阅以获取依赖项信息！_

首先安装 [CLBlast](https://github.com/CNugteren/CLBlast/blob/master/doc/installation.md) 和 [ROCm](https://rocm.docs.amd.com/en/latest/) 开发包，以及 `make`、`gcc` 和 `golang`。

通常构建脚本会自动检测 ROCm，但是如果你的 Linux 发行版或安装方法使用了非标准路径，可以通过设置环境变量 `ROCM_PATH` 指定 ROCm 安装位置（通常是 `/opt/rocm`），并通过 `CLBlast_DIR` 指定 CLBlast 安装位置（通常是 `/usr/lib/cmake/CLBlast`）。你还可以通过设置 `AMDGPU_TARGETS` 来自定义 AMD GPU 目标（例如 `AMDGPU_TARGETS="gfx1101;gfx1102"`）。

然后生成依赖项：（根据你的处理器数量调整作业数以加快构建速度）

```
make -j 5
```

然后构建二进制文件：

```
go build .
```

ROCm 需要提升的权限才能在运行时访问 GPU。在大多数发行版中，你可以将用户帐户添加到 `render` 组，或者以 root 用户身份运行。

#### 高级 CPU 设置

默认情况下，运行 `make` 将基于常见的 CPU 家族和向量数学能力编译 LLM 库的几个不同变体，包括一个最低公分母版本，该版本应该可以在几乎任何 64 位 CPU 上运行，但速度较慢。在运行时，Ollama 会自动检测并加载最优的变体。

目前，新的 Go 服务器构建不支持自定义 CPU 设置，但将在我们完成过渡后重新添加。

#### 容器化 Linux 构建

如果你有 Docker 可用，可以使用 `./scripts/build_linux.sh` 构建包含 CUDA 和 ROCm 依赖项的 Linux 二进制文件。生成的二进制文件将放置在 `./dist` 目录中。

### Windows

以下工具是构建 CPU 推理支持所需的最小开发环境。

- Go 1.22 或更高版本
  - https://go.dev/dl/
- Git
  - https://git-scm.com/download/win
- 具有 gcc 兼容性的 clang 和 Make。在 Windows 上安装这些工具有多种选择。我们已验证以下方法，但其他方法也可能有效：
  - [MSYS2](https://www.msys2.org/)
    - 安装后，从 MSYS2 终端运行 `pacman -S mingw-w64-clang-x86_64-gcc-compat mingw-w64-clang-x86_64-clang make` 以安装所需的工具
  - 假设你使用了上述默认安装前缀，将 `C:\msys64\clang64\bin` 和 `c:\msys64\usr\bin` 添加到你将执行以下构建步骤的环境变量 `PATH` 中（例如，系统级、帐户级、PowerShell、cmd 等）。

> [!NOTE]  
> 由于 GCC C++ 库在 Unicode 支持方面存在 bug，Ollama 应在 Windows 上使用 clang 构建。

然后，构建 `ollama` 二进制文件：

```powershell
$env:CGO_ENABLED="1"
make -j 8
go build .
```

#### GPU 支持

GPU 工具需要 Microsoft 本机构建工具。要构建 CUDA 或 ROCm，你必须首先通过 Visual Studio 安装 MSVC：

- 在 Visual Studio 安装过程中，确保选择 `使用 C++ 的桌面开发` 作为工作负载
- 你必须完成 Visual Studio 的安装并运行一次 **在安装 CUDA 或 ROCm 之前**，以确保工具正确注册
- 将 **64 位 (x64)** 编译器 (`cl.exe`) 的位置添加到你的 `PATH`
- 注意：默认的开发 shell 可能会配置 32 位 (x86) 编译器，这将导致构建失败。Ollama 需要一个 64 位工具链。

#### Windows CUDA (NVIDIA)

除了上述的通用 Windows 开发工具和 MSVC：

- [NVIDIA CUDA](https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/index.html)

#### Windows ROCm (AMD Radeon)

除了上述的通用 Windows 开发工具和 MSVC：

- [AMD HIP](https://www.amd.com/en/developer/resources/rocm-hub/hip-sdk.html)

#### Windows arm64

默认的 `Developer PowerShell for VS 2022` 可能会默认使用 x86，这不是你想要的。为了确保你获得一个 arm64 开发环境，请启动一个普通的 PowerShell 终端并运行：

```powershell
import-module 'C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\Common7\\Tools\\Microsoft.VisualStudio.DevShell.dll'
Enter-VsDevShell -Arch arm64 -vsinstallpath 'C:\\Program Files\\Microsoft Visual Studio\\2022\\Community' -skipautomaticlocation
```

你可以通过 `write-host $env:VSCMD_ARG_TGT_ARCH` 来确认。

按照 https://www.msys2.org/wiki/arm64/ 的说明设置 arm64 msys2 环境。Ollama 需要 gcc 和 mingw32-make 来编译，但目前 Windows arm64 上没有提供这些工具，不过可以通过 `mingw-w64-clang-aarch64-gcc-compat` 获取一个 gcc 兼容适配器。至少你需要安装以下内容：

```
pacman -S mingw-w64-clang-aarch64-clang mingw-w64-clang-aarch64-gcc-compat mingw-w64-clang-aarch64-make make
```

你需要确保你的 PATH 包含 go、cmake、gcc 和 clang mingw32-make 以从源代码构建 ollama。（通常为 `C:\msys64\clangarm64\bin\`）