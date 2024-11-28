# GPU
## Nvidia
Ollama 支持计算能力为 5.0 及以上的 Nvidia GPU。

检查你的计算兼容性，以确认你的显卡是否受支持：
[https://developer.nvidia.com/cuda-gpus](https://developer.nvidia.com/cuda-gpus)


| Compute Capability | Family              | Cards                                                                                                       |
| ------------------ | ------------------- | ----------------------------------------------------------------------------------------------------------- |
| 9.0                | NVIDIA              | `H100`                                                                                                      |
| 8.9                | GeForce RTX 40xx    | `RTX 4090` `RTX 4080 SUPER` `RTX 4080` `RTX 4070 Ti SUPER` `RTX 4070 Ti` `RTX 4070 SUPER` `RTX 4070` `RTX 4060 Ti` `RTX 4060`  |
|                    | NVIDIA Professional | `L4` `L40` `RTX 6000`                                                                                       |
| 8.6                | GeForce RTX 30xx    | `RTX 3090 Ti` `RTX 3090` `RTX 3080 Ti` `RTX 3080` `RTX 3070 Ti` `RTX 3070` `RTX 3060 Ti` `RTX 3060` `RTX 3050 Ti` `RTX 3050`   |
|                    | NVIDIA Professional | `A40` `RTX A6000` `RTX A5000` `RTX A4000` `RTX A3000` `RTX A2000` `A10` `A16` `A2`                          |
| 8.0                | NVIDIA              | `A100` `A30`                                                                                                |
| 7.5                | GeForce GTX/RTX     | `GTX 1650 Ti` `TITAN RTX` `RTX 2080 Ti` `RTX 2080` `RTX 2070` `RTX 2060`                                    |
|                    | NVIDIA Professional | `T4` `RTX 5000` `RTX 4000` `RTX 3000` `T2000` `T1200` `T1000` `T600` `T500`                                 |
|                    | Quadro              | `RTX 8000` `RTX 6000` `RTX 5000` `RTX 4000`                                                                 |
| 7.0                | NVIDIA              | `TITAN V` `V100` `Quadro GV100`                                                                             |
| 6.1                | NVIDIA TITAN        | `TITAN Xp` `TITAN X`                                                                                        |
|                    | GeForce GTX         | `GTX 1080 Ti` `GTX 1080` `GTX 1070 Ti` `GTX 1070` `GTX 1060` `GTX 1050 Ti` `GTX 1050`                       |
|                    | Quadro              | `P6000` `P5200` `P4200` `P3200` `P5000` `P4000` `P3000` `P2200` `P2000` `P1000` `P620` `P600` `P500` `P520` |
|                    | Tesla               | `P40` `P4`                                                                                                  |
| 6.0                | NVIDIA              | `Tesla P100` `Quadro GP100`                                                                                 |
| 5.2                | GeForce GTX         | `GTX TITAN X` `GTX 980 Ti` `GTX 980` `GTX 970` `GTX 960` `GTX 950`                                          |
|                    | Quadro              | `M6000 24GB` `M6000` `M5000` `M5500M` `M4000` `M2200` `M2000` `M620`                                        |
|                    | Tesla               | `M60` `M40`                                                                                                 |
| 5.0                | GeForce GTX         | `GTX 750 Ti` `GTX 750` `NVS 810`                                                                            |
|                    | Quadro              | `K2200` `K1200` `K620` `M1200` `M520` `M5000M` `M4000M` `M3000M` `M2000M` `M1000M` `K620M` `M600M` `M500M`  |


### GPU 选择

如果你的系统中有多个 NVIDIA GPU 并且希望限制 Ollama 使用其中的一部分，可以将 `CUDA_VISIBLE_DEVICES` 设置为 GPU 的逗号分隔列表。可以使用数字 ID，但顺序可能会变化，因此使用 UUID 更可靠。你可以通过运行 `nvidia-smi -L` 来发现 GPU 的 UUID。如果你希望忽略 GPU 并强制使用 CPU，可以使用无效的 GPU ID（例如，"-1"）。

### 笔记本电脑挂起恢复

在 Linux 上，经过一次挂起/恢复周期后，有时 Ollama 会无法发现你的 NVIDIA GPU，并回退到在 CPU 上运行。你可以通过重新加载 NVIDIA UVM 驱动来解决这个驱动程序错误，命令为 `sudo rmmod nvidia_uvm && sudo modprobe nvidia_uvm`。

## AMD Radeon
Ollama 支持以下 AMD GPU：

### Linux 支持


| Family         | Cards and accelerators                                                                                                               |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| AMD Radeon RX  | `7900 XTX` `7900 XT` `7900 GRE` `7800 XT` `7700 XT` `7600 XT` `7600` `6950 XT` `6900 XTX` `6900XT` `6800 XT` `6800` `Vega 64` `Vega 56`    |
| AMD Radeon PRO | `W7900` `W7800` `W7700` `W7600` `W7500` `W6900X` `W6800X Duo` `W6800X` `W6800` `V620` `V420` `V340` `V320` `Vega II Duo` `Vega II` `VII` `SSG` |
| AMD Instinct   | `MI300X` `MI300A` `MI300` `MI250X` `MI250` `MI210` `MI200` `MI100` `MI60` `MI50`                                                               |


### Windows 支持
从 ROCm v6.1 开始，以下 GPU 在 Windows 上受支持。


| Family         | Cards and accelerators                                                                                                               |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| AMD Radeon RX  | `7900 XTX` `7900 XT` `7900 GRE` `7800 XT` `7700 XT` `7600 XT` `7600` `6950 XT` `6900 XTX` `6900XT` `6800 XT` `6800`    |
| AMD Radeon PRO | `W7900` `W7800` `W7700` `W7600` `W7500` `W6900X` `W6800X Duo` `W6800X` `W6800` `V620` |


### Linux 上的覆盖设置
Ollama 利用了 AMD ROCm 库，但该库并不支持所有 AMD GPU。在某些情况下，你可以强制系统尝试使用一个接近的 LLVM 目标。例如，Radeon RX 5400 是 `gfx1034`（也称为 10.3.4），但 ROCm 当前不支持此目标。最接近的支持目标是 `gfx1030`。你可以使用环境变量 `HSA_OVERRIDE_GFX_VERSION`，其语法为 `x.y.z`。因此，例如，要强制系统在 RX 5400 上运行，你可以将 `HSA_OVERRIDE_GFX_VERSION="10.3.0"` 作为服务器的环境变量。如果你有一个不受支持的 AMD GPU，可以尝试使用以下支持的类型列表。

如果你有多个具有不同 GFX 版本的 GPU，可以在环境变量后附加数字设备编号以分别设置它们。例如，`HSA_OVERRIDE_GFX_VERSION_0=10.3.0` 和 `HSA_OVERRIDE_GFX_VERSION_1=11.0.0`。

目前，已知在 Linux 上支持的 GPU 类型如下 LLVM 目标。下表显示了一些映射到这些 LLVM 目标的示例 GPU：


| **LLVM Target** | **An Example GPU** |
|-----------------|---------------------|
| gfx900 | Radeon RX Vega 56 |
| gfx906 | Radeon Instinct MI50 |
| gfx908 | Radeon Instinct MI100 |
| gfx90a | Radeon Instinct MI210 |
| gfx940 | Radeon Instinct MI300 |
| gfx941 | |
| gfx942 | |
| gfx1030 | Radeon PRO V620 |
| gfx1100 | Radeon PRO W7900 |
| gfx1101 | Radeon PRO W7700 |
| gfx1102 | Radeon RX 7600 |


AMD 正在努力增强 ROCm v6，以在未来版本中扩展对更多 GPU 系列的支持，这应该会增加对更多 GPU 的支持。

如果你需要更多帮助，请在 [Discord](https://discord.gg/ollama) 上联系我们，或在 [GitHub](https://github.com/ollama/ollama/issues) 上提交一个 issue。

### GPU 选择

如果你的系统中有多个 AMD GPU，并且希望限制 Ollama 使用其中的一部分，可以将 `ROCR_VISIBLE_DEVICES` 设置为 GPU 的逗号分隔列表。你可以使用 `rocminfo` 查看设备列表。如果你希望忽略 GPU 并强制使用 CPU，可以使用无效的 GPU ID（例如，"-1"）。如果可用，建议使用 `Uuid` 来唯一标识设备，而不是使用数字值。

### 容器权限

在某些 Linux 发行版中，SELinux 可能会阻止容器访问 AMD GPU 设备。你可以在主机系统上运行 `sudo setsebool container_use_devices=1` 以允许容器使用设备。

### Metal（Apple GPU）
Ollama 通过 Metal API 支持 Apple 设备上的 GPU 加速。