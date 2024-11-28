<div align="center">
 <img alt="ollama" height="200px" src="https://github.com/ollama/ollama/assets/3325447/0d0b44e2-8f4a-4e99-9b52-a5c1c741c8f7">
</div>


# Ollama

[![Discord](https://dcbadge.vercel.app/api/server/ollama?style=flat&compact=true)](https://discord.gg/ollama)

快速上手大型语言模型。

### macOS

[下载](https://ollama.com/download/Ollama-darwin.zip)

### Windows

[下载](https://ollama.com/download/OllamaSetup.exe)

### Linux

```
curl -fsSL https://ollama.com/install.sh | sh
```

[手动安装说明](https://github.com/ollama/ollama/blob/main/docs/linux.md)

### Docker

官方 [Ollama Docker 镜像](https://hub.docker.com/r/ollama/ollama) `ollama/ollama` 可在 Docker Hub 上获取。

### 库

- [ollama-python](https://github.com/ollama/ollama-python)
- [ollama-js](https://github.com/ollama/ollama-js)

## 快速入门

要运行并与 [Llama 3.2](https://ollama.com/library/llama3.2) 聊天：

```
ollama run llama3.2
```

## 模型库

Ollama 支持在 [ollama.com/library](https://ollama.com/library 'ollama 模型库') 上提供的模型列表。

以下是一些可以下载的示例模型：


| Model              | Parameters | Size  | Download                         |
| ------------------ | ---------- | ----- | -------------------------------- |
| Llama 3.2          | 3B         | 2.0GB | `ollama run llama3.2`            |
| Llama 3.2          | 1B         | 1.3GB | `ollama run llama3.2:1b`         |
| Llama 3.2 Vision   | 11B        | 7.9GB | `ollama run llama3.2-vision`     |
| Llama 3.2 Vision   | 90B        | 55GB  | `ollama run llama3.2-vision:90b` |
| Llama 3.1          | 8B         | 4.7GB | `ollama run llama3.1`            |
| Llama 3.1          | 70B        | 40GB  | `ollama run llama3.1:70b`        |
| Llama 3.1          | 405B       | 231GB | `ollama run llama3.1:405b`       |
| Phi 3 Mini         | 3.8B       | 2.3GB | `ollama run phi3`                |
| Phi 3 Medium       | 14B        | 7.9GB | `ollama run phi3:medium`         |
| Gemma 2            | 2B         | 1.6GB | `ollama run gemma2:2b`           |
| Gemma 2            | 9B         | 5.5GB | `ollama run gemma2`              |
| Gemma 2            | 27B        | 16GB  | `ollama run gemma2:27b`          |
| Mistral            | 7B         | 4.1GB | `ollama run mistral`             |
| Moondream 2        | 1.4B       | 829MB | `ollama run moondream`           |
| Neural Chat        | 7B         | 4.1GB | `ollama run neural-chat`         |
| Starling           | 7B         | 4.1GB | `ollama run starling-lm`         |
| Code Llama         | 7B         | 3.8GB | `ollama run codellama`           |
| Llama 2 Uncensored | 7B         | 3.8GB | `ollama run llama2-uncensored`   |
| LLaVA              | 7B         | 4.5GB | `ollama run llava`               |
| Solar              | 10.7B      | 6.1GB | `ollama run solar`               |


> [!NOTE]
> 你应该至少有 8 GB 的 RAM 来运行 7B 模型，16 GB 的 RAM 来运行 13B 模型，以及 32 GB 的 RAM 来运行 33B 模型。

## 自定义模型

### 从 GGUF 导入

Ollama 支持在 Modelfile 中导入 GGUF 模型：

1. 创建一个名为 `Modelfile` 的文件，并在其中包含一个 `FROM` 指令，该指令指向你想要导入的模型的本地文件路径。

   ```
   FROM ./vicuna-33b.Q4_0.gguf
   ```

2. 在 Ollama 中创建模型

   ```
   ollama create example -f Modelfile
   ```

3. 运行模型

   ```
   ollama run example
   ```

### 从 PyTorch 或 Safetensors 导入

有关导入模型的更多信息，请参阅[指南](./import.md)。

### 自定义提示

来自 Ollama 库的模型可以通过提示进行自定义。例如，要自定义 `llama3.2` 模型：

```
ollama pull llama3.2
```

创建一个 `Modelfile`：

```
FROM llama3.2

# set the temperature to 1 [higher is more creative, lower is more coherent]
PARAMETER temperature 1

# set the system message
SYSTEM """
You are Mario from Super Mario Bros. Answer as Mario, the assistant, only.
"""
```

接下来，创建并运行模型：

```
ollama create mario -f ./Modelfile
ollama run mario
>>> hi
Hello! It's your friend Mario.
```

对于更多示例，请参阅 [examples](examples) 目录。有关如何使用 Modelfile 的更多信息，请参阅 [Modelfile](./modelfile.md) 文档。

## 命令行参考

### 创建模型

`ollama create` 用于从 Modelfile 创建模型。

```
ollama create mymodel -f ./Modelfile
```

### 拉取模型

```
ollama pull llama3.2
```

> 此命令也可以用于更新本地模型。只有差异部分会被拉取。

### 删除模型

```
ollama rm llama3.2
```

### 复制模型

```
ollama cp llama3.2 my-model
```

### 多行输入

对于多行输入，你可以用 `"""` 包裹文本：

```
>>> """Hello,
... world!
... """
I'm a basic program that prints the famous "Hello, world!" message to the console.
```

### 多模态模型

```
ollama run llava "What's in this image? /Users/jmorgan/Desktop/smile.png"
The image features a yellow smiley face, which is likely the central focus of the picture.
```

### 将提示作为参数传递

```
$ ollama run llama3.2 "Summarize this file: $(cat README.md)"
 Ollama is a lightweight, extensible framework for building and running language models on the local machine. It provides a simple API for creating, running, and managing models, as well as a library of pre-built models that can be easily used in a variety of applications.
```

### 显示模型信息

```
ollama show llama3.2
```

### 列出你计算机上的模型

```
ollama list
```

### 列出当前已加载的模型

```
ollama ps
```

### 停止当前正在运行的模型

```
ollama stop llama3.2
```

### 启动 Ollama

`ollama serve` 用于在不运行桌面应用程序的情况下启动 Ollama。

## 构建

参见 [开发者指南](https://github.com/ollama/ollama/blob/main/docs/development.md)

### 运行本地构建

接下来，启动服务器：

```
./ollama serve
```

最后，在单独的 shell 中运行模型：

```
./ollama run llama3.2
```

## REST API

Ollama 拥有一个用于运行和管理模型的 REST API。

### 生成响应

```
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt":"Why is the sky blue?"
}'
```

### 与模型聊天

```
curl http://localhost:11434/api/chat -d '{
  "model": "llama3.2",
  "messages": [
    { "role": "user", "content": "why is the sky blue?" }
  ]
}'
```

请参阅 [API 文档](././api.md) 以获取所有端点的信息。

## 社区集成

### Web 与桌面端

- [Open WebUI](https://github.com/open-webui/open-webui)
- [Enchanted (macOS 原生)](https://github.com/AugustDev/enchanted)
- [Hollama](https://github.com/fmaclen/hollama)
- [Lollms-Webui](https://github.com/ParisNeo/lollms-webui)
- [LibreChat](https://github.com/danny-avila/LibreChat)
- [Bionic GPT](https://github.com/bionic-gpt/bionic-gpt)
- [HTML UI](https://github.com/rtcfirefly/ollama-ui)
- [Saddle](https://github.com/jikkuatwork/saddle)
- [Chatbot UI](https://github.com/ivanfioravanti/chatbot-ollama)
- [Chatbot UI v2](https://github.com/mckaywrigley/chatbot-ui)
- [Typescript UI](https://github.com/ollama-interface/Ollama-Gui?tab=readme-ov-file)
- [Minimalistic React UI for Ollama Models](https://github.com/richawo/minimal-llm-ui)
- [Ollamac](https://github.com/kevinhermawan/Ollamac)
- [big-AGI](https://github.com/enricoros/big-AGI/blob/main/docs/config-local-ollama.md)
- [Cheshire Cat assistant framework](https://github.com/cheshire-cat-ai/core)
- [Amica](https://github.com/semperai/amica)
- [chatd](https://github.com/BruceMacD/chatd)
- [Ollama-SwiftUI](https://github.com/kghandour/Ollama-SwiftUI)
- [Dify.AI](https://github.com/langgenius/dify)
- [MindMac](https://mindmac.app)
- [NextJS Web Interface for Ollama](https://github.com/jakobhoeg/nextjs-ollama-llm-ui)
- [Msty](https://msty.app)
- [Chatbox](https://github.com/Bin-Huang/Chatbox)
- [WinForm Ollama Copilot](https://github.com/tgraupmann/WinForm_Ollama_Copilot)
- [NextChat](https://github.com/ChatGPTNextWeb/ChatGPT-Next-Web) 附带 [入门文档](https://docs.nextchat.dev/models/ollama)
- [Alpaca WebUI](https://github.com/mmo80/alpaca-webui)
- [OllamaGUI](https://github.com/enoch1118/ollamaGUI)
- [OpenAOE](https://github.com/InternLM/OpenAOE)
- [Odin Runes](https://github.com/leonid20000/OdinRunes)
- [LLM-X](https://github.com/mrdjohnson/llm-x) (渐进式 Web 应用)
- [AnythingLLM (Docker + macOS/Windows/Linux 原生应用)](https://github.com/Mintplex-Labs/anything-llm)
- [Ollama Basic Chat: 使用 HyperDiv 反应式 UI](https://github.com/rapidarchitect/ollama_basic_chat)
- [Ollama-chats RPG](https://github.com/drazdra/ollama-chats)
- [QA-Pilot](https://github.com/reid41/QA-Pilot) (与代码仓库聊天)
- [ChatOllama](https://github.com/sugarforever/chat-ollama) (基于 Ollama 的开源聊天机器人，支持知识库)
- [CRAG Ollama Chat](https://github.com/Nagi-ovo/CRAG-Ollama-Chat) (简单的 Web 搜索，带有纠正的 RAG)
- [RAGFlow](https://github.com/infiniflow/ragflow) (基于深度文档理解的开源检索增强生成引擎)
- [StreamDeploy](https://github.com/StreamDeploy-DevRel/streamdeploy-llm-app-scaffold) (LLM 应用框架)
- [chat](https://github.com/swuecho/chat) (团队聊天 Web 应用)
- [Lobe Chat](https://github.com/lobehub/lobe-chat) 附带 [集成文档](https://lobehub.com/docs/self-hosting/examples/ollama)
- [Ollama RAG Chatbot](https://github.com/datvodinh/rag-chatbot.git) (使用 Ollama 和 RAG 与多个 PDF 文件本地聊天)
- [BrainSoup](https://www.nurgo-software.com/products/brainsoup) (灵活的原生客户端，带有 RAG 和多代理自动化)
- [macai](https://github.com/Renset/macai) (macOS 客户端，支持 Ollama、ChatGPT 和其他兼容的 API 后端)
- [Ollama Grid Search](https://github.com/dezoito/ollama-grid-search) (评估和比较模型的应用)
- [Olpaka](https://github.com/Otacon/olpaka) (用户友好的 Flutter Web 应用，支持 Ollama)
- [OllamaSpring](https://github.com/CrazyNeil/OllamaSpring) (macOS 客户端，支持 Ollama)
- [LLocal.in](https://github.com/kartikm7/llocal) (易于使用的 Electron 桌面客户端，支持 Ollama)
- [Shinkai Desktop](https://github.com/dcSpark/shinkai-apps) (两步安装本地 AI，使用 Ollama + 文件 + RAG)
- [AiLama](https://github.com/zeyoyt/ailama) (Discord 用户应用，允许你在 Discord 中与 Ollama 互动)
- [Ollama with Google Mesop](https://github.com/rapidarchitect/ollama_mesop/) (使用 Ollama 的 Mesop 聊天客户端实现)
- [R2R](https://github.com/SciPhi-AI/R2R) (开源 RAG 引擎)
- [Ollama-Kis](https://github.com/elearningshow/ollama-kis) (一个简单易用的 GUI，带有示例自定义 LLM，用于驾驶员教育)
- [OpenGPA](https://opengpa.org) (开源离线优先的企业代理应用)
- [Painting Droid](https://github.com/mateuszmigas/painting-droid) (带有 AI 集成的绘画应用)
- [Kerlig AI](https://www.kerlig.com/) (macOS 的 AI 写作助手)
- [AI Studio](https://github.com/MindWorkAI/AI-Studio)
- [Sidellama](https://github.com/gyopak/sidellama) (基于浏览器的 LLM 客户端)
- [LLMStack](https://github.com/trypromptly/LLMStack) (无代码多代理框架，用于构建 LLM 代理和工作流)
- [BoltAI for Mac](https://boltai.com) (Mac 的 AI 聊天客户端)
- [Harbor](https://github.com/av/harbor) (以 Ollama 为默认后端的容器化 LLM 工具包)
- [PyGPT](https://github.com/szczyglis-dev/py-gpt) (适用于 Linux、Windows 和 Mac 的 AI 桌面助手)
- [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT/blob/master/docs/content/platform/ollama.md) (AutoGPT Ollama 集成)
- [Go-CREW](https://www.jonathanhecl.com/go-crew/) (强大的 Golang 离线 RAG)
- [PartCAD](https://github.com/openvmp/partcad/) (使用 OpenSCAD 和 CadQuery 生成 CAD 模型)
- [Ollama4j Web UI](https://github.com/ollama4j/ollama4j-web-ui) - 基于 Java 的 Ollama Web UI，使用 Vaadin、Spring Boot 和 Ollama4j 构建
- [PyOllaMx](https://github.com/kspviswa/pyOllaMx) - macOS 应用，支持与 Ollama 和 Apple MLX 模型聊天
- [Claude Dev](https://github.com/saoudrizwan/claude-dev) - VSCode 扩展，支持多文件/全仓库编码
- [Cherry Studio](https://github.com/kangfenmao/cherry-studio) (支持 Ollama 的桌面客户端)
- [ConfiChat](https://github.com/1runeberg/confichat) (轻量级、独立、多平台、注重隐私的 LLM 聊天界面，可选加密)
- [Archyve](https://github.com/nickthecook/archyve) (支持 RAG 的文档库)
- [crewAI with Mesop](https://github.com/rapidarchitect/ollama-crew-mesop) (运行 crewAI 的 Mesop Web 界面，支持 Ollama)
- [Tkinter-based client](https://github.com/chyok/ollama-gui) (基于 Python tkinter 的 Ollama 客户端)
- [LLMChat](https://github.com/trendy-design/llmchat) (注重隐私、100% 本地、直观的全功能聊天界面)
- [Local Multimodal AI Chat](https://github.com/Leon-Sander/Local-Multimodal-AI-Chat) (基于 Ollama 的 LLM 聊天，支持多种功能，包括 PDF RAG、语音聊天、图像交互和 OpenAI 集成)
- [ARGO](https://github.com/xark-argo/argo) (在 Mac/Windows/Linux 上本地下载和运行 Ollama 和 Huggingface 模型，支持 RAG)
- [OrionChat](https://github.com/EliasPereirah/OrionChat) - OrionChat 是一个用于与不同 AI 提供商聊天的 Web 界面
- [G1](https://github.com/bklieger-groq/g1) (使用提示策略改进 LLM 推理的原型，通过 o1 类推理链)
- [Web management](https://github.com/lemonit-eric-mao/ollama-web-management) (Web 管理页面)
- [Promptery](https://github.com/promptery/promptery) (Ollama 的桌面客户端)
- [Ollama App](https://github.com/JHubi1/ollama-app) (现代且易于使用的多平台客户端，支持 Ollama)
- [ollamarama-matrix](https://github.com/h1ddenpr0cess20/ollamarama-matrix) (Matrix 聊天协议的 Ollama 聊天机器人)
- [ollama-chat-app](https://github.com/anan1213095357/ollama-chat-app) (基于 Flutter 的聊天应用)
- [Perfect Memory AI](https://www.perfectmemory.ai/) (根据你在屏幕上的所见、会议中的所听和所说，个性化辅助的生产力 AI)
- [Hexabot](https://github.com/hexastack/hexabot) (对话式 AI 构建器)
- [Reddit Rate](https://github.com/rapidarchitect/reddit_analyzer) (搜索和评分 Reddit 主题，带有加权求和)
- [OpenTalkGpt](https://github.com/adarshM84/OpenTalkGpt)
- [VT](https://github.com/vinhnx/vt.ai) (一个最小的多模态 AI 聊天应用，支持动态对话路由。通过 Ollama 支持本地模型)
- [Nosia](https://github.com/nosia-ai/nosia) (基于 Ollama 的易于安装和使用的 RAG 平台)
- [Witsy](https://github.com/nbonamy/witsy) (适用于 Mac/Windows/Linux 的 AI 桌面应用)
- [Abbey](https://github.com/US-Artificial-Intelligence/abbey) (可配置的 AI 接口服务器，支持笔记本、文档存储和 YouTube 支持)

### 云服务

- [Google Cloud](https://cloud.google.com/run/docs/tutorials/gpu-gemma2-with-ollama)
- [Fly.io](https://fly.io/docs/python/do-more/add-ollama/)
- [Koyeb](https://www.koyeb.com/deploy/ollama)

### 终端

- [oterm](https://github.com/ggozad/oterm)
- [Ellama Emacs 客户端](https://github.com/s-kostyaev/ellama)
- [Emacs 客户端](https://github.com/zweifisch/ollama)
- [gen.nvim](https://github.com/David-Kunz/gen.nvim)
- [ollama.nvim](https://github.com/nomnivore/ollama.nvim)
- [ollero.nvim](https://github.com/marco-souza/ollero.nvim)
- [ollama-chat.nvim](https://github.com/gerazov/ollama-chat.nvim)
- [ogpt.nvim](https://github.com/huynle/ogpt.nvim)
- [gptel Emacs 客户端](https://github.com/karthink/gptel)
- [Oatmeal](https://github.com/dustinblackman/oatmeal)
- [cmdh](https://github.com/pgibler/cmdh)
- [ooo](https://github.com/npahlfer/ooo)
- [shell-pilot](https://github.com/reid41/shell-pilot)
- [tenere](https://github.com/pythops/tenere)
- [llm-ollama](https://github.com/taketwo/llm-ollama) 用于 [Datasette 的 LLM CLI](https://llm.datasette.io/en/stable/)
- [typechat-cli](https://github.com/anaisbetts/typechat-cli)
- [ShellOracle](https://github.com/djcopley/ShellOracle)
- [tlm](https://github.com/yusufcanb/tlm)
- [podman-ollama](https://github.com/ericcurtin/podman-ollama)
- [gollama](https://github.com/sammcj/gollama)
- [ParLlama](https://github.com/paulrobello/parllama)
- [Ollama 电子书摘要](https://github.com/cognitivetech/ollama-ebook-summary/)
- [Ollama 专家混合模型 (MOE) 50 行代码实现](https://github.com/rapidarchitect/ollama_moe)
- [vim-intelligence-bridge](https://github.com/pepo-ec/vim-intelligence-bridge) “Ollama” 与 Vim 编辑器的简单交互
- [x-cmd ollama](https://x-cmd.com/mod/ollama)
- [bb7](https://github.com/drunkwcodes/bb7)
- [SwollamaCLI](https://github.com/marcusziade/Swollama) 与 Swollama Swift 包捆绑。[演示](https://github.com/marcusziade/Swollama?tab=readme-ov-file#cli-usage)
- [aichat](https://github.com/sigoden/aichat) 一体化 LLM CLI 工具，包含 Shell 助手、Chat-REPL、RAG、AI 工具和代理，支持 OpenAI、Claude、Gemini、Ollama、Groq 等。
- [orbiton](https://github.com/xyproto/orbiton) 无需配置的文本编辑器和 IDE，支持使用 Ollama 进行代码补全。

### Apple Vision Pro

- [Enchanted](https://github.com/AugustDev/enchanted)

### 数据库

- [MindsDB](https://github.com/mindsdb/mindsdb/blob/staging/mindsdb/integrations/handlers/ollama_handler/README.md)（将 Ollama 模型与近 200 个数据平台和应用程序连接）
- [chromem-go](https://github.com/philippgille/chromem-go/blob/v0.5.0/embed_ollama.go) 附带 [示例](https://github.com/philippgille/chromem-go/tree/v0.5.0/examples/rag-wikipedia-ollama)

### 软件包管理器

- [Pacman](https://archlinux.org/packages/extra/x86_64/ollama/)
- [Gentoo](https://github.com/gentoo/guru/tree/master/app-misc/ollama)
- [Helm Chart](https://artifacthub.io/packages/helm/ollama-helm/ollama)
- [Guix 通道](https://codeberg.org/tusharhero/ollama-guix)
- [Nix 软件包](https://search.nixos.org/packages?channel=24.05&show=ollama&from=0&size=50&sort=relevance&type=packages&query=ollama)
- [Flox](https://flox.dev/blog/ollama-part-one)

### 库

- [LangChain](https://python.langchain.com/docs/integrations/llms/ollama) 和 [LangChain.js](https://js.langchain.com/docs/integrations/chat/ollama/) 附带 [示例](https://js.langchain.com/docs/tutorials/local_rag/)
- [Firebase Genkit](https://firebase.google.com/docs/genkit/plugins/ollama)
- [crewAI](https://github.com/crewAIInc/crewAI)
- [Spring AI](https://github.com/spring-projects/spring-ai) 附带 [参考](https://docs.spring.io/spring-ai/reference/api/chat/ollama-chat.html) 和 [示例](https://github.com/tzolov/ollama-tools)
- [LangChainGo](https://github.com/tmc/langchaingo/) 附带 [示例](https://github.com/tmc/langchaingo/tree/main/examples/ollama-completion-example)
- [LangChain4j](https://github.com/langchain4j/langchain4j) 附带 [示例](https://github.com/langchain4j/langchain4j-examples/tree/main/ollama-examples/src/main/java)
- [LangChainRust](https://github.com/Abraxas-365/langchain-rust) 附带 [示例](https://github.com/Abraxas-365/langchain-rust/blob/main/examples/llm_ollama.rs)
- [LLPhant](https://github.com/theodo-group/LLPhant?tab=readme-ov-file#ollama)
- [LlamaIndex](https://docs.llamaindex.ai/en/stable/examples/llm/ollama/) 和 [LlamaIndexTS](https://ts.llamaindex.ai/modules/llms/available_llms/ollama)
- [LiteLLM](https://github.com/BerriAI/litellm)
- [OllamaFarm for Go](https://github.com/presbrey/ollamafarm)
- [OllamaSharp for .NET](https://github.com/awaescher/OllamaSharp)
- [Ollama for Ruby](https://github.com/gbaptista/ollama-ai)
- [Ollama-rs for Rust](https://github.com/pepperoni21/ollama-rs)
- [Ollama-hpp for C++](https://github.com/jmont-dev/ollama-hpp)
- [Ollama4j for Java](https://github.com/ollama4j/ollama4j)
- [ModelFusion Typescript 库](https://modelfusion.dev/integration/model-provider/ollama)
- [OllamaKit for Swift](https://github.com/kevinhermawan/OllamaKit)
- [Ollama for Dart](https://github.com/breitburg/dart-ollama)
- [Ollama for Laravel](https://github.com/cloudstudio/ollama-laravel)
- [LangChainDart](https://github.com/davidmigloz/langchain_dart)
- [Semantic Kernel - Python](https://github.com/microsoft/semantic-kernel/tree/main/python/semantic_kernel/connectors/ai/ollama)
- [Haystack](https://github.com/deepset-ai/haystack-integrations/blob/main/integrations/ollama.md)
- [Elixir LangChain](https://github.com/brainlid/langchain)
- [Ollama for R - rollama](https://github.com/JBGruber/rollama)
- [Ollama for R - ollama-r](https://github.com/hauselin/ollama-r)
- [Ollama-ex for Elixir](https://github.com/lebrunel/ollama-ex)
- [Ollama Connector for SAP ABAP](https://github.com/b-tocs/abap_btocs_ollama)
- [Testcontainers](https://testcontainers.com/modules/ollama/)
- [Portkey](https://portkey.ai/docs/welcome/integration-guides/ollama)
- [PromptingTools.jl](https://github.com/svilupp/PromptingTools.jl) 附带 [示例](https://svilupp.github.io/PromptingTools.jl/dev/examples/working_with_ollama)
- [LlamaScript](https://github.com/Project-Llama/llamascript)
- [llm-axe](https://github.com/emirsahin1/llm-axe)（用于构建 LLM 驱动应用程序的 Python 工具包）
- [Gollm](https://docs.gollm.co/examples/ollama-example)
- [Gollama for Golang](https://github.com/jonathanhecl/gollama)
- [Ollamaclient for Golang](https://github.com/xyproto/ollamaclient)
- [Go 中的高级函数抽象](https://gitlab.com/tozd/go/fun)
- [Ollama PHP](https://github.com/ArdaGnsrn/ollama-php)
- [Agents-Flex for Java](https://github.com/agents-flex/agents-flex) 附带 [示例](https://github.com/agents-flex/agents-flex/tree/main/agents-flex-llm/agents-flex-llm-ollama/src/test/java/com/agentsflex/llm/ollama)
- [Parakeet](https://github.com/parakeet-nest/parakeet) 是一个 GoLang 库，旨在简化使用 Ollama 开发小型生成式 AI 应用程序的过程。
- [Haverscript](https://github.com/andygill/haverscript) 附带 [示例](https://github.com/andygill/haverscript/tree/main/examples)
- [Ollama for Swift](https://github.com/mattt/ollama-swift)
- [Swollama for Swift](https://github.com/marcusziade/Swollama) 附带 [DocC](https://marcusziade.github.io/Swollama/documentation/swollama/)
- [GoLamify](https://github.com/prasad89/golamify)
- [Ollama for Haskell](https://github.com/tusharad/ollama-haskell)
- [multi-llm-ts](https://github.com/nbonamy/multi-llm-ts)（一个允许通过统一 API 访问不同 LLM 的 Typescript/JavaScript 库）

### 移动端

- [Enchanted](https://github.com/AugustDev/enchanted)
- [Maid](https://github.com/Mobile-Artificial-Intelligence/maid)
- [Ollama App](https://github.com/JHubi1/ollama-app)（现代且易于使用的多平台 Ollama 客户端）
- [ConfiChat](https://github.com/1runeberg/confichat)（轻量级、独立、多平台且注重隐私的 LLM 聊天界面，可选加密）

### 扩展与插件

- [Raycast 扩展](https://github.com/MassimilianoPasquini97/raycast_ollama)
- [Discollama](https://github.com/mxyng/discollama)（Ollama Discord 频道内的 Discord 机器人）
- [Continue](https://github.com/continuedev/continue)
- [Vibe](https://github.com/thewh1teagle/vibe)（使用 Ollama 转录和分析会议）
- [Obsidian Ollama 插件](https://github.com/hinterdupfinger/obsidian-ollama)
- [Logseq Ollama 插件](https://github.com/omagdy7/ollama-logseq)
- [NotesOllama](https://github.com/andersrex/notesollama)（Apple Notes Ollama 插件）
- [Dagger Chatbot](https://github.com/samalba/dagger-chatbot)
- [Discord AI 机器人](https://github.com/mekb-turtle/discord-ai-bot)
- [Ollama Telegram 机器人](https://github.com/ruecat/ollama-telegram)
- [Hass Ollama 会话](https://github.com/ej52/hass-ollama-conversation)
- [Rivet 插件](https://github.com/abrenneke/rivet-plugin-ollama)
- [Obsidian BMO Chatbot 插件](https://github.com/longy2k/obsidian-bmo-chatbot)
- [Cliobot](https://github.com/herval/cliobot)（支持 Ollama 的 Telegram 机器人）
- [Copilot for Obsidian 插件](https://github.com/logancyang/obsidian-copilot)
- [Obsidian Local GPT 插件](https://github.com/pfrankov/obsidian-local-gpt)
- [Open Interpreter](https://docs.openinterpreter.com/language-model-setup/local-models/ollama)
- [Llama Coder](https://github.com/ex3ndr/llama-coder)（使用 Ollama 的 Copilot 替代方案）
- [Ollama Copilot](https://github.com/bernardo-bruning/ollama-copilot)（允许你将 Ollama 用作类似 Github Copilot 的代理）
- [twinny](https://github.com/rjmacarthy/twinny)（使用 Ollama 的 Copilot 和 Copilot 聊天替代方案）
- [Wingman-AI](https://github.com/RussellCanfield/wingman-ai)（使用 Ollama 和 Hugging Face 的 Copilot 代码和聊天替代方案）
- [Page Assist](https://github.com/n4ze3m/page-assist)（Chrome 扩展）
- [Plasmoid Ollama Control](https://github.com/imoize/plasmoid-ollamacontrol)（KDE Plasma 扩展，允许你快速管理和控制 Ollama 模型）
- [AI Telegram 机器人](https://github.com/tusharhero/aitelegrambot)（使用 Ollama 作为后端的 Telegram 机器人）
- [AI ST Completion](https://github.com/yaroslavyaroslav/OpenAI-sublime-text)（支持 Ollama 的 Sublime Text 4 AI 助手插件）
- [Discord-Ollama 聊天机器人](https://github.com/kevinthedang/discord-ollama)（通用的 TypeScript Discord 机器人，附带调优文档）
- [Discord AI 聊天/管理机器人](https://github.com/rapmd73/Companion)（用 Python 编写的聊天/管理机器人。使用 Ollama 创建个性。）
- [Headless Ollama](https://github.com/nischalj10/headless-ollama)（脚本自动在任何操作系统上安装 Ollama 客户端和模型，适用于依赖 Ollama 服务器的应用程序）
- [Terraform AWS Ollama & Open WebUI](https://github.com/xuyangbocn/terraform-aws-self-host-llm)（一个 Terraform 模块，用于在 AWS 上部署一个即用型 Ollama 服务，附带前端 Open WebUI 服务）
- [node-red-contrib-ollama](https://github.com/jakubburkiewicz/node-red-contrib-ollama)
- [Local AI Helper](https://github.com/ivostoykov/localAI)（Chrome 和 Firefox 扩展，允许与当前标签页和自定义 API 端点进行交互。包括用户提示的安全存储。）
- [vnc-lm](https://github.com/jk011ru/vnc-lm)（支持附件和网页链接的容器化 Discord 机器人）
- [LSP-AI](https://github.com/SilasMarvin/lsp-ai)（开源 AI 功能语言服务器）
- [QodeAssist](https://github.com/Palm1r/QodeAssist)（Qt Creator 的 AI 功能编码助手插件）
- [Obsidian Quiz Generator 插件](https://github.com/ECuiDev/obsidian-quiz-generator)
- [TextCraft](https://github.com/suncloudsmoon/TextCraft)（使用 Ollama 的 Word 中的 Copilot 替代方案）
- [Alfred Ollama](https://github.com/zeitlings/alfred-ollama)（Alfred 工作流）

### 支持的后端

- [llama.cpp](https://github.com/ggerganov/llama.cpp) 项目由 Georgi Gerganov 创立。