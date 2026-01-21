# 实验环境搭建指南

本文档提供网络安全学习所需的基础实验环境搭建指南。所有实验应在合法授权的自建环境中进行。

---

## 硬件需求（最低配置）

- CPU: 4核心
- 内存: 16GB
- 磁盘: 200GB SSD
- 网络: 稳定的互联网连接

---

## 软件环境

### 1. 宿主机（Windows）

**必备软件**:
```
- VMware Workstation Pro / VirtualBox 7.x
- Wireshark 4.x
- Python 3.9+ (通过 python.org 安装)
- Git (通过 git-scm.com 安装)
- VS Code (可选，用于编辑)
- OpenSSL (Windows 版本或使用 WSL)
- Nmap (Windows 版本)
- Putty / SSH 客户端
```

**Python 环境设置**:
```powershell
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
.venv\Scripts\Activate.ps1

# 安装依赖
pip install ruff pillow wordcloud markdown2 requests
```

---

### 2. 虚拟机规划

#### 虚拟机 1: Kali Linux (攻击机/渗透测试学习)

**用途**: 学习渗透测试方法论、工具使用（仅限授权靶场）

**配置**:
- OS: Kali Linux 2024.x
- CPU: 2核
- 内存: 4GB
- 磁盘: 50GB
- 网络: NAT 或桥接（根据实验需求）

**关键软件**:
- Nmap (预装)
- Burp Suite Community
- Wireshark (预装)
- SQLMap (学习用途)
- Metasploit Framework (学习用途，仅授权环境)

**重要提示**: 
- 仅用于自建靶场或明确授权的目标
- 所有实验需记录授权文件
- 禁止对公网任何目标进行扫描

#### 虚拟机 2: Ubuntu Server (靶机/服务器)

**用途**: Web 服务、数据库、日志采集学习

**配置**:
- OS: Ubuntu 22.04 LTS Server
- CPU: 2核
- 内存: 2GB
- 磁盘: 30GB
- 网络: 桥接模式

**服务配置**:
```bash
# 安装常用服务
sudo apt update
sudo apt install nginx mysql-server php-fpm openssh-server

# Web 根目录
/var/www/html

# MySQL 配置路径
/etc/mysql/mysql.conf.d/mysqld.cnf
```

#### 虚拟机 3: Windows Server (Windows 安全学习)

**用途**: Windows 安全基线、事件查看器、AD 基础（可选）

**配置**:
- OS: Windows Server 2022 Evaluation
- CPU: 2核
- 内存: 4GB
- 磁盘: 60GB
- 网络: 桥接模式

**关键功能**:
- 事件查看器 (eventvwr.msc)
- 本地安全策略 (secpol.msc)
- PowerShell 脚本执行策略

---

## 网络拓扑（基础）

```
                    ┌─────────────────┐
                    │   宿主机       │
                    │  (Windows)     │
                    │  Wireshark     │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
        ┌─────▼────┐  ┌─────▼────┐  ┌─────▼────┐
        │ Kali     │  │ Ubuntu   │  │ Win Srv  │
        │ (NAT/桥) │  │ (桥接)   │  │ (桥接)   │
        └──────────┘  └──────────┘  └──────────┘
```

---

## 初始化检查清单

### Week 1 前完成

- [ ] 宿主机安装完成
- [ ] Python 环境配置完成
- [ ] 虚拟机软件安装完成
- [ ] 至少创建 1 台 Linux 虚拟机（Ubuntu 推荐）
- [ ] Wireshark 抓包验证（抓一次 ping 流量）
- [ ] 测试虚拟机网络连通性

### Week 3 前完成

- [ ] Kali Linux 虚拟机搭建完成（仅用于授权靶场）
- [ ] Nmap 安装并验证
- [ ] 测试虚拟机间网络通信
- [ ] 配置 SSH 密钥登录（Linux → Linux）

### Week 4 前完成

- [ ] Ubuntu Server 搭建 Web 服务 (Nginx)
- [ ] Ubuntu Server 搭建数据库
- [ ] Windows Server 虚拟机搭建（可选）
- [ ] 创建基础靶场环境（DVWA 或类似，仅学习用途）

---

## 常见问题

### 1. 虚拟机网络不通

**检查步骤**:
```powershell
# Windows 宿主机查看网络适配器
ipconfig

# 确认虚拟机网络模式
# - NAT: 可以上网，但宿主机无法直接访问
# - 桥接: 与宿主机同网段，可以互相访问
```

**解决方案**:
- 首选桥接模式，便于虚拟机间通信
- 如使用 NAT，需配置端口转发

### 2. Wireshark 抓不到虚拟机流量

**检查步骤**:
- 确认抓取的是正确的网卡（VirtualBox Host-Only Network 或 VMnet8）
- Windows 宿主机可能需要启用"混杂模式"

### 3. SSH 连接被拒绝

**检查步骤**:
```bash
# Ubuntu 检查 SSH 服务状态
sudo systemctl status ssh

# 检查防火墙
sudo ufw status

# 查看监听端口
sudo ss -tulnp | grep ssh
```

**解决方案**:
- 确保 SSH 服务运行中
- 防火墙允许 22 端口
- 检查 `/etc/ssh/sshd_config` 配置

### 4. Python 脚本无法运行

**检查步骤**:
```bash
# 检查 Python 版本
python --version

# 检查虚拟环境
which python

# 检查依赖
pip list
```

**解决方案**:
- 确保激活虚拟环境
- 安装缺失的依赖包

---

## 推荐靶场（学习用途，仅自建环境）

### DVWA (Damn Vulnerable Web Application)

**用途**: Web 漏洞学习（授权靶场）

**安装** (Ubuntu):
```bash
sudo apt install dvwa
# 或下载源码手动安装
```

**访问**: `http://<Ubuntu IP>/dvwa`

**注意**: 仅在本地环境使用，切勿暴露到公网

### OWASP Juice Shop

**用途**: OWASP Top 10 学习（授权靶场）

**安装**:
```bash
# 使用 Docker
docker run -d -p 3000:3000 bkimminich/juice-shop
```

---

## 安全提醒

1. **严禁对任何未授权目标进行扫描或攻击**
2. 所有实验应在隔离的网络环境进行
3. 使用靶场学习漏洞原理，而非用于非法目的
4. 定期备份实验环境和脚本
5. 遵循法律法规和道德准则

---

## 下一步

环境搭建完成后，即可开始 `Day001` 的学习。每日内容详见 `daily/DayXXX.md`。
