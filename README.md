# 网络安全学习计划（3 个月）

本项目提供从零基础到进阶掌握的网络安全系统化学习路径，按天划分，共 90 天。每一天包含：

- 学习目标（明确当天要达成的知识点）
- 学习内容（阅读/视频/标准文档建议）
- 实践任务（动手实验与验证）
- 巩固练习（题目与复盘）
- 评估标准（达成判定）
- 学习成果达成情况（每日自评与证据，如截图/笔记/脚本）

## 项目结构

- `plan/3-month-roadmap.md`: 总体路线图与每周主题概览，链接到每日内容
- `daily/DayXXX.md`: 每日学习卡片（Day001 ~ Day090）
- `scripts/generate_daily_content.py`: 生成每日学习卡片的脚本（可按开始日期生成带日期的文件）
- `.gitignore`: 忽略不必要的文件

## 使用方式

1. 安装依赖（仅需 Python 3.9+，无第三方库）
2. 运行生成脚本（默认从今天开始）：
   - Windows PowerShell：
     ```powershell
     python .\scripts\generate_daily_content.py
     ```
   - 可指定开始日期与输出目录：
     ```powershell
     python .\scripts\generate_daily_content.py -s 2025-12-25 -o .\daily
     ```
3. 每日学习时：
   - 打开当日对应的 `daily/DayXXX.md`，按卡片进行学习与实践
   - 在“学习成果达成情况”处记录截图、命令输出、关键笔记与结论
4. 每日结束后提交到 Git：
   ```powershell
   git add .; git commit -m "DayXXX: 完成学习与记录"
   ```

## 上传到 GitHub 的指南

- 首次初始化：
  ```powershell
  git init
  git add .; git commit -m "初始化网络安全学习计划"
  ```
- 创建 GitHub 仓库（两种方式）：
  1. 使用 GitHub Desktop 或网页端手动新建仓库，然后复制远程地址
  2. 若已安装 GitHub CLI（gh），可执行：
     ```powershell
     gh repo create <your-username>/network-security-learning --source . --private --confirm
     ```
- 关联远程并推送：
  ```powershell
  git remote add origin https://github.com/<your-username>/network-security-learning.git
  git branch -M main
  git push -u origin main
  ```

## 学习原则与环境

- 始终遵循法律与道德规范，仅在授权的实验环境中进行渗透测试与漏洞验证
- 推荐使用本地虚拟化实验环境（如：2 台 Linux + 1 台 Windows + 1 台 Web 靶机），或使用合法的在线靶场
- 对外网目标的任何扫描与攻击行为禁止；仅对自建靶场或明确授权的目标开展实验

## 路线概览（按周主题）

详见 `plan/3-month-roadmap.md`，涵盖：

- 计算机网络与协议栈、抓包与分析（Wireshark）、常见协议安全（HTTP/TLS/DNS/SSH）
- 操作系统与脚本（Linux/Windows、Shell/Python）、端口与服务枚举（Nmap）
- 漏洞扫描与基线、安全加固、防火墙、日志与可观测性、SIEM 基础
- Web 安全（OWASP Top 10）、身份认证与会话安全、API 安全
- 密码学与 PKI、证书与 TLS、哈希与对称/非对称加密
- 渗透测试方法论（信息收集/攻击面/验证/报告）、内网与横向基础
- 云与容器安全概览、合规与风险、威胁建模、事件响应与取证基础
- CTF 入门与综合实战、复盘与沉淀（报告与作品集）

## 贡献

欢迎以 PR 的形式补充更多实验脚本、学习资料索引与题库。
