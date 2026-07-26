# GKI 5.4 内核云编译 (带 KernelSU)

使用 GitHub Actions 在云端自动编译 Android GKI 5.4 内核，集成 KernelSU 支持。

## 适用设备
- **Meizu 18s** (Snapdragon 888+, ARM64)
- 其他使用 GKI 5.4 内核的 ARM64 设备

## 编译内容
- 内核版本：GKI 5.4 (android12-5.4 分支)
- 工具链：AOSP Clang r416183b + GCC 4.9
- 内核模块：KernelSU 支持（KPROBES + OVERLAY_FS）

## 使用方法

### 方法一：GitHub 网页操作
1. Fork 本仓库到你的 GitHub 账号
2. 进入 Actions 页面，启用 Workflows
3. 点击 "Build GKI 5.4 Kernel with KernelSU"
4. 点击 "Run workflow" → "Run workflow"
5. 等待编译完成（约 20-40 分钟）
6. 在 Actions 运行详情页下载 Artifacts

### 方法二：本地推送触发
```bash
git init
git add .
git commit -m "init gki builder"
git branch -M main
git remote add origin https://github.com/你的用户名/gki-kernel-builder.git
git push -u origin main
```

## 产物说明
编译产物 `GKI-5.4-meizu18s-日期.tar.gz` 包含：
- `Image` — 内核镜像
- `modules/*.ko` — 内核模块
- `kernel_config` — 内核编译配置
- `build.log` — 编译日志

## 技术参数
| 项目 | 值 |
|------|-----|
| 内核分支 | android12-5.4 |
| 架构 | ARM64 (aarch64) |
| Clang 版本 | r416183b |
| 交叉编译器 | aarch64-linux-android- (GCC 4.9) |
| 32位编译器 | arm-linux-androideabi- (GCC 4.9) |

## KernelSU 内核配置
编译时自动启用以下内核选项以支持 KernelSU：
- CONFIG_KPROBES=y
- CONFIG_HAVE_KPROBES=y
- CONFIG_KPROBE_EVENTS=y
- CONFIG_OVERLAY_FS=y
- CONFIG_MODULES=y
- CONFIG_MODULE_UNLOAD=y

## 注意事项
- GitHub Actions 免费额度：每月 2000 分钟
- 首次编译约需 30-40 分钟（含工具链下载）
- 后续编译可利用缓存加速至约 15-20 分钟
- Artifacts 保留 30 天
