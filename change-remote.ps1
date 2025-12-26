# ========================================
# Git 远程仓库迁移脚本
# ========================================

# 请先在 GitHub 创建新仓库，然后填写以下信息：
$newRepoName = "新仓库名"  # 替换为您的新仓库名
$username = "tigercoll-zsh"

# ========================================
# 方案选择（取消注释您需要的方案）
# ========================================

# 方案 1：完全迁移到新仓库
# git remote set-url origin "git@github.com:$username/$newRepoName.git"
# git push -u origin main

# 方案 2：添加备份仓库（保留原仓库）
# git remote add backup "git@github.com:$username/$newRepoName.git"
# git push -u backup main

# 方案 3：镜像推送到新仓库
# git push --mirror "git@github.com:$username/$newRepoName.git"

# ========================================
# 验证远程仓库配置
# ========================================
Write-Host "当前远程仓库配置：" -ForegroundColor Cyan
git remote -v

Write-Host "`n请编辑此脚本，填写新仓库名并取消注释相应的方案" -ForegroundColor Yellow
