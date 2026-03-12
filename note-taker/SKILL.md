---
name: note-taker
description: Records the current conversation context into a Markdown note. It saves to a specific Obsidian directory by default or a user-specified location, creating project folders as needed.
---

# Note Taker

## Description
This skill triggers when the user asks to record the current conversation or "above content" into a note. It formats the conversation history into a structured Markdown file and saves it using a helper script.

## Triggering
- "将上述内容记在笔记中" (Record the above content in notes)
- "记笔记" (Take a note)
- "把这段对话存为笔记" (Save this conversation as a note)
- "Create a note for this"
- "Document this discussion"

## Behavior

1.  **Identify Content**: Capture the key points, code snippets, decisions, and reasoning from the recent conversation history. The note should be self-contained and easy to read.
2.  **Format Note**:
    - Create a Markdown string.
    - **Title**: Use a concise summary of the topic or the current date/time.
    - **Frontmatter**:
        ```yaml
        ---
        date: <YYYY-MM-DD>
        project: <ProjectName>
        tags: [note, <ProjectName>]
        ---
        ```
    - **Content**: Summary, Details, Action Items.
3.  **Execute Script**:
    - **Write to Temp File**:
        - Write the formatted markdown content to a temporary file (e.g., `temp_note.md`) using the `Write` tool.
    - **Run Script**:
        - Run the python script referencing this file: `python "scripts/save_note.py" --file "temp_note.md" --project "<ProjectName>"`.
        - **IMPORTANT**: If the user has specified a path, add `--path "<UserPath>"`.
        - **IMPORTANT**: Wait for the command to finish and **READ THE OUTPUT**.
    - **Cleanup**:
        - Delete the temporary file using `DeleteFile` after execution.
4.  **Confirmation**:
    - **Check Output**: Look for "SUCCESS: Note saved successfully to: ..." in the command output.
    - **Inform User**: Tell the user the exact path where the note was saved.
    - **Fallback**: If the script fails (check for "ERROR" in output), try to save manually to the current directory and inform the user of the failure reason.

## Instructions for the Model

- **Context Analysis**: Look at the `<user_input>` and the preceding conversation history.
- **Project Name**: Default to current directory name (`D:\desktop\研究生资料\自动记笔记` -> `自动记笔记`).
- **File Handling**:
    - Use `Write` to create a temporary file with the note content.
    - Run: `python "scripts/save_note.py" --file "temp_note.md"` (add `--path` if user specified one).
    - **MUST READ OUTPUT**: The script will print the saved path. Use this information in your final response.
    - Cleanup: `DeleteFile` "temp_note.md".
- **Troubleshooting**:
    - If the script fails to save to the default path (e.g. permission error), it will try to fallback to `./notes`. Check the output log!
    - If you see `UnicodeEncodeError`, the script has been updated to handle this, but ensure you are passing valid UTF-8 content.
