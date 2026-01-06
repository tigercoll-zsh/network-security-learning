import os
import requests
import json
from PIL import Image, ImageDraw, ImageFont
from wordcloud import WordCloud


def _load_dotenv(dotenv_path: str = ".env") -> None:
    """轻量加载 .env（仅支持 KEY=VALUE / 可选引号），不引入第三方依赖。

    - 已存在的环境变量不覆盖（避免 CI/系统变量被意外替换）
    - 忽略空行与以 # 开头的注释行
    """

    if not os.path.exists(dotenv_path):
        return

    try:
        with open(dotenv_path, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                if not key:
                    continue
                if os.getenv(key) is None:
                    os.environ[key] = val
    except Exception:
        # .env 加载失败不应阻断主流程（之后会有密钥缺失的显式报错）
        return

# 可选：自动加载项目根目录 .env（Windows 下尤其实用）
_load_dotenv(".env")

# 配置微信公众号的接口信息（建议通过环境变量注入，避免密钥入库）
APP_ID = os.getenv("WECHAT_APP_ID", "").strip()
APP_SECRET = os.getenv("WECHAT_APP_SECRET", "").strip()
ACCESS_TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token"
UPLOAD_IMAGE_URL = "https://api.weixin.qq.com/cgi-bin/media/upload"
DRAFT_ADD_URL = "https://api.weixin.qq.com/cgi-bin/draft/add"
ADD_MATERIAL_URL = "https://api.weixin.qq.com/cgi-bin/material/add_material"
DRAFT_GET_URL = "https://api.weixin.qq.com/cgi-bin/draft/get"

# 获取微信公众号的 Access Token
def get_access_token(app_id, app_secret):
    response = requests.get(ACCESS_TOKEN_URL, params={
        "grant_type": "client_credential",
        "appid": app_id,
        "secret": app_secret
    })
    data = response.json()
    if "access_token" in data:
        return data["access_token"]
    else:
        raise Exception(f"获取 Access Token 失败: {data}")

# 自动查询图片路径
def find_image(directory, extensions=(".jpg", ".png")):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(extensions):
                return os.path.join(root, file)
    raise FileNotFoundError("未找到符合条件的图片文件")

# 上传图片到微信公众号素材库
def upload_image(access_token, image_path):
    with open(image_path, "rb") as image_file:
        files = {"media": image_file}
        response = requests.post(UPLOAD_IMAGE_URL, params={
            "access_token": access_token,
            "type": "image"
        }, files=files)
    data = response.json()
    if "media_id" in data:
        return data["media_id"]
    else:
        raise Exception(f"上传图片失败: {data}")

# 更新图片上传逻辑为永久素材上传接口
def upload_permanent_image(access_token, image_path):
    with open(image_path, "rb") as image_file:
        files = {"media": image_file}
        response = requests.post(ADD_MATERIAL_URL, params={
            "access_token": access_token,
            "type": "image"
        }, files=files)
    data = response.json()
    if "media_id" in data:
        return data["media_id"]
    else:
        raise Exception(f"上传永久图片失败: {data}")

import markdown2
import re

# 确保文件读取和写入使用 UTF-8 编码
def convert_markdown_to_html(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        md_content = file.read()

    # 关键句高亮语法：支持 ==高亮== （不影响原 Markdown，可在笔记里按需使用）
    # 先把标记替换成临时 HTML 标签，避免 markdown2 处理时丢失。
    md_content = re.sub(r"==(.+?)==", r"<mark>\\1</mark>", md_content)
    # 使用 markdown2 转换为简单 HTML
    html_content = markdown2.markdown(
        md_content,
        extras=[
            "fenced-code-blocks",
            "tables",
            "strike",
            "task_list",
            "break-on-newline",
        ],
    )

    # --- 微信兼容性关键修复 ---
    # 1) markdown2 在某些场景会输出 codehilite + span 的“高亮 HTML”。公众号端可能过滤 class/span，
    #    如果我们全局删除 <span>，会误伤非代码内容或破坏结构，造成“代码块缺行/缺内容”。
    #    这里改为：只把 codehilite 块降级为安全的 <pre><code>，并仅在该块内移除 span。
    def _downgrade_codehilite(m: re.Match) -> str:
        inner = m.group(1)
        inner = re.sub(r"<span[^>]*>", "", inner)
        inner = inner.replace("</span>", "")
        # markdown2 可能在 pre 里放 <code> 或不放，这里统一包成 <pre><code>
        inner = inner.replace("<pre>", "").replace("</pre>", "")
        inner = inner.replace("<code>", "").replace("</code>", "")
        return "<pre><code>" + inner + "</code></pre>"

    html_content = re.sub(
        r'<div class="codehilite">\s*([\s\S]*?)\s*</div>',
        _downgrade_codehilite,
        html_content,
    )

    # 2) <mark> 在公众号里经常被样式重置；用更安全的 <span> 来承载高亮样式。
    html_content = html_content.replace("<mark>", "<span>").replace("</mark>", "</span>")

    # ========= 手机端排版：稳字当头（尽量走“微信不会抽风”的属性） =========
    # 公众号有时会重置默认样式（p/ul/ol/pre 等），仅靠 inline 替换仍可能出现“手机端像没适配”。
    # 这里注入一段极小的、作用域限定在 section 内的 reset（微信通常允许 style 标签，且比 class 更稳）。
    # 若个别账号/场景过滤 <style>，也不会影响：后面的 inline 仍然生效。
    wechat_reset_css = (
        "<style>"
        "section.wechat-article{max-width:100%;padding:0 12px;margin:0;box-sizing:border-box;}"
        "section.wechat-article *{box-sizing:border-box;}"
        "section.wechat-article p{margin:12px 0;line-height:1.9;font-size:14px;color:#333;}"
        "section.wechat-article ul,section.wechat-article ol{margin:10px 0;padding-left:0;list-style:none;}"
        "section.wechat-article li{margin:8px 0;line-height:1.75;font-size:13.5px;color:#333;padding-left:14px;text-indent:-14px;}"
        "section.wechat-article img{max-width:100%;height:auto;display:block;margin:12px auto;}"
        "section.wechat-article table{border-collapse:collapse;width:100%;}"
        # 移动端适配：pre 允许换行，避免窄屏时整段看起来被“压成一行”；同时保留横向滚动作为兜底。
        "section.wechat-article pre{white-space:pre-wrap;word-break:break-word;overflow-wrap:anywhere;overflow-x:auto;-webkit-overflow-scrolling:touch;}"
        "section.wechat-article pre code{white-space:inherit;}"
        "section.wechat-article code{font-family:Consolas,'Courier New',monospace;}"
        "</style>"
    )

    wrapper_prefix = (
        wechat_reset_css
        + '<section class="wechat-article" style="font-size: 14px; color: #333; line-height: 1.8; '
        'word-break: break-word; overflow-wrap: anywhere;">'
    )
    wrapper_suffix = "</section>"

    # 标题/段落/分割线
    html_content = html_content.replace(
        "<h1>",
        '<h1 style="font-size: 18px; font-weight: 800; color: #111; margin: 18px 0 14px; line-height: 1.35; text-align: center;">',
    )
    html_content = html_content.replace(
        "<h2>",
        '<h2 style="font-size: 16px; font-weight: 800; color: #111; margin: 20px 0 10px; line-height: 1.4; padding-left: 10px; border-left: 4px solid #1976d2;">',
    )
    html_content = html_content.replace(
        "<h3>",
        '<h3 style="font-size: 15px; font-weight: 800; color: #111; margin: 16px 0 8px; line-height: 1.45; padding-left: 10px; border-left: 4px solid #2e7d32;">',
    )
    html_content = html_content.replace(
        "<p>",
        '<p style="margin: 12px 0; line-height: 1.9; font-size: 14px; color: #333; text-align: left; letter-spacing: 0.2px; word-spacing: 0.2px;">',
    )
    html_content = html_content.replace(
        "<hr />",
        '<hr style="border: none; border-top: 1px solid #eaecef; margin: 20px 0;" />',
    )
    html_content = html_content.replace(
        "<hr>",
        '<hr style="border: none; border-top: 1px solid #eaecef; margin: 20px 0;" />',
    )

    # 高亮条：渲染为安全的 span（避免公众号对 mark 的默认样式重置）
    html_content = html_content.replace(
        "<span>",
        '<span style="background: #fff3cd; color: #5d4037; padding: 2px 4px; border-radius: 4px;">',
    )

    # --- 伪列表修复：把段落内用 <br /> + '-' 形成的“假列表”转成真正的 <ul><li> ---
    # 例：markdown2 + break-on-newline 可能生成：
    # <p>xxx<br />
    # - a<br />
    # - b</p>
    # 微信里会原样显示 '-'，观感很差。这里仅处理“同一段落内出现 2 行及以上的 - 项”，避免误伤正文。
    def _convert_pseudo_list_paragraphs(html: str) -> str:
        def _p_repl(m: re.Match) -> str:
            body = m.group(1)
            # 统一换行，便于解析
            normalized = re.sub(r"<br\s*/?>", "\n", body, flags=re.I)
            lines = [re.sub(r"\s+", " ", ln).strip() for ln in normalized.split("\n")]
            lines = [ln for ln in lines if ln]

            # 收集以 '-' 开头的行
            items = []
            non_item_lines = []
            for ln in lines:
                if re.match(r"^[-•·]\s+", ln):
                    items.append(re.sub(r"^[-•·]\s+", "", ln))
                else:
                    non_item_lines.append(ln)

            # 至少 2 个条目才认为是“列表段落”（Day001 的伪列表基本都是这种）
            if len(items) < 2:
                return m.group(0)

            # 如果段落里混有非条目行（比如标题 + 列表），保守处理：只在纯列表段落时转换。
            # 这样可以避免把正常解释性文字打散。
            if non_item_lines:
                return m.group(0)

            lis = "".join(
                f'<li style="margin: 6px 0; line-height: 1.7; font-size: 13.5px; color: #333;">{it}</li>'
                for it in items
            )
            return (
                '<ul style="margin: 10px 0; padding-left: 20px;">'
                + lis
                + "</ul>"
            )

        # 仅处理不包含 <ul>/<ol>/<li> 的段落（避免二次处理或嵌套破坏）
        return re.sub(
            r"<p>((?:(?!</p>)[\s\S])*?)</p>",
            lambda m: m.group(0)
            if re.search(r"<(?:ul|ol|li)\b", m.group(1), flags=re.I)
            else _p_repl(m),
            html,
        )

    # 用户需求：不自动把 Markdown 中的 '-' 转成列表（保持原文/原结构）。
    # 如需再次开启该“伪列表修复”，可在运行前设置环境变量：WECHAT_CONVERT_PSEUDO_LIST=1
    if os.getenv("WECHAT_CONVERT_PSEUDO_LIST", "").strip() == "1":
        html_content = _convert_pseudo_list_paragraphs(html_content)

    # 列表：彻底去掉项目符号（无圆点、无 '-'），改成“干净缩进 + 行间距”的文本列表
    ul_plain_style = (
        '<ul style="margin: 10px 0; padding-left: 0; list-style: none;">'
    )

    html_content = html_content.replace(
        "<ul>",
        ul_plain_style,
    )
    html_content = html_content.replace(
        "<ol>",
        '<ol style="margin: 10px 0; padding-left: 20px;">',
    )
    html_content = html_content.replace(
        "<li>",
        '<li style="margin: 8px 0; line-height: 1.75; font-size: 13.5px; color: #333; padding-left: 14px; text-indent: -14px;">',
    )

    # “学习目标”希望视觉上更像“学习内容”那样的模块：给列表加一个浅底卡片容器 + 更稳的列表样式。
    goals_ul_open = ul_plain_style
    goals_card_open = (
        '<div style="margin: 10px 0 14px; padding: 10px 12px; border: 1px solid #e5e7eb; '
        'background: #f7f9fb; border-radius: 8px;">'
    )
    html_content = html_content.replace(
        'border-left: 4px solid #1976d2;">学习目标</h2>\n\n' + goals_ul_open,
        'border-left: 4px solid #1976d2;">学习目标</h2>\n\n'
        + goals_card_open
        + '<ul style="margin: 0; padding-left: 0; list-style: none;">',
    )

    # 只关闭“学习目标”这一段的 ul（避免误把开头日期/周次或其它列表提前闭合，导致公众号渲染截断）
    html_content = re.sub(
        r'(学习目标</h2>\n\n<div[^>]*>\s*<ul[^>]*>[\s\S]*?</ul>)',
        lambda m: m.group(1) + "</div>",
        html_content,
        count=1,
    )

    # --- 特定内容增强：把“OSI 与 TCP/IP 映射对照表”的 ASCII 表转为真表格 ---
    # Day001 当前用 ``` 包了 ASCII 对照表，公众号端只能当代码块；这里识别该段并输出 HTML table。
    def _render_mapping_table() -> str:
        rows = [
            ("OSI 七层", "TCP/IP 四层", "协议示例", "数据单位"),
            ("应用层 / 表示层 / 会话层", "应用层", "HTTP、FTP、DNS、SMTP、SSH、Telnet", "数据"),
            ("传输层", "传输层", "TCP、UDP", "段/数据报"),
            ("网络层", "网络层", "IP、ICMP、ARP", "数据包"),
            ("数据链路层 / 物理层", "网络接口层", "以太网、Wi‑Fi", "帧/比特"),
        ]

        # 复用你现有的表格横滑样式
        out = []
        out.append(
            '<div style="overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 12px 0;">'
            '<table style="border-collapse: collapse; width: 100%; min-width: 420px; font-size: 13px; border: 1px solid #e5e7eb;">'
        )
        # header
        out.append("<thead><tr>")
        for h in rows[0]:
            out.append(
                '<th style="border: 1px solid #e5e7eb; padding: 8px; background: #f3f4f6; color: #111; text-align: left; font-weight: 700;">'
                + h
                + "</th>"
            )
        out.append("</tr></thead><tbody>")
        for r in rows[1:]:
            out.append("<tr>")
            for c in r:
                out.append('<td style="border: 1px solid #e5e7eb; padding: 8px;">' + c + "</td>")
            out.append("</tr>")
        out.append("</tbody></table></div>")
        return "".join(out)

    # 识别：标题后紧跟的 code block（ASCII 表）
    mapping_title = (
        '<h3 style="font-size: 15px; font-weight: 800; color: #111; margin: 16px 0 8px; line-height: 1.45; '
        'padding-left: 10px; border-left: 4px solid #2e7d32;">📊 OSI 与 TCP/IP 映射对照表</h3>'
    )
    if mapping_title in html_content:
        # 用一个比较保守的正则：抓住紧随其后的第一段 <pre ...>...</pre>
        html_content = re.sub(
            re.escape(mapping_title) + r"\s*<pre[\s\S]*?</pre>",
            mapping_title + _render_mapping_table(),
            html_content,
            count=1,
        )
    # markdown2 常见格式： </li>\n<ul> / </li>\n<ol>
    html_content = html_content.replace(
        '</li>\n<ul style="margin: 10px 0; padding-left: 20px;">',
        '</li>\n<ul style="margin: 8px 0; padding-left: 18px;">',
    )
    html_content = html_content.replace(
        '</li>\n<ol style="margin: 10px 0; padding-left: 20px;">',
        '</li>\n<ol style="margin: 8px 0; padding-left: 18px;">',
    )

    # 强调
    html_content = html_content.replace(
        "<strong>",
        '<strong style="font-weight: 700; color: #d32f2f;">',
    )
    html_content = html_content.replace(
        "<em>",
        '<em style="font-style: italic; color: #6a1b9a;">',
    )

    # 代码块：必须先处理 pre，避免后续行内 code 替换把代码块弄坏
    # 公众号可能剥离/不应用 <style>，因此对代码块的关键样式使用 inline 强兜底。
    # 目标：手机端不要被“挤成一行”，允许换行，同时保留横向滚动作为兜底。
    pre_open = (
        '<pre style="background: #0b1020; color: #e6edf3; padding: 12px 12px; border-radius: 10px; '
        'border: 1px solid rgba(255,255,255,0.10); box-shadow: 0 2px 10px rgba(0,0,0,0.10); '
        # 代码块移动端策略：默认保留空白与换行；遇到超宽内容可横滑。避免 break-word 造成“字被劈开”。
        'white-space: pre-wrap; word-break: normal; overflow-wrap: anywhere; '
        'overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 12px 0;">'
    )
    html_content = html_content.replace(
        "<pre><code>",
        pre_open
        + '<code style="font-family: Consolas, \'Courier New\', monospace; font-size: 12.5px; line-height: 1.7; white-space: inherit;">',
    )

    # 代码块内容清理：pre/code 内不应出现 <br />（会导致等宽图/编号对齐被破坏）
    # 例如 Day001 的“本地网络示意图”末尾可能被插入 <br />。
    def _strip_br_in_pre(m: re.Match) -> str:
        inner = m.group(1)
        inner = re.sub(r"<br\s*/?>", "", inner, flags=re.I)
        return "<pre" + m.group(0).split("<pre", 1)[1].split(">", 1)[0] + ">" + inner + "</pre>"

    # 更稳的写法：只在 <pre ...>...</pre> 内部移除 <br>，不影响外部段落的换行策略
    html_content = re.sub(
        r"(<pre[\s\S]*?>[\s\S]*?</pre>)",
        lambda mm: re.sub(r"<br\s*/?>", "", mm.group(1), flags=re.I),
        html_content,
    )

    # 行内 code：保护 pre 区块，避免二次替换
    inline_code_tag = (
        '<code style="background-color: #f6f8fa; padding: 2px 4px; border-radius: 4px; '
        'font-family: Consolas, \'Courier New\', monospace; font-size: 12px; color: #b71c1c;">'
    )
    token_open = "__WECHAT_PRE_OPEN__"
    token_close = "__WECHAT_PRE_CLOSE__"
    html_content = html_content.replace(pre_open, token_open + pre_open)
    html_content = html_content.replace("</pre>", "</pre>" + token_close)

    segments = html_content.split(token_open)
    rebuilt = segments[0].replace("<code>", inline_code_tag)
    for seg in segments[1:]:
        if token_close in seg:
            in_pre, rest = seg.split(token_close, 1)
            # pre 内不替换行内 code
            rebuilt += token_open + in_pre + token_close
            rebuilt += rest.replace("<code>", inline_code_tag)
        else:
            rebuilt += token_open + seg
    html_content = rebuilt.replace(token_open, "").replace(token_close, "")

    # 链接：下划线+颜色，且靠容器的 overflow-wrap 兜底长 URL
    html_content = html_content.replace(
        "<a ",
        '<a style="color: #1976d2; text-decoration: underline;" ',
    )

    # 引用：更像公众号原生引用块（并收紧内部段落 margin）
    # 引用块升级为“卡片”：默认信息卡，并对常见关键词做颜色区分（纯字符串替换，尽量不引入复杂解析）
    quote_style = (
        'margin: 14px 0; padding: 10px 12px; border-left: 4px solid #90a4ae; '
        'background: #f7f9fb; color: #444; border-radius: 8px;'
    )
    html_content = html_content.replace(
        "<blockquote>",
        f'<blockquote style="{quote_style}">',
    )
    html_content = html_content.replace(
        f'<blockquote style="{quote_style}"><p style="margin: 10px 0; line-height: 1.85; font-size: 14px; color: #333; text-align: left; letter-spacing: 0.2px; word-spacing: 0.2px;">',
        f'<blockquote style="{quote_style}"><p style="margin: 6px 0; line-height: 1.75; font-size: 14px; color: #444; text-align: left;">',
    )

    # 关键词卡片：提示/注意/警告/结论（适配 markdown2 常见输出：blockquote 内第一段以加粗开头）
    html_content = html_content.replace(
        f'<blockquote style="{quote_style}"><p style="margin: 6px 0; line-height: 1.75; font-size: 14px; color: #444; text-align: left;"><strong style="font-weight: 700; color: #d32f2f;">提示：</strong>',
        '<blockquote style="margin: 14px 0; padding: 10px 12px; border-left: 4px solid #1976d2; background: #eef6ff; color: #0d47a1; border-radius: 8px;"><p style="margin: 6px 0; line-height: 1.75; font-size: 14px; color: #0d47a1; text-align: left;"><strong style="font-weight: 800; color: #0d47a1;">提示：</strong>',
    )
    html_content = html_content.replace(
        f'<blockquote style="{quote_style}"><p style="margin: 6px 0; line-height: 1.75; font-size: 14px; color: #444; text-align: left;"><strong style="font-weight: 700; color: #d32f2f;">注意：</strong>',
        '<blockquote style="margin: 14px 0; padding: 10px 12px; border-left: 4px solid #f57c00; background: #fff4e5; color: #e65100; border-radius: 8px;"><p style="margin: 6px 0; line-height: 1.75; font-size: 14px; color: #e65100; text-align: left;"><strong style="font-weight: 800; color: #e65100;">注意：</strong>',
    )
    html_content = html_content.replace(
        f'<blockquote style="{quote_style}"><p style="margin: 6px 0; line-height: 1.75; font-size: 14px; color: #444; text-align: left;"><strong style="font-weight: 700; color: #d32f2f;">警告：</strong>',
        '<blockquote style="margin: 14px 0; padding: 10px 12px; border-left: 4px solid #d32f2f; background: #ffebee; color: #b71c1c; border-radius: 8px;"><p style="margin: 6px 0; line-height: 1.75; font-size: 14px; color: #b71c1c; text-align: left;"><strong style="font-weight: 800; color: #b71c1c;">警告：</strong>',
    )
    html_content = html_content.replace(
        f'<blockquote style="{quote_style}"><p style="margin: 6px 0; line-height: 1.75; font-size: 14px; color: #444; text-align: left;"><strong style="font-weight: 700; color: #d32f2f;">结论：</strong>',
        '<blockquote style="margin: 14px 0; padding: 10px 12px; border-left: 4px solid #2e7d32; background: #e8f5e9; color: #1b5e20; border-radius: 8px;"><p style="margin: 6px 0; line-height: 1.75; font-size: 14px; color: #1b5e20; text-align: left;"><strong style="font-weight: 800; color: #1b5e20;">结论：</strong>',
    )

    # 表格：横向滚动兜底 + min-width 更保守
    # 注意：不能全局把 </table> 替换成 </table></div>，否则会误伤我们在映射表里手写的 table（它本身已带外层 div），
    # 造成多余 </div>，微信端可能直接截断后续内容。
    html_content = re.sub(
        r"<table>([\s\S]*?)</table>",
        r'<div style="overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 12px 0; border: 1px solid #e5e7eb; border-radius: 10px;">'
        r'<table style="border-collapse: collapse; width: 100%; min-width: 360px; table-layout: auto; font-size: 12.5px; border: 0;">\1</table></div>',
        html_content,
    )
    html_content = html_content.replace(
        "<th>",
        '<th style="border: 1px solid #e5e7eb; padding: 7px 8px; background: #f3f4f6; color: #111; text-align: left; font-weight: 800; white-space: nowrap;">',
    )
    html_content = html_content.replace(
        "<td>",
        '<td style="border: 1px solid #e5e7eb; padding: 7px 8px; vertical-align: top; word-break: break-word; overflow-wrap: anywhere;">',
    )

    # 图片：居中 + 圆角 + 如果被包在 <p> 内，兜底改为居中段落
    html_content = html_content.replace(
        "<img ",
        '<img style="max-width: 100%; height: auto; display: block; margin: 12px auto; border-radius: 8px;" ',
    )
    html_content = html_content.replace(
        '<p style="margin: 10px 0; line-height: 1.85; font-size: 14px; color: #333; text-align: left; letter-spacing: 0.2px; word-spacing: 0.2px;"><img style=',
        '<p style="margin: 12px 0; line-height: 1.6; text-align: center;"><img style=',
    )

    # 最后包裹容器
    html_content = wrapper_prefix + html_content + wrapper_suffix
    return html_content

# 确保 API 请求的 Content-Type 和编码正确
headers = {"Content-Type": "application/json; charset=utf-8"}

# 替换文章上传逻辑为草稿箱接口
def add_draft(access_token, title, content, media_id, digest):
    payload = {
        "articles": [
            {
                "title": title,
                "thumb_media_id": media_id,
                "author": "网络安全学习",
                "digest": digest,
                "show_cover_pic": 1,
                "content": content,
                "content_source_url": "",
            }
        ]
    }
    response = requests.post(DRAFT_ADD_URL, params={"access_token": access_token}, headers=headers, data=json.dumps(payload, ensure_ascii=False).encode("utf-8"))
    return response.json()

# 添加获取草稿详情的逻辑
def get_draft(access_token, media_id):
    response = requests.post(DRAFT_GET_URL, params={"access_token": access_token}, json={"media_id": media_id})
    data = response.json()
    if "news_item" in data:
        return data["news_item"]
    else:
        raise Exception(f"获取草稿详情失败: {data}")

# 添加自动生成图片的逻辑
def generate_placeholder_image(output_path, text="Placeholder", size=(800, 600)):
    # 创建一个白色背景的图片
    image = Image.new("RGB", size, "white")
    draw = ImageDraw.Draw(image)

    # 设置字体和文本位置
    try:
        font = ImageFont.truetype("arial.ttf", 40)  # 确保系统中有 Arial 字体
    except IOError:
        font = ImageFont.load_default()
    text_width, text_height = draw.textsize(text, font=font)
    text_position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)

    # 绘制文本
    draw.text(text_position, text, fill="black", font=font)

    # 保存图片
    image.save(output_path)
    print(f"生成占位图片: {output_path}")

# 根据内容智能生成图片
def generate_image_from_content(content, output_path):
    # 使用词云生成图片
    wordcloud = WordCloud(width=800, height=600, background_color="white").generate(content)
    # 确保输出路径正确
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    wordcloud.to_file(output_path)
    print(f"智能生成图片: {output_path}")

# 优化文章格式以适配微信公众号
def format_content_for_wechat(content):
    # 示例：将 Markdown 转换为更适合微信公众号的 HTML
    formatted_content = content.replace("\n", "<br>")  # 替换换行符为 <br>
    formatted_content = formatted_content.replace("**", "<b>").replace("**", "</b>")  # 替换加粗语法
    return formatted_content

def reupload_draft(access_token, title, content, media_id):
    headers = {"Content-Type": "application/json"}
    payload = {
        "articles": [
            {
                "title": title,
                "thumb_media_id": media_id,
                "author": "网络安全学习",
                "digest": "重新上传的文章摘要",
                "show_cover_pic": 1,
                "content": content,
                "content_source_url": "",
            }
        ]
    }
    response = requests.post(DRAFT_ADD_URL, params={"access_token": access_token}, headers=headers, data=json.dumps(payload))
    return response.json()

# 修复标题长度调整逻辑，确保按字符数截断（微信限制约 50 字符）
def adjust_title_length(title, max_length=50):
    if len(title) > max_length:
        return title[:max_length - 3] + "..."
    return title

# 主函数
def main():
    try:
        if not APP_ID or not APP_SECRET:
            raise Exception(
                "缺少公众号密钥：请设置环境变量 WECHAT_APP_ID / WECHAT_APP_SECRET（可参考项目根目录 .env.example）"
            )
        # 获取 Access Token
        access_token = get_access_token(APP_ID, APP_SECRET)
        print("Access Token 获取成功！")

        # 先转换 Day001.md 为 HTML
        html_content = convert_markdown_to_html("daily/Day001.md")
        print("转换后的 HTML 内容预览:", html_content[:500])  # 打印前 500 字符
        # 生成本地预览文件（可用浏览器/手机打开快速看排版）
        try:
            with open("preview.html", "w", encoding="utf-8") as f:
                f.write("<!doctype html><html><head><meta charset='utf-8'>")
                f.write("<meta name='viewport' content='width=device-width, initial-scale=1'>")
                f.write("<title>WeChat Preview</title></head><body>")
                f.write(html_content)
                f.write("</body></html>")
            print("已生成本地预览: preview.html")
        except Exception as _:
            pass
        formatted_content = html_content  # 直接使用 HTML
        print("Markdown 转换为微信公众号 HTML 成功！")

        # 总是根据文章内容生成图片
        print("根据文章内容生成图片。")
        # 使用纯文本内容生成图片
        with open("daily/Day001.md", "r", encoding="utf-8") as file:
            text_content = file.read()
        image_path = "d:/projects/Network Security/daily/images/generated_content_image.png"
        generate_image_from_content(text_content, image_path)
        print(f"生成图片文件: {image_path}")

        # 上传缩略图并获取 media_id
        media_id = upload_permanent_image(access_token, image_path)
        print(f"永久缩略图上传成功，media_id: {media_id}")

        # 从文章中提取标题和摘要
        with open("daily/Day001.md", "r", encoding="utf-8") as file:
            lines = file.readlines()
        title = ""
        digest = ""
        content_lines = []
        for line in lines:
            line = line.strip()
            if line.startswith('#') and not title:
                title = line[1:].strip()
            elif line and not line.startswith('#') and len(content_lines) < 3:
                content_lines.append(line)
        if not title:
            title = "网络安全学习"
        title = adjust_title_length(title)
        digest = " ".join(content_lines)[:120] if content_lines else "网络安全学习摘要"
        print(f"生成的标题: {title}")
        print(f"生成的摘要: {digest}")

        # 上传文章到草稿箱
        result = add_draft(access_token, title, formatted_content, media_id, digest)
        print("草稿箱上传结果:", result)

        if 'media_id' in result:
            print("上传成功！草稿 media_id:", result['media_id'])
            # 立刻拉取草稿内容，验证是否“上传完整”（而不是客户端显示/过滤导致）
            try:
                news_items = get_draft(access_token, result["media_id"])
                content_remote = (news_items[0] or {}).get("content", "") if news_items else ""
                print("草稿 content 长度(远端):", len(content_remote))
                print("草稿 content 长度(本地):", len(formatted_content))
                # 微信可能会对 content 做二次包装/转义，直接用纯中文标题匹配可能不可靠。
                # 这里输出远端前后片段并落盘，方便你在本地直接对比。
                try:
                    with open("debug_draft_remote.html", "w", encoding="utf-8") as f:
                        f.write(content_remote)
                    with open("debug_draft_local.html", "w", encoding="utf-8") as f:
                        f.write(formatted_content)
                    print("已保存对比文件: debug_draft_remote.html / debug_draft_local.html")
                except Exception:
                    pass

                print("远端 content 前 400:", content_remote[:400])
                print("远端 content 后 400:", content_remote[-400:])
                # 用更稳的结构特征检测：是否存在我们统一注入的 wechat-article section
                for k in [
                    "wechat-article",
                    "<h2",
                    "<h3",
                    "<pre",
                    "<table",
                ]:
                    print(f"结构片段[{k}] 远端={'YES' if k in content_remote else 'NO'} / 本地={'YES' if k in formatted_content else 'NO'}")
            except Exception as e:
                print("草稿回读验证失败:", e)

            return  # 成功则退出

        # 如果失败，尝试重新上传
        print("第一次上传失败，尝试重新上传。")
        # 调用重新上传草稿的逻辑
        retry_title = adjust_title_length(title + " (重新上传)")
        print(f"修正后的标题: {retry_title}")  # 调试标题长度调整逻辑
        try:
            reupload_result = reupload_draft(access_token, retry_title, formatted_content, media_id)
            print("重新上传草稿结果:", reupload_result)

            # 调试 media_id 问题
            print("草稿箱上传返回的完整数据:", reupload_result)

            # 验证 media_id 是否有效
            if 'media_id' in reupload_result:
                print(f"生成的 media_id: {reupload_result['media_id']}")
            else:
                print("草稿箱上传未返回有效的 media_id")
        except Exception as e:
            print("重新上传草稿时发生错误:", e)

        # 根据内容智能生成图片
        try:
            image_path = find_image("d:/projects/Network Security/daily/images")
        except FileNotFoundError:
            print("未找到图片，智能生成图片。")
            image_path = "d:/projects/Network Security/daily/images/generated_image.png"
            generate_image_from_content(formatted_content, image_path)
    except Exception as e:
        print("发生错误:", e)

if __name__ == "__main__":
    main()