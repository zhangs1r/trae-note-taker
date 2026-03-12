import os
import sys
import datetime
import argparse
import io

# 强制设置标准输出的编码为 utf-8，避免 Windows 下的乱码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def save_note(content, project_name=None, target_path=None):
    # 检测是否为 SSH 远程环境（简单的跨平台/盘符检测）
    # 在 Linux/Mac 上 os.name 是 'posix'，Windows 上是 'nt'
    is_remote_or_non_windows = False
    
    if os.name != 'nt':
        is_remote_or_non_windows = True
    
    # 默认基础路径
    DEFAULT_BASE_PATH = r"D:\desktop\学习\obsidian\Note\项目"
    
    # 如果检测到非 Windows 环境，或者 D 盘不存在（针对 Windows SSH 到另一台 Windows 但没有 D 盘的情况）
    if os.name == 'nt' and not os.path.exists("D:\\"):
         # 这种情况比较少见，但也算作无法访问默认路径
         pass 

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
        # 如果是远程环境（Linux/Mac），无法使用 Windows 的 D:\ 路径
        if is_remote_or_non_windows:
            print(f"WARNING: Detected non-Windows environment (os.name={os.name}). Cannot access local path '{DEFAULT_BASE_PATH}'.")
            print("WARNING: Falling back to current directory './notes'.")
            # 在远程环境下，默认保存在当前项目下的 notes 目录
            save_dir = os.path.join(os.getcwd(), "notes")
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
        try:
            os.makedirs(save_dir, exist_ok=True)
        except Exception as e2:
             print(f"ERROR: Failed to create fallback directory: {e2}")
             # 如果连后备目录都创建不了，直接打印内容让用户复制
             print("\n" + "="*20 + " NOTE CONTENT " + "="*20)
             print(content)
             print("="*54 + "\n")
             print("CRITICAL: Could not save file. Please copy the content above manually.")
             sys.exit(1)

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
        
        # 成功保存后的提示信息优化
        if is_remote_or_non_windows:
            print(f"SUCCESS: Note saved to REMOTE path: {file_path}")
            print("ATTENTION: You are in a remote environment. The file is on the REMOTE machine, NOT your local machine.")
            print("ACTION REQUIRED: You may need to manually download this file or copy the content.")
        else:
            print(f"SUCCESS: Note saved successfully to: {file_path}")
            
        print(f"PATH: {file_path}") # 专门输出一行供 regex 提取
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
        # Try reading from stdin if no arguments provided
        if not sys.stdin.isatty():
             # 指定 stdin 编码读取
             input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
             content = input_stream.read()
        else:
             print("ERROR: No content provided via --content, --file, or stdin.")
             sys.exit(1)

    save_note(content, args.project, args.path)
