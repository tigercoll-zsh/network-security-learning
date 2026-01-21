"""
批量更新 Day013-Day090 文件，使其结构与 Day012 保持一致
"""
import os
import re
from pathlib import Path

# 标准模板结构（基于 Day012）
STANDARD_SECTIONS = [
    "## 学习目标",
    "## 学习内容", 
    "## 实践任务（合法授权范围内）",
    "## 巩固练习（题与复盘）",
    "## 评估标准（达成判定）",
    "## 学习成果达成情况（由学习者填写）",
    "### 截图与证据",
    "### 关键命令与输出（粘贴关键片段）",
    "### 结论与反思",
    "## 集中参考答案（含思路）",
    "## 学习成果示例填写（可照抄）",
]

def clean_title(title: str) -> str:
    """去除标题中的'傻瓜版能照做'等字样"""
    cleaned = re.sub(r'[（(]傻瓜版能照做[)）]', '', title)
    cleaned = re.sub(r'[（(]严格授权[)）]', '', cleaned)
    return cleaned.strip()

def ensure_section_exists(content: str, section: str, default_text: str = "") -> str:
    """确保指定章节存在，不存在则添加"""
    if section not in content:
        # 找到合适的插入位置（在上一个章节之后）
        return content + f"\n\n{section}\n\n{default_text}"
    return content

def add_missing_subsections(content: str) -> str:
    """补充缺失的子章节"""
    
    # 确保学习成果区有完整结构
    if "## 学习成果达成情况（由学习者填写）" in content:
        成果区_start = content.find("## 学习成果达成情况（由学习者填写）")
        成果区_end = content.find("## 集中参考答案", 成果区_start)
        if 成果区_end == -1:
            成果区_end = len(content)
        
        成果区 = content[成果区_start:成果区_end]
        
        # 补充缺失的子章节
        if "### 截图与证据" not in 成果区:
            insert_pos = content.find("\n\n", 成果区_start + len("## 学习成果达成情况（由学习者填写）")) 
            if insert_pos > 成果区_start:
                content = content[:insert_pos] + "\n\n### 截图与证据\n\n- [ ] 任务截图\n" + content[insert_pos:]
        
        if "### 关键命令与输出" not in 成果区:
            截图_pos = content.find("### 截图与证据", 成果区_start)
            if 截图_pos > 0:
                insert_pos = content.find("\n\n", 截图_pos + len("### 截图与证据"))
                if insert_pos > 截图_pos and insert_pos < 成果区_end:
                    content = content[:insert_pos] + "\n\n### 关键命令与输出（粘贴关键片段）\n\n- 命令：\n- 输出：\n" + content[insert_pos:]
        
        if "### 结论与反思" not in 成果区:
            命令_pos = content.find("### 关键命令与输出", 成果区_start)
            if 命令_pos > 0:
                insert_pos = content.find("\n\n", 命令_pos + len("### 关键命令与输出（粘贴关键片段）"))
                if insert_pos > 命令_pos and insert_pos < 成果区_end:
                    reflection_template = """
**我今天搞清楚了**：
- 

**我差点搞混的是**：
- 

**明天我要继续补的是**：
- 

**本次学习耗时**：约 ___ 小时

**掌握程度自评**：
- [ ] 😕 看懂了但没动手
- [ ] 🙂 跑通了基础任务
- [ ] 😃 完成了所有任务并理解原理
- [ ] 🤩 额外做了扩展实验
"""
                    content = content[:insert_pos] + f"\n\n### 结论与反思\n{reflection_template}" + content[insert_pos:]
    
    return content

def add_reference_answers_if_missing(content: str) -> str:
    """如果缺少参考答案章节，添加模板"""
    if "## 集中参考答案（含思路）" not in content:
        # 在评估标准或学习成果区之后添加
        insert_markers = [
            "## 学习成果达成情况（由学习者填写）",
            "## 评估标准（达成判定）",
        ]
        
        for marker in insert_markers:
            if marker in content:
                # 找到该章节的结束位置
                marker_pos = content.find(marker)
                next_section = content.find("\n## ", marker_pos + len(marker))
                
                if next_section == -1:  # 如果是最后一章
                    content += "\n\n## 集中参考答案（含思路）\n\n### 题 1 参考答案\n\n（待补充）\n"
                else:
                    content = content[:next_section] + "\n\n## 集中参考答案（含思路）\n\n### 题 1 参考答案\n\n（待补充）\n" + content[next_section:]
                break
    
    return content

def add_example_section_if_missing(content: str) -> str:
    """如果缺少示例填写章节，添加模板"""
    if "## 学习成果示例填写" not in content:
        # 在参考答案之后添加
        if "## 集中参考答案（含思路）" in content:
            答案_pos = content.find("## 集中参考答案（含思路）")
            next_section = content.find("\n## ", 答案_pos + len("## 集中参考答案（含思路）"))
            
            example_template = """

## 学习成果示例填写（可照抄）

> 可将"示例"内容替换为你自己的时间与截图文件名。

### 截图与证据（示例）

- 任务 1：`images/dayXXX_task1.png`

### 关键命令与输出（示例）

```
命令示例：
输出示例：
```

### 结论与反思（示例）

**我今天搞清楚了**：
- （示例）理解了核心概念

**我差点搞混的是**：
- （示例）某个易混淆点

**明天我要继续补的是**：
- （示例）下一步深入方向

**本次学习耗时**：约 2 小时

**掌握程度自评**：
- [x] 😃 完成了所有任务并理解原理
"""
            
            if next_section == -1:
                content += example_template
            else:
                content = content[:next_section] + example_template + content[next_section:]
    
    return content

def process_day_file(filepath: Path) -> bool:
    """处理单个 Day 文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 清理标题
        lines = content.split('\n')
        if lines and lines[0].startswith('# Day'):
            lines[0] = clean_title(lines[0])
        content = '\n'.join(lines)
        
        # 2. 补充缺失章节
        content = add_missing_subsections(content)
        content = add_reference_answers_if_missing(content)
        content = add_example_section_if_missing(content)
        
        # 3. 标准化评估标准格式
        if "## 评估标准（达成判定）" in content:
            # 确保使用复选框格式
            评估_start = content.find("## 评估标准（达成判定）")
            评估_end = content.find("\n## ", 评估_start + 1)
            if 评估_end == -1:
                评估_end = len(content)
            
            评估区 = content[评估_start:评估_end]
            # 将简单的 "- 你能..." 改为 "- ✅ 你能..."
            评估区 = re.sub(r'\n- 你能', r'\n- ✅ 你能', 评估区)
            评估区 = re.sub(r'\n- 能', r'\n- ✅ 能', 评估区)
            
            content = content[:评估_start] + 评估区 + content[评估_end:]
        
        # 只在内容有变化时写入
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"处理 {filepath.name} 时出错: {e}")
        return False

def main():
    """主函数"""
    daily_dir = Path(__file__).parent.parent / "daily"
    
    print("开始批量更新 Day013-Day090...")
    print("=" * 60)
    
    updated_count = 0
    skipped_count = 0
    
    for day_num in range(13, 91):
        day_file = daily_dir / f"Day{day_num:03d}.md"
        
        if not day_file.exists():
            print(f"⚠️  {day_file.name} 不存在，跳过")
            skipped_count += 1
            continue
        
        print(f"处理 {day_file.name}...", end=" ")
        
        if process_day_file(day_file):
            print("✅ 已更新")
            updated_count += 1
        else:
            print("⏭️  无需更新")
    
    print("=" * 60)
    print(f"完成！共更新 {updated_count} 个文件，跳过 {skipped_count} 个文件")
    print("\n建议：")
    print("1. 运行 git diff 检查变更内容")
    print("2. 手动检查几个示例文件确保格式正确")
    print("3. 针对内容过简的文件（如Day050）需要手动补充学习内容")

if __name__ == "__main__":
    main()
