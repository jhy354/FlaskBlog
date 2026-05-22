# My Blog

Flask 个人博客，支持文章发布与实验报告管理。

## 功能

- **文章** — Markdown/HTML 格式，分类归档
- **实验报告** — PDF 在线预览与下载，按课程分类
- **深色/浅色模式** — 跟随系统 / 手动切换，自动记忆
- **响应式** — 手机、平板、桌面自适应

## 本地运行

```bash
pip install flask
python app.py
```

打开 `http://localhost:5000` 即可。

## 发布文章

编辑 `posts.json` 添加元信息，在 `content/<id>.html` 中写正文。

## 上传报告

1. 将 PDF 放入 `static/reports/<课程名>/`
2. 在 `reports.json` 中添加对应条目
