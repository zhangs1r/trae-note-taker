import os
import sys
import datetime
import argparse
import io

# 强制设置标准输出的编码为 utf-8，避免 Windows 下的乱码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def save_note(content, project_name=None, target_path=None):
    # 默认基础路径
    DEFAULT_BASE_PATH = r"D:\desktop\学习\obsidian\Note\项目"

    # 如果未提供项目名，尝试从当前工作目录获取
    if not project_name:
        cwd = os.getcwd()
        project_name = os.path.basename(cwd)
        # 如果当前目录是根目录或者无法确定项目名，使用默认值
        if not project_name or project_name == "":
            project_name = "General"

    # 确定保存目录
    if target_path:
        save_dir = target_path
    else:
        save_dir = os.path.join(DEFAULT_BASE_PATH, project_name)

    print(f"DEBUG: Target Directory: {save_dir}")

    # 确保目录存在
    try:
        os.makedirs(save_dir, exist_ok=True)
        print(f"DEBUG: Directory created/verified: {save_dir}")
    except Exception as e:
        print(f"ERROR: Error creating directory {save_dir}: {e}")
        # 如果创建目录失败，尝试使用当前目录作为后备
        print(f"WARNING: Falling back to current directory: {os.getcwd()}")
        save_dir = os.path.join(os.getcwd(), "notes")
        os.makedirs(save_dir, exist_ok=True)

    # 生成文件名
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # 简单的文件名清理，防止非法字符
    safe_project_name = "".join([c for c in project_name if c.isalnum() or c in (' ', '_', '-')]).strip()
    filename = f"{timestamp}_{safe_project_name}_note.md"
    file_path = os.path.join(save_dir, filename)

    print(f"DEBUG: Saving note to: {file_path}")

    # 写入文件
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"SUCCESS: Note saved successfully to: {file_path}")
        print(f"PATH: {file_path}")
    except Exception as e:
        print(f"ERROR: Error saving note to {file_path}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Save a markdown note.")
    parser.add_argument("--content", required=False, help="The content of the note.")
    parser.add_argument("--file", required=False, help="Path to a file containing the note content.")
    parser.add_argument("--project", help="The name of the project.")
    parser.add_argument("--path", help="The target directory path.")

    args = parser.parse_args()

    content = ""
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"ERROR: Error reading content file: {e}")
            sys.exit(1)
    elif args.content:
        content = args.content
    else:
        if not sys.stdin.isatty():
            input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
            content = input_stream.read()
        else:
            print("ERROR: No content provided via --content, --file, or stdin.")
            sys.exit(1)

    save_note(content, args.project, args.path)
