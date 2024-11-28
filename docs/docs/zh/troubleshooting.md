# 如何排查问题

有时 Ollama 可能无法按预期工作。找出问题的最佳方法之一是查看日志。在 **Mac** 上，可以通过运行以下命令找到日志：

```shell
cat ~/.ollama/logs/server.log
```

在 **Linux** 系统中使用 systemd 时，可以使用以下命令查找日志：

```shell
journalctl -u ollama --no-pager
```

当你在 **容器** 中运行 Ollama 时，日志会输出到容器的 stdout/stderr：

```shell
docker logs <container-name>
```

(使用 `docker ps` 查找容器名称)

如果在终端手动运行 `ollama serve`，日志将显示在该终端上。

当你在 **Windows** 上运行 Ollama 时，日志可能位于几个不同的位置。你可以在资源管理器窗口中通过按下 `<cmd>+R` 并输入以下内容来查看：
- `explorer %LOCALAPPDATA%\Ollama` 以查看日志。最新的服务器日志将在 `server.log` 中，旧日志将在 `server-#.log` 中
- `explorer %LOCALAPPDATA%\Programs\Ollama` 以浏览二进制文件（安装程序会将其添加到你的用户 PATH 中）
- `explorer %HOMEPATH%\.ollama` 以浏览模型和配置的存储位置
- `explorer %TEMP%` 其中临时可执行文件存储在一个或多个 `ollama*` 目录中

要启用额外的调试日志以帮助解决问题，首先从托盘菜单中**退出正在运行的应用程序**，然后在 PowerShell 终端中

```powershell
$env:OLLAMA_DEBUG="1"
& "ollama app.exe"
```

加入 [Discord](https://discord.gg/ollama) 以获取帮助解读日志。

## LLM 库

Ollama 包含多个为不同 GPU 和 CPU 向量特性编译的 LLM 库。Ollama 会根据你的系统功能选择最佳的库。如果自动检测出现问题，或者你遇到其他问题（例如 GPU 崩溃），你可以通过强制使用特定的 LLM 库来解决这些问题。`cpu_avx2` 的性能最佳，其次是 `cpu_avx`，最慢但最兼容的是 `cpu`。在 MacOS 下使用 Rosetta 模拟时，`cpu` 库可以正常工作。

在服务器日志中，你会看到类似以下的消息（具体消息可能因版本而异）：

```
Dynamic LLM libraries [rocm_v6 cpu cpu_avx cpu_avx2 cuda_v11 rocm_v5]
```

**实验性 LLM 库覆盖**

你可以将 OLLAMA_LLM_LIBRARY 设置为任何可用的 LLM 库以绕过自动检测，例如，如果你有一张 CUDA 卡，但想强制使用带有 AVX2 向量支持的 CPU LLM 库，可以使用：

```
OLLAMA_LLM_LIBRARY="cpu_avx2" ollama serve
```

你可以通过以下方法查看你的 CPU 具有哪些特性。

```
cat /proc/cpuinfo| grep flags | head -1
```

## 在 Linux 上安装旧版本或预发布版本

如果你在 Linux 上遇到问题并希望安装旧版本，或者想在正式发布前尝试预发布版本，你可以告诉安装脚本要安装哪个版本。

```sh
curl -fsSL https://ollama.com/install.sh | OLLAMA_VERSION="0.1.29" sh
```

## Linux tmp noexec

如果你的系统配置了 "noexec" 标志，而 Ollama 存储其临时可执行文件的位置正是该位置，你可以通过设置 OLLAMA_TMPDIR 指定一个用户可写的替代位置。例如 OLLAMA_TMPDIR=/usr/share/ollama/

## NVIDIA GPU Discovery

当 Ollama 启动时，它会检查系统中可用的 GPU 以确定兼容性和可用的 VRAM。有时这个发现过程可能会失败，无法找到你的 GPU。通常，运行最新驱动程序会获得最佳结果。

### Linux NVIDIA 故障排除

如果你使用容器运行 Ollama，请确保你已按照 [docker.md](./docker.md) 中的描述设置好容器运行时。

有时 Ollama 在初始化 GPU 时可能会遇到困难。当你检查服务器日志时，这可能会显示各种错误代码，例如 "3"（未初始化）、"46"（设备不可用）、"100"（无设备）、"999"（未知）或其他错误代码。以下故障排除技术可能有助于解决问题：

- 如果你使用的是容器，容器运行时是否正常工作？尝试 `docker run --gpus all ubuntu nvidia-smi` - 如果这不起作用，Ollama 将无法看到你的 NVIDIA GPU。
- uvm 驱动是否已加载？`sudo nvidia-modprobe -u`
- 尝试重新加载 nvidia_uvm 驱动 - `sudo rmmod nvidia_uvm` 然后 `sudo modprobe nvidia_uvm`
- 尝试重启
- 确保你正在运行最新的 NVIDIA 驱动程序

如果以上方法都无法解决问题，请收集更多信息并提交问题：
- 设置 `CUDA_ERROR_LEVEL=50` 并再次尝试以获取更多诊断日志


- Check dmesg for any errors `sudo dmesg | grep -i nvrm` and `sudo dmesg | grep -i nvidia`




## AMD GPU Discovery

在 Linux 上，访问 AMD GPU 通常需要 `video` 和/或 `render` 组的成员身份来访问 `/dev/kfd` 设备。如果权限设置不正确，Ollama 会检测到这一点并在服务器日志中报告错误。

在容器中运行时，在某些 Linux 发行版和容器运行时中，ollama 进程可能无法访问 GPU。使用 `ls -lnd /dev/kfd /dev/dri /dev/dri/*` 命令在主机系统上确定 **数字** 组 ID，然后将额外的 `--group-add ...` 参数传递给容器，以便它可以访问所需的设备。例如，在以下输出 `crw-rw---- 1 0  44 226,   0 Sep 16 16:55 /dev/dri/card0` 中，组 ID 列为 `44`。

如果 Ollama 最初在 Docker 容器中使用 GPU 运行，但一段时间后切换到使用 CPU 运行，并且服务器日志中报告 GPU 发现失败的错误，可以通过禁用 Docker 中的 systemd cgroup 管理来解决。在主机上编辑 `/etc/docker/daemon.json` 并添加 `"exec-opts": ["native.cgroupdriver=cgroupfs"]` 到 Docker 配置中。

如果你在让 Ollama 正确发现或使用 GPU 进行推理时遇到问题，以下方法可能有助于隔离故障：
- `AMD_LOG_LEVEL=3` 在 AMD HIP/ROCm 库中启用信息日志级别。这可以帮助显示更详细的错误代码，从而有助于故障排除。
- `OLLAMA_DEBUG=1` 在 GPU 发现过程中会报告更多详细信息。


- Check dmesg for any errors from amdgpu or kfd drivers `sudo dmesg | grep -i amdgpu` and `sudo dmesg | grep -i kfd`



## 多个 AMD GPU

如果你在 Linux 上使用多个 AMD GPU 加载模型时遇到乱码响应，请参阅以下指南。

- https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/native_linux/mgpu.html#mgpu-known-issues-and-limitations

## Windows 终端错误

较旧版本的 Windows 10（例如 21H1）已知存在一个 bug，标准终端程序无法正确显示控制字符。这可能导致显示一长串类似 `←[?25h←[?25l` 的字符串，有时会报错 `The parameter is incorrect`。要解决此问题，请更新到 Win 10 22H1 或更高版本。