# Trae Obsidian 自动记笔记 Skill（note-taker）

一个用于 Trae / Claude Code 环境的技能：当你输入“把上述内容记录在笔记中 / 记笔记 / 将上述内容记在笔记中”等指令时，会把当前对话整理成 Markdown 并保存到你的 Obsidian 笔记库里。

## 项目命名

- **中文名**：Trae Obsidian 自动记笔记 Skill
- **英文名**：note-taker
- **推荐 GitHub 仓库名**：`trae-note-taker`（全小写 + 连字符）

## 功能特性

- 自动把“上述对话/内容”整理为结构化 Markdown（含摘要、详情、行动项）
- 默认保存到 `D:\desktop\学习\obsidian\Note\项目\<项目名>\`（若首次记录会自动创建目录）
- 支持用户显式指定保存路径（例如“记到 D:\MyNotes\TestProject 下”）
- 兼容 Windows 中文路径，脚本输出使用 UTF-8，便于定位保存路径与排错

## 目录结构

```
.
├─ note-taker/
│  ├─ SKILL.md
│  ├─ evals.json
│  └─ scripts/
│     └─ save_note.py
└─ README.md
```

## 安装与启用

### 方式一：直接复制到全局 skills 目录（Windows）

把本仓库的 `note-taker/` 目录复制到：

`C:\Users\<你的用户名>\.trae\skills\note-taker`

确保目录中至少包含：

- `SKILL.md`
- `scripts/save_note.py`

### 方式二：从本地开发目录同步

如果你在本地修改了 skill 文件，确保同步覆盖到全局目录（示例）：

```powershell
Copy-Item -Path ".\note-taker\SKILL.md" -Destination "$env:USERPROFILE\.trae\skills\note-taker\SKILL.md" -Force
Copy-Item -Path ".\note-taker\scripts\save_note.py" -Destination "$env:USERPROFILE\.trae\skills\note-taker\scripts\save_note.py" -Force
Copy-Item -Path ".\note-taker\evals.json" -Destination "$env:USERPROFILE\.trae\skills\note-taker\evals.json" -Force
```

## 使用方法

在对话中直接输入类似指令即可触发：

- “把上述内容记录在笔记中”
- “记笔记”
- “将上述内容记在笔记中”
- “把这段对话存为笔记”

### 默认保存位置

默认保存到：

`D:\desktop\学习\obsidian\Note\项目\<项目名>\`

其中 `<项目名>` 默认取当前工作目录的文件夹名（例如工作目录为 `D:\desktop\研究生资料\自动记笔记`，则项目名为 `自动记笔记`）。

### 指定保存位置

如果你在指令里明确提到路径，skill 会优先保存到该路径，例如：

“把这段记到 D:\MyNotes\TestProject 下”

## 自检（可选）

你可以直接运行脚本做一次保存验证（会打印保存目录与最终文件路径）：

```powershell
python ".\note-taker\scripts\save_note.py" --content "# hello\n\n测试" --project "自动记笔记"
```

成功时输出包含：

- `SUCCESS: Note saved successfully to: ...`
- `PATH: ...`

## 常见问题

### 1) 没有保存到默认 Obsidian 目录？

请看脚本输出的 `DEBUG: Target Directory:` 与 `ERROR/WARNING` 行。若默认目录不可写或创建失败，脚本会回退到当前目录下的 `notes/` 以避免笔记丢失。

### 2) 中文乱码或路径显示异常？

脚本已将 stdout/stderr 强制设置为 UTF-8。若你仍遇到乱码，建议在 PowerShell 里使用 UTF-8 编码输出环境，并确保你传入的内容是 UTF-8。

## 版本与发布

如需打包分发，可以把 `note-taker/` 作为一个独立目录发布，或通过压缩包进行分发。
