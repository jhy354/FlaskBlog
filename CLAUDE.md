# Flask 个人博客 — 项目指南

## 运行

```bash
pip install flask
python app.py
# 访问 http://localhost:5000
```

## 项目结构

```
app.py              # Flask 主入口，定义所有路由
posts.json          # 文章元数据（id, title, summary, date, read_time）
reports.json        # 报告元数据（自动生成，按日期降序排列）
content/<id>.html   # 文章正文，与 posts.json 的 id 对应
static/
  css/style.css     # 全部样式（深色/浅色模式用 CSS 变量）
  js/main.js        # 主题切换、返回顶部、报告筛选
  reports/<课程>/   # PDF 文件，不提交到 Git（.gitignore 已排除）
templates/
  _head.html        # <head> 通用部分，含防闪烁内联脚本
  _navbar.html      # 顶部导航栏（首页/文章/报告）
  _footer.html      # 底部（只有一个 GitHub 链接）
  index.html        # 首页（最近 2 篇文章 + 最近 2 份报告）
  blog.html         # 全部文章列表
  post.html         # 文章详情
  reports.html      # 报告列表（按课程筛选）
  report.html       # 报告详情（PDF 嵌入预览）
  404.html          # 404 页面
CLAUDE.md           # 本文件
README.md           # 用户说明文档
```

## 关键约定

- 每个模板需传入 `now=datetime.now()`，否则 `_footer.html` 的年份渲染会出错
- 每个模板需传入 `nav_active`（`"home"` / `"blog"` / `"reports"` / `""`）导航栏高亮
- 文章正文在 `content/<id>.html` 中编写，纯 HTML，无需包裹 `<html><body>`
- 报告放入 `static/reports/<课程名>/`，然后运行命令自动更新 `reports.json`
- `reports.json` 按日期降序排列，由脚本从目录内容自动生成
- `app.py` 使用 `get_reports()` 每次请求重新读取 `reports.json`，修改后无需重启
- 深色模式防闪烁通过 `_head.html` 中的同步内联脚本实现（`defer` 不够早）
- FAB 按钮顺序：返回顶部 > 返回主页 > 主题切换（使用 `column-reverse` 实现）

## 发布新文章

1. 在 `content/` 下创建 `<id>.html` 写正文
2. 在 `posts.json` 中添加条目

## 上传报告

1. PDF 放入 `static/reports/<课程名>/`
2. 运行以下命令自动更新 `reports.json`：

```bash
python -c "
import os, json, time, re
entries = []
for c in ['大学物理学实验', '无机化学实验', '物理化学实验']:
    d = 'static/reports/' + c
    for f in sorted(os.listdir(d)):
        if not f.endswith('.pdf'): continue
        fp = os.path.join(d, f)
        t = time.strftime('%Y-%m-%d', time.localtime(os.path.getmtime(fp)))
        s = os.path.getsize(fp)
        ss = '%d KB' % (s//1024)
        title = re.sub(r'^2410314\s+蒋浩阳\s+', '', f.replace('.pdf', ''))
        entries.append({'title': title, 'course': c, 'filename': '%s/%s' % (c, f), 'date': t, 'size': ss, '_ts': os.path.getmtime(fp)})
entries.sort(key=lambda x: x['_ts'], reverse=True)
for i, e in enumerate(entries, 1): e['id'] = i; del e['_ts']
with open('reports.json', 'w', encoding='utf-8') as f:
    json.dump(entries, f, ensure_ascii=False, indent=4)
print('reports.json updated with %d entries' % len(entries))
"
```

## 主题系统

- 使用 `data-theme` 属性切换 `light` / `dark`
- 偏好存储在 `localStorage('blog-theme')`
- 首次访问根据 `prefers-color-scheme` 决定
- CSS 变量在 `:root` 和 `[data-theme="dark"]` 中定义

## Git 注意事项

- `static/reports/` 已加入 `.gitignore`，PDF 不会进入版本控制
- PDF 已从远程仓库删除（`git rm --cached` + push）
