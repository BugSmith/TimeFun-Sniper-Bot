# TimeFun Sniper Bot

[![en](https://img.shields.io/badge/lang-English-blue.svg)](README.md) [![cn](https://img.shields.io/badge/语言-中文-red.svg)](README_CN.md)

这是一个监控Twitter并在time.fun网站上自动购买时间币的机器人。

> **开发状态**: [已完成] 自动购买功能已完成并测试通过。[已完成] Twitter监控功能已完成。

## 功能特点

- 监控@timedotfun Twitter账号的转发
- 自动识别被推广的用户名
- 自动在time.fun上为推广用户购买时间币
- 连接到您现有的Chrome会话以避免Cloudflare检测
- 支持两步购买确认流程

## [SAFE]安全提示

**重要**: 此机器人需要访问您的Chrome浏览器和TimeFun账户。请注意以下安全考虑事项：

- 机器人通过远程调试模式连接到您的Chrome浏览器，这可能会使您的浏览器暴露给其他应用程序
- 您的Chrome用户数据目录包含敏感信息，包括cookies和保存的密码
- `.env.utf8`文件包含配置信息
- 切勿共享您的`.env.utf8`文件、调试截图或Chrome用户数据目录
- 在运行前请审查代码，确保它符合您的安全要求

## 安装步骤

1. 克隆此仓库
2. 安装依赖: `pip install -r requirements.txt`
3. 创建`.env.utf8`文件并进行必要的配置（参见配置部分）

## 配置说明

在您的`.env.utf8`文件中配置以下内容（注意：不要在值后面添加注释，这可能会导致解析错误）：

```
# 购买设置
BUY_AMOUNT=2
MAX_BUY_ATTEMPTS=3
BUY_DELAY=2

# 监控设置
CHECK_INTERVAL=60
HEADLESS=False

# Chrome设置
# 重要：您必须设置为您的Chrome用户数据目录
CHROME_USER_DATA_DIR=C:\\Users\\YourUsername\\AppData\\Local\\Google\\Chrome\\User Data
```

### Chrome用户数据目录

`CHROME_USER_DATA_DIR`设置是**必需的**，必须指向您的Chrome用户数据目录：

- **Windows:** 通常为 `C:\Users\您的用户名\AppData\Local\Google\Chrome\User Data`
- **Mac:** 通常为 `~/Library/Application Support/Google/Chrome`
- **Linux:** 通常为 `~/.config/google-chrome`

确保在Windows路径中使用双反斜杠(`\\`)。

### 配置详情

- `BUY_AMOUNT`: 每次购买的USDC金额
- `MAX_BUY_ATTEMPTS`: 最大购买尝试次数
- `BUY_DELAY`: 购买操作之间的延迟（秒）
- `CHECK_INTERVAL`: 检查Twitter的间隔（秒）
- `HEADLESS`: 使用现有Chrome会话时应设置为False

## Chrome设置

机器人可以连接到已运行的Chrome实例或自动启动Chrome：

### 选项1：手动启动Chrome（推荐）

1. 关闭所有Chrome窗口
2. 使用以下命令启动带有远程调试功能的Chrome：

   **Windows:**
   ```
   "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\您的用户名\AppData\Local\Google\Chrome\User Data"
   ```

   **Mac:**
   ```
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="~/Library/Application Support/Google/Chrome"
   ```

   **Linux:**
   ```
   google-chrome --remote-debugging-port=9222 --user-data-dir="~/.config/google-chrome"
   ```

3. 在打开的Chrome窗口中，导航到https://time.fun并登录
4. 保持Chrome打开并运行
5. 然后运行机器人

### 选项2：自动启动Chrome

如果满足以下条件，机器人现在可以自动使用正确的参数启动Chrome：
- Chrome尚未以远程调试模式运行
- 您已在`.env.utf8`文件中正确设置了`CHROME_USER_DATA_DIR`

## 使用方法

程序提供了以下运行模式：

### 1. 监控模式（主要功能）

使用`timefun_buyer_en.py`来监控Twitter并自动购买：

```bash
python timefun_buyer_en.py [选项]
```

可用选项：
- `--username` 或 `-u`: 设置要监控的Twitter用户名（默认：timedotfun）
- `--interval` 或 `-i`: 设置检查间隔（秒，默认：30）
- `--timezone` 或 `-t`: 设置时区偏移（默认：8，北京时间）
- `--max-tweets` 或 `-m`: 设置每次检查的最大推文数（默认：5）
- `--skip-login-check`: 跳过登录检查

### 2. 直接购买模式

使用`timefun_buyer_en.py`直接购买指定用户的时间币：

```bash
python timefun_buyer_en.py --buy 用户名 [--skip-login-check]
```

### 3. 验证模式

验证用户是否存在于time.fun：

```bash
python timefun_buyer_en.py --verify 用户名
```

## 故障排除

### 登录检测问题

如果机器人无法检测到您已登录（即使您确实已登录），请使用`--skip-login-check`标志：

```bash
python timefun_buyer_en.py --skip-login-check
```

### 按钮检测问题

如果机器人找不到购买按钮：
1. 检查项目目录中保存的调试截图（debug_screenshot_*.png）
2. 查看控制台输出中的按钮文本信息
3. 确保您在Chrome会话中已登录TimeFun

## 文件说明

- `timefun_buyer_en.py` - 主程序，包含监控和购买功能
- `test_buy_en.py` - 购买功能测试脚本
- `.env.utf8` - 环境变量配置文件

## 开发状态

当前版本: 1.0.0

### 已完成功能
- [已完成] 自动购买功能
  - Chrome集成和远程调试
  - 自动启动Chrome
  - 市场页面导航
  - 两步购买流程
  - 详细错误日志和截图
- [已完成] Twitter监控功能
  - 实时监控@timedotfun账号
  - 自动识别推广用户名

### 计划中的功能
- [计划中] Web界面监控和控制
- [计划中] 多账户支持

## 重要提示

- 确保您的TimeFun账户有足够的USDC余额
- 使用自动交易工具存在风险
- 开始时使用小金额测试功能，然后再增加
- 此机器人仅供教育目的提供
- 开发者不对任何财务损失或账户问题负责

## 许可证

[MIT许可证](LICENSE) 