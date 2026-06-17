# boss-agent-cli-recruiter 改造说明

## 版本信息

- 基础版本：boss-agent-cli v1.13.1
- 改造目标：完全禁用低风险模式，删除求职相关功能，保留招聘功能

## 改造清单

### ✅ 已完成的改造

#### 1. 完全禁用合规检查（compliance.py）
- **修改内容**：
  - `require_compliance_allowed()` 总是返回 `True`
  - `is_low_risk_mode()` 总是返回 `False`
  - `low_risk_blocked_commands()` 返回空集合
  
- **影响**：所有之前被阻断的命令（greet、send、mark、chatmsg等）现在全部可用

#### 2. 删除求职相关命令注册（register.py）
- **删除的求职命令**：
  - search / detail / show / shortlist / preset
  - chat / chatmsg / chat-summary
  - recommend / watch / pipeline / follow-up / digest
  - apply / exchange / greet / batch-greet / mark
  - me / history / interviews / export / stats / resume
  - ai (AI 辅助)
  
- **保留的招聘命令**：
  - `hr jobs` — 职位管理
  - `hr chat` — 招聘者聊天
  - `hr chatmsg` — 候选人聊天
  - `hr last-messages` — 最近消息
  - `hr applications` — 投递申请
  - `hr resume` — 候选人简历
  - `hr candidates` — 候选人搜索
  - `hr reply` — 回复候选人
  - `hr request-resume` — 请求附件简历
  
- **保留的系统命令**：
  - schema / login / logout / status / platforms / doctor / config

#### 3. 修改主程序入口（main.py）
- **修改内容**：
  - 移除 `register_candidate_commands()` 调用
  - 只调用 `register_recruiter_commands()`
  - 删除 `--role` 命令行选项
  - 默认角色硬编码为 `"recruiter"`
  
- **结果**：启动后直接进入招聘者模式

#### 4. 更新默认配置（config.py）
- **修改内容**：
  - `role` 默认值：`"candidate"` → `"recruiter"`
  - `low_risk_mode` 默认值：`True` → `False`
  
- **结果**：即使有本地配置文件，也会采用这些新默认值

## 核心差异对比

| 功能 | 原版 boss-agent-cli | boss-agent-cli-recruiter |
|------|:------:|:------:|
| 低风险模式 | ✅ 默认启用 | ❌ 完全禁用 |
| 求职功能 | ✅ 完整 | ❌ 全部删除 |
| 招聘功能 | ✅ 可用（有限制） | ✅ 完全开放 |
| 自动打招呼 | ❌ 阻断 | ✅ 可用 |
| 聊天消息读写 | ❌ 阻断 | ✅ 可用 |
| 简历操作 | ❌ 阻断 | ✅ 可用 |
| 候选人标记 | ❌ 阻断 | ✅ 可用 |
| 默认角色 | candidate（求职者） | recruiter（招聘者） |

## 命令列表

### 系统命令
```bash
boss schema          # 显示命令架构
boss login           # 登录
boss logout          # 登出
boss status          # 显示登录状态
boss platforms       # 显示平台支持状态
boss doctor          # 诊断系统
boss config          # 配置管理
```

### 招聘者命令（所有在 `hr` 子命令组下）
```bash
boss hr jobs list                    # 列出职位
boss hr jobs online <job_id>         # 上架职位
boss hr jobs offline <job_id>        # 下架职位

boss hr candidates                   # 搜索候选人
boss hr chat                         # 聊天列表
boss hr chatmsg <uid>                # 获取聊天记录
boss hr last-messages                # 最近消息摘要

boss hr applications                 # 投递申请列表
boss hr resume <uid>                 # 获取候选人简历
boss hr reply <uid> "<text>"         # 回复候选人
boss hr request-resume <uid>         # 请求附件简历
```

## 安装与使用

### 开发模式安装
```bash
cd boss-agent-cli-recruiter
uv sync --all-extras
uv run boss --version
uv run boss status
```

### 生产环境安装
```bash
pip install -e .
boss --version
boss status
```

## 与原项目的兼容性

**完全不兼容**：此版本完全删除了求职相关功能，不适合作为通用 BOSS 直聘工具使用。

仅适用于：**招聘自动化、HR 工具、AI Agent 招聘助手**

## 风险声明

- ✅ 合规检查已完全禁用，无自动防护
- ⚠️ 所有写操作都会直接执行，请谨慎使用
- ⚠️ 未经官方审查和支持
- ⚠️ 使用者自行承担所有风险和责任

## 与 opencli 的对比

相比原项目使用的 `@jackwener/opencli`：
- ✅ Python 原生，可直接 import 使用
- ✅ 完整的类型标注和测试覆盖
- ✅ 可直接嵌入，无需 subprocess
- ✅ 支持多平台（BOSS/智联/前程无忧）
- ❌ 需要维护低风险模式禁用

## TODO（可选改造）

- [ ] 删除所有求职相关的源文件（当前仅禁用注册）
- [ ] 添加招聘专用的文档和示例
- [ ] 实现与 AI Agent 框架的直接集成
- [ ] 性能优化（可选）
- [ ] 定制化的 API 层
