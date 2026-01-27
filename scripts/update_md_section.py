import re
import sys
import os

def update_section(file_path, header, new_content):
    """
    Updates a section in a Markdown file identified by a specific header.

    Args:
        file_path (str): Path to the Markdown file.
        header (str): The header of the section to update (e.g., "## 🎯 学习目标").
        new_content (str): The new content to replace the existing section content.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return False
    except Exception as e:
        print(f"Error reading file: {e}")
        return False

    # Regex to find the section
    # Matches the header, followed by anything until the next header of the same level or higher, or EOF.
    # We assume headers start with #

    # Escape special characters in header just in case, but usually ## is fine
    escaped_header = re.escape(header)

    # Determine the level of the header (e.g., ## is level 2)
    header_level = len(header.split()[0])

    # Pattern explanation:
    # 1. The specific header we want to find (start of capture group 1)
    # 2. \n (newline after header)
    # 3. (.*?) (content - non-greedy match)
    # 4. (?=^#{1,header_level}\s|\Z) (Lookahead: stop at next header of same or higher level, or End of File)
    # flags=re.MULTILINE | re.DOTALL to handle newlines correctly

    pattern = rf"(^{escaped_header}\s*\n)(.*?)(?=^#{{1,{header_level}}}\s|\Z)"

    match = re.search(pattern, content, flags=re.MULTILINE | re.DOTALL)

    if not match:
        print(f"Warning: Section '{header}' not found in {file_path}. Appending to end or check header name.")
        # Optional: Append if not found? For now, let's just warn.
        # To be safe, we can try to find where it *should* be, but simple replacement is safer.
        return False

    # Perform replacement
    # We keep the header (group 1) and replace the content (group 2)
    updated_content = content[:match.start(2)] + new_content.strip() + "\n\n" + content[match.end(2):]

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"Successfully updated section '{header}' in {file_path}")
        return True
    except Exception as e:
        print(f"Error writing file: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python update_md_section.py <file_path> <header_text> <new_content_file_or_string>")
        print("Example: python update_md_section.py daily/Day022.md \"## 🎯 学习目标\" \"new_content.txt\"")
        sys.exit(1)

    f_path = sys.argv[1]
    head = sys.argv[2]
    content_arg = sys.argv[3]

    # Check if content_arg is a file path
    if os.path.isfile(content_arg):
        try:
            with open(content_arg, 'r', encoding='utf-8') as f:
                n_content = f.read()
        except:
            n_content = content_arg # Treat as string if read fails
    else:
        n_content = content_arg

    update_section(f_path, head, n_content)
