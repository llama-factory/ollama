# 常见问题

## 如何升级 Ollama？

Ollama 在 macOS 和 Windows 上会自动下载更新。点击任务栏或菜单栏图标，然后点击“重启以更新”来应用更新。也可以通过手动下载最新版本[手动](https://ollama.com/download/)来安装更新。

在 Linux 上，重新运行安装脚本：

```shell
curl -fsSL https://ollama.com/install.sh | sh
```

## 如何查看日志？

请参阅 [故障排除](./troubleshooting.md) 文档，了解有关使用日志的更多信息。

## 我的 GPU 是否兼容 Ollama？

请参阅 [GPU 文档](./gpu.md)。

## 如何指定上下文窗口大小？

默认情况下，Ollama 使用 2048 个 token 的上下文窗口大小。

在使用 `ollama run` 时，可以通过 `/set parameter` 来更改此设置：

```
/set parameter num_ctx 4096
```

在使用 API 时，指定 `num_ctx` 参数：

```shell
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Why is the sky blue?",
  "options": {
    "num_ctx": 4096
  }
}'
```

## 如何判断我的模型是否加载到了 GPU？

使用 `ollama ps` 命令查看当前加载到内存中的模型。

```shell
ollama ps
NAME      	ID          	SIZE 	PROCESSOR	UNTIL
llama3:70b	bcfb190ca3a7	42 GB	100% GPU 	4 minutes from now
```

`Processor` 列将显示模型加载到的内存：
* `100% GPU` 表示模型完全加载到 GPU
* `100% CPU` 表示模型完全加载到系统内存
* `48%/52% CPU/GPU` 表示模型部分加载到 GPU 和系统内存

## 如何配置 Ollama 服务器？ {#how-do-i-configure-ollama-server}

Ollama 服务器可以通过环境变量进行配置。

### 在 Mac 上设置环境变量

如果 Ollama 作为 macOS 应用程序运行，应使用 `launchctl` 设置环境变量：

1. 对于每个环境变量，调用 `launchctl setenv`。

    ```bash
    launchctl setenv OLLAMA_HOST "0.0.0.0"
    ```

2. 重启 Ollama 应用程序。

### 在 Linux 上设置环境变量

如果 Ollama 作为 systemd 服务运行，应使用 `systemctl` 设置环境变量：

1. 通过调用 `systemctl edit ollama.service` 编辑 systemd 服务。这将打开一个编辑器。

2. 对于每个环境变量，在 `[Service]` 部分下添加一行 `Environment`：

    ```ini
    [Service]
    Environment="OLLAMA_HOST=0.0.0.0"
    ```

3. 保存并退出。

4. 重新加载 `systemd` 并重启 Ollama：

   ```bash
   systemctl daemon-reload
   systemctl restart ollama
   ```

### 在 Windows 上设置环境变量

在 Windows 上，Ollama 会继承你的用户和系统环境变量。

1. 首先，通过点击任务栏中的 Ollama 图标来退出 Ollama。

2. 启动设置（Windows 11）或控制面板（Windows 10）应用程序，并搜索 _环境变量_。

3. 点击 _编辑账户的环境变量_。

4. 编辑或为你的用户账户创建新的变量，例如 `OLLAMA_HOST`、`OLLAMA_MODELS` 等。

5. 点击确定/应用以保存。

6. 从 Windows 开始菜单启动 Ollama 应用程序。

## 如何在代理后面使用 Ollama？

Ollama 从互联网拉取模型，可能需要通过代理服务器来访问这些模型。使用 `HTTPS_PROXY` 将出站请求重定向到代理。确保代理证书已安装为系统证书。有关如何在你的平台上使用环境变量的详细信息，请参阅上面的章节。

> [!NOTE]
> 避免设置 `HTTP_PROXY`。Ollama 不使用 HTTP 拉取模型，只使用 HTTPS。设置 `HTTP_PROXY` 可能会中断客户端与服务器的连接。

### 如何在 Docker 中使用代理？

可以通过在启动容器时传递 `-e HTTPS_PROXY=https://proxy.example.com` 来配置 Ollama Docker 镜像使用代理。

或者，可以配置 Docker 守护程序使用代理。有关配置 Docker Desktop 的说明，请参阅 [macOS](https://docs.docker.com/desktop/settings/mac/#proxies)、[Windows](https://docs.docker.com/desktop/settings/windows/#proxies) 和 [Linux](https://docs.docker.com/desktop/settings/linux/#proxies) 的文档，以及 Docker [守护程序与 systemd](https://docs.docker.com/config/daemon/systemd/#httphttps-proxy) 的文档。

使用 HTTPS 时，确保证书已安装为系统证书。如果使用自签名证书，可能需要创建新的 Docker 镜像。

```dockerfile
FROM ollama/ollama
COPY my-ca.pem /usr/local/share/ca-certificates/my-ca.crt
RUN update-ca-certificates
```

构建并运行此镜像：

```shell
docker build -t ollama-with-ca .
docker run -d -e HTTPS_PROXY=https://my.proxy.example.com -p 11434:11434 ollama-with-ca
```

## Ollama 是否会将我的提示和回答发送回 ollama.com？

不会。Ollama 在本地运行，对话数据不会离开你的机器。

## 如何在我的网络上暴露 Ollama？

Ollama 默认绑定 127.0.0.1 端口 11434。你可以通过设置 `OLLAMA_HOST` 环境变量来更改绑定地址。

请参阅上方的 [如何配置 Ollama 服务器](#how-do-i-configure-ollama-server) 部分，了解如何在你的平台上设置环境变量。

## 如何使用代理服务器与 Ollama 一起工作？

Ollama 运行一个 HTTP 服务器，可以使用如 Nginx 这样的代理服务器来暴露。为此，配置代理以转发请求，并可选地设置所需的标头（如果不在网络上暴露 Ollama）。例如，使用 Nginx：

```
server {
    listen 80;
    server_name example.com;  # Replace with your domain or IP
    location / {
        proxy_pass http://localhost:11434;
        proxy_set_header Host localhost:11434;
    }
}
```

## 如何使用 Ollama 与 ngrok？

Ollama 可以通过多种隧道工具访问。例如，使用 Ngrok：

```shell
ngrok http 11434 --host-header="localhost:11434"
```

## 如何使用 Ollama 与 Cloudflare Tunnel？

要使用 Ollama 与 Cloudflare Tunnel，使用 `--url` 和 `--http-host-header` 标志：

```shell
cloudflared tunnel --url http://localhost:11434 --http-host-header="localhost:11434"
```

## 如何允许其他 Web 源访问 Ollama？

Ollama 默认允许来自 `127.0.0.1` 和 `0.0.0.0` 的跨源请求。可以通过设置 `OLLAMA_ORIGINS` 来配置其他源。

请参阅上方的 [如何配置 Ollama 服务器](#how-do-i-configure-ollama-server) 部分，了解如何在你的平台上设置环境变量。

## 模型存储在哪里？

- macOS: `~/.ollama/models`
- Linux: `/usr/share/ollama/.ollama/models`
- Windows: `C:\Users\%username%\.ollama\models`

### 如何将它们设置为不同的位置？

如果需要使用不同的目录，可以将环境变量 `OLLAMA_MODELS` 设置为你选择的目录。

> 注意：在 Linux 上使用标准安装程序时，`ollama` 用户需要对指定目录有读写权限。要将目录分配给 `ollama` 用户，请运行 `sudo chown -R ollama:ollama <directory>`.

请参考[上面的部分](#how-do-i-configure-ollama-server)了解如何在你的平台上设置环境变量。

## 如何在 Visual Studio Code 中使用 Ollama？

已经有大量适用于 VSCode 和其他编辑器的插件可供使用，这些插件利用了 Ollama。请参阅主仓库自述文件底部的[扩展和插件](https://github.com/ollama/ollama#extensions--plugins)列表。

## 如何在 Docker 中使用 Ollama 进行 GPU 加速？

Ollama Docker 容器可以在 Linux 或 Windows（使用 WSL2）中配置 GPU 加速。这需要[nvidia-container-toolkit](https://github.com/NVIDIA/nvidia-container-toolkit)。更多详情请参阅[ollama/ollama](https://hub.docker.com/r/ollama/ollama)。

由于缺乏 GPU 透传和模拟，Docker Desktop 在 macOS 上不支持 GPU 加速。

## 为什么在 Windows 10 上的 WSL2 中网络速度较慢？

这会影响安装 Ollama 以及下载模型。

打开 `控制面板 > 网络和 Internet > 查看网络状态和任务`，然后点击左侧的 `更改适配器设置`。找到 `vEthernel (WSL)` 适配器，右键点击并选择 `属性`。点击 `配置` 并打开 `高级` 选项卡。浏览每个属性，直到找到 `大型发送卸载版本 2 (IPv4)` 和 `大型发送卸载版本 2 (IPv6)`。*禁用*这两个属性。

## 如何预加载模型到 Ollama 以获得更快的响应时间？

如果你使用的是 API，可以通过向 Ollama 服务器发送一个空请求来预加载模型。这适用于 `/api/generate` 和 `/api/chat` API 端点。

要使用生成端点预加载 mistral 模型，请使用：

```shell
curl http://localhost:11434/api/generate -d '{"model": "mistral"}'
```

要使用聊天补全端点，请使用：

```shell
curl http://localhost:11434/api/chat -d '{"model": "mistral"}'
```

要使用 CLI 预加载模型，请使用以下命令：

```shell
ollama run llama3.2 ""
```

## 如何保持模型在内存中加载或立即卸载？

默认情况下，模型会在内存中保留 5 分钟后才被卸载。这允许在你向 LLM 发送多个请求时获得更快的响应时间。如果你希望立即从内存中卸载模型，可以使用 `ollama stop` 命令：

```shell
ollama stop llama3.2
```

如果你正在使用 API，可以使用 `keep_alive` 参数与 `/api/generate` 和 `/api/chat` 端点来设置模型在内存中保持的时间。`keep_alive` 参数可以设置为：
* 一个持续时间字符串（例如 "10m" 或 "24h"）
* 以秒为单位的数字（例如 3600）
* 任何负数，这将使模型保持在内存中（例如 -1 或 "-1m"）
* '0'，这将在生成响应后立即卸载模型

例如，要预加载模型并将其保留在内存中，可以使用：

```shell
curl http://localhost:11434/api/generate -d '{"model": "llama3.2", "keep_alive": -1}'
```

要卸载模型并释放内存，请使用：

```shell
curl http://localhost:11434/api/generate -d '{"model": "llama3.2", "keep_alive": 0}'
```

或者，你可以在启动 Ollama 服务器时通过设置 `OLLAMA_KEEP_ALIVE` 环境变量来更改所有模型加载到内存中的时间。`OLLAMA_KEEP_ALIVE` 变量使用与上述 `keep_alive` 参数类型相同的参数类型。请参阅 [如何配置 Ollama 服务器](#how-do-i-configure-ollama-server) 部分，以正确设置环境变量。

`keep_alive` API 参数在 `/api/generate` 和 `/api/chat` API 端点中将覆盖 `OLLAMA_KEEP_ALIVE` 设置。

## 如何管理 Ollama 服务器可以排队的最大请求数？

如果发送到服务器的请求数过多，服务器将返回 503 错误，表示服务器过载。你可以通过设置 `OLLAMA_MAX_QUEUE` 来调整可以排队的请求数。

## Ollama 如何处理并发请求？

Ollama 支持两个级别的并发处理。如果你的系统有足够的可用内存（使用 CPU 推理时为系统内存，使用 GPU 推理时为 VRAM），则可以同时加载多个模型。对于给定的模型，如果在加载模型时有足够的可用内存，它将被配置为允许并行请求处理。

如果在加载新模型请求时，已有一个或多个模型已加载且可用内存不足，所有新请求将被排队，直到新模型可以加载。当先前的模型空闲时，一个或多个将被卸载以腾出空间加载新模型。排队的请求将按顺序处理。使用 GPU 推理时，新模型必须能够完全适应 VRAM 才能允许并发模型加载。

对于给定模型的并行请求处理将通过并行请求的数量增加上下文大小。例如，2K 上下文与 4 个并行请求将导致 8K 上下文和额外的内存分配。

以下服务器设置可用于调整 Ollama 在大多数平台上处理并发请求的方式：

- `OLLAMA_MAX_LOADED_MODELS` - 可以同时加载的最大模型数量，前提是它们适合可用内存。默认值为 GPU 数量的 3 倍，或对于 CPU 推理为 3。
- `OLLAMA_NUM_PARALLEL` - 每个模型同时处理的最大并行请求数。默认值将根据可用内存自动选择 4 或 1。
- `OLLAMA_MAX_QUEUE` - Ollama 在拒绝额外请求之前可以排队的最大请求数。默认值为 512。

注意：由于 ROCm v5.7 在可用 VRAM 报告方面的限制，Windows 上使用 Radeon GPU 当前默认为最大 1 个模型。一旦 ROCm v6.2 可用，Windows Radeon 将遵循上述默认值。你可以在 Windows 上启用 Radeon 的并发模型加载，但请确保加载的模型数量不超过 GPU 的 VRAM 容量。

## Ollama 如何在多个 GPU 上加载模型？

安装多个相同品牌的 GPU 是增加可用 VRAM 以加载更大模型的好方法。当你加载新模型时，Ollama 会评估模型所需的 VRAM 与当前可用的 VRAM。如果模型可以完全适应任何一个 GPU，Ollama 将在该 GPU 上加载模型。这通常可以提供最佳性能，因为它减少了推理过程中通过 PCI 总线传输的数据量。如果模型不能完全适应一个 GPU，它将分布在所有可用的 GPU 上。