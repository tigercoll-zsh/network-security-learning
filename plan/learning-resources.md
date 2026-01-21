# 学习资源汇总

本文档汇总网络安全学习过程中的常用资源，包括文档、工具、在线课程等。

---

## 官方文档与标准

### 网络协议
- [RFC Editor](https://www.rfc-editor.org/) - 互联网协议官方标准
- [TCP/IP Illustrated](https://en.wikipedia.org/wiki/TCP/IP_Illustrated) - 经典教材
- [Wireshark Wiki](https://wiki.wireshark.org/) - Wireshark 官方文档

### 加密与证书
- [OpenSSL Documentation](https://www.openssl.org/docs/) - OpenSSL 官方文档
- [Let's Encrypt](https://letsencrypt.org/docs/) - 免费 SSL 证书
- [TLS 1.3 RFC 8446](https://datatracker.ietf.org/doc/html/rfc8446) - TLS 1.3 规范

### Web 安全
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - OWASP 十大 Web 漏洞
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/) - Web 安全测试指南
- [CWE (Common Weakness Enumeration)](https://cwe.mitre.org/) - 通用弱点枚举
- [CVE Database](https://nvd.nist.gov/) - 国家漏洞数据库

### 合规与标准
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks) - 安全基线标准
- [NIST 800-53](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final) - 安全控制标准
- [ISO 27001](https://www.iso.org/standard/27001) - 信息安全管理体系

---

## 推荐书籍

### 入门级
1. **《计算机网络：自顶向下方法》** - Kurose & Ross
   - 网络协议入门经典教材
   - 适合初学者

2. **《Linux 权威指南》**
   - Linux 操作系统基础
   - 涵盖系统管理和安全

3. **《Python 编程：从入门到实践》**
   - Python 编程入门
   - 适合编写安全工具脚本

### 进阶级
1. **《Web 安全深度剖析》** - 吴翰清
   - Web 安全深入讲解
   - 涵盖常见漏洞与防护

2. **《Python 黑帽子：黑客与渗透测试编程之道》**
   - Python 在安全领域的应用
   - 实战性强

3. **《Metasploit 渗透测试魔鬼训练营》**
   - Metasploit 框架深入学习
   - 实战案例丰富

### 高级
1. **《TCP/IP 详解 卷1: 协议》**
   - 网络协议底层原理
   - 适合深入理解

2. **《恶意代码分析实战》**
   - 恶意软件分析方法
   - 逆向工程基础

3. **《网络防御与安全监控》**
   - 防御体系建设
   - 蓝队视角

---

## 在线课程与平台

### 免费资源
- [Coursera - Cybersecurity Specialization](https://www.coursera.org/specializations/cyber-security) - 网络安全专项课程
- [edX - Introduction to Cybersecurity](https://www.edx.org/learn/cybersecurity) - 网络安全入门
- [Cybrary](https://www.cybrary.it/) - 网络安全免费课程库
- [Hacker101](https://www.hacker101.com/) - 漏洞赏金平台（学习用）
- [PortSwigger Web Security Academy](https://portswigger.net/web-security) - Web 安全实战教程

### 中文资源
- [MOOC 网 - 网络安全课程](https://www.icourse163.org/) - 中国大学 MOOC
- [B 站 - 网络安全教程](https://www.bilibili.com/) - 搜索"网络安全""渗透测试"
- [看雪学院](https://bbs.kanxue.com/) - 软件安全论坛
- [FreeBuf](https://www.freebuf.com/) - 网络安全资讯

### 付费平台（仅供参考）
- [Udemy - Web Hacking & Penetration Testing](https://www.udemy.com/)
- [Pluralsight](https://www.pluralsight.com/)
- [SANS](https://www.sans.org/) - 企业级培训

---

## 工具资源

### 网络与抓包
- [Wireshark](https://www.wireshark.org/download.html) - 网络协议分析器
- [Nmap](https://nmap.org/download.html) - 网络扫描器
- [Tcpdump](https://www.tcpdump.org/) - 命令行抓包工具

### Web 安全
- [Burp Suite Community](https://portswigger.net/burp/communitydownload) - Web 应用安全测试工具
- [OWASP ZAP](https://www.zaproxy.org/download/) - 免费开源 Web 应用扫描器
- [SQLMap](http://sqlmap.org/) - 自动化 SQL 注入工具（学习用）

### 渗透测试（仅授权环境）
- [Kali Linux](https://www.kali.org/get-kali/) - 渗透测试专用发行版
- [Metasploit Framework](https://www.metasploit.com/) - 漏洞利用框架
- [John the Ripper](https://www.openwall.com/john/) - 密码破解工具

### 防御与监控
- [OSSEC](https://ossec.github.io/) - 开源 HIDS
- [Snort](https://www.snort.org/) - 开源 IDS/IPS
- [Wazuh](https://wazuh.com/) - 安全监控平台

### 日志与 SIEM
- [Elastic Stack (ELK)](https://www.elastic.co/elastic-stack/) - 日志收集与分析
- [Splunk Free](https://www.splunk.com/en_us/download.html) - 商业 SIEM（免费版）
- [Graylog](https://www.graylog.org/) - 开源日志管理

---

## 靶场与实验环境

### 本地靶场
- [DVWA](http://www.dvwa.co.uk/) - Damn Vulnerable Web Application
- [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) - OWASP Top 10 靶场
- [Metasploitable2](https://sourceforge.net/projects/metasploitable/) - 漏洞测试 Linux 虚拟机
- [VulnHub](https://www.vulnhub.com/) - 虚拟机靶场集合

### 在线靶场
- [TryHackMe](https://tryhackme.com/) - 适合初学者的在线靶场
- [Hack The Box](https://www.hackthebox.com/) - 进阶靶场
- [PortSwigger Labs](https://portswigger.net/web-security) - Web 安全实验室

**重要提示**: 所有靶场学习应遵循平台规则，仅对平台提供的目标进行实验。

---

## 认证路径（可选）

### 入门级
- **CompTIA Security+** - 网络安全入门认证
- **ISC2 CC** - Cybersecurity 认证
- **CISSP Associate** - 信息安全师（经验不足可先考取 Associate）

### 中级
- **CEH (Certified Ethical Hacker)** - 道德黑客认证
- **OSCP (Offensive Security Certified Professional)** - 实战渗透测试认证
- **GIAC Security Essentials (GSEC)** - 安全基础知识

### 高级
- **CISSP** - 信息安全专业人员认证
- **CISM** - 信息安全管理师
- **OSCE** - 高级渗透测试认证

**注意**: 认证不是必须的，但可以作为学习的里程碑。建议先完成学习内容再考虑认证。

---

## 社区与资讯

### 中文社区
- [FreeBuf](https://www.freebuf.com/) - 网络安全资讯
- [安全客](https://www.anquanke.com/) - 安全资讯与漏洞分析
- [看雪论坛](https://bbs.kanxue.com/) - 软件安全技术
- [先知社区](https://xz.aliyun.com/) - 阿里云安全社区

### 国际社区
- [Reddit r/netsec](https://www.reddit.com/r/netsec/) - 网络安全讨论
- [Twitter Infosec Community](https://twitter.com/) - 关注 #infosec 标签
- [Packet Storm](https://packetstormsecurity.com/) - 安全工具与公告

### 漏洞资讯
- [CVE Details](https://www.cvedetails.com/) - CVE 数据库
- [NIST NVD](https://nvd.nist.gov/) - 国家漏洞数据库
- [Exploit-DB](https://www.exploit-db.com/) - 漏洞利用数据库（仅供学习）

---

## 实用脚本与代码库

### Python 安全工具
- [Scapy](https://scapy.net/) - 网络包操作库
- [Requests](https://requests.readthedocs.io/) - HTTP 请求库
- [Paramiko](https://www.paramiko.org/) - SSH 库

### 自动化框架
- [Ansible](https://www.ansible.com/) - 基础设施自动化
- [Terraform](https://www.terraform.io/) - 基础设施即代码

### 代码审计
- [Bandit](https://bandit.readthedocs.io/) - Python 安全检查工具
- [Semgrep](https://semgrep.dev/) - 静态代码分析

---

## 学习建议

1. **理论 + 实践结合**
   - 先理解原理，再动手实验
   - 每个知识点至少做一次验证

2. **记录学习过程**
   - 每天记录笔记和截图
   - 整理成个人知识库

3. **跟随社区动态**
   - 关注安全资讯和漏洞公告
   - 参与讨论和分享

4. **建立实验环境**
   - 搭建自己的靶场
   - 练习常用工具

5. **遵守法律道德**
   - 所有实验在授权范围内
   - 不得用于非法目的

---

## 更新记录

- 2026-01-20: 初始版本创建
