import os
import chardet

OUTPUT_FILE = "project_dump.txt"
IGNORE_DIRS = {'.git', '__pycache__', 'node_modules', '.venv', '.idea', '.vscode', 'dist', 'build', '.vscode'}
IGNORE_FILES = {'package-lock.json'}
TEXT_EXTENSIONS = {'.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.json', '.md', '.txt', '.yml', '.yaml', '.env'}

def is_text_file(filepath):
    _, ext = os.path.splitext(filepath)
    if ext.lower() in TEXT_EXTENSIONS:
        return True
    else:
        return False
    # try:
    #     with open(filepath, 'rb') as f:
    #         raw = f.read(2048)
    #     result = chardet.detect(raw)
    #     encoding = result.get('encoding')
    #     if not encoding:
    #         return False
    #     text = raw.decode(encoding)
    #     return True
    # except Exception:
    #     return False

def dump_directory(base_dir):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            rel_root = os.path.relpath(root, base_dir)
            out.write(f"\n# 📁 Directory: {rel_root}\n\n")

            for filename in files:
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, base_dir)

                out.write(f"## 📄 File: {rel_path}\n")
                try:
                    if is_text_file(filepath) and not (filename in IGNORE_FILES):
                        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                            out.write(f"```\n{content}\n```\n\n")
                    else:
                        size_kb = os.path.getsize(filepath) / 1024
                        out.write(f"[Binary file skipped: {size_kb:.1f} KB]\n\n")
                except Exception as e:
                    out.write(f"[Error reading file: {e}]\n\n")
    print(f"✅ Projeto salvo em {OUTPUT_FILE}")

if __name__ == "__main__":
    base = os.path.abspath(".")
    print(f"🔍 Varredura iniciada em: {base}")
    dump_directory(base)
