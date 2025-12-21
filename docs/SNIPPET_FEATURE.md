# Quick Reference: Code Snippet Display

## What Changed?

When you chat with ChatGit and receive code snippets, they now automatically show:

✅ **File Name** - Which file the code comes from
✅ **Line Numbers** - Exact line numbers from the actual file
✅ **Visual Header** - Pretty header with file emoji and clear formatting

## Example Output

When you ask: *"Show me the chat endpoint"*

**You'll see:**

```
**📁 api.py** · Lines 330-340
```

Then the code block with line numbers:
```
  330 | @app.post("/api/chat")
  331 | async def process_chat(payload: MessagePayload):
  332 |     if not session.search_index:
  333 |         raise HTTPException(status_code=400, detail="Repository not loaded")
  ...
```

## How to Use

1. **Load a repository** (paste GitHub URL in sidebar)
2. **Enable "Enhance Code Snippets"** checkbox (enabled by default)
3. **Ask coding questions** - code snippets will automatically include file info!

## Control

Toggle the feature on/off using the **"Enhance Code Snippets"** checkbox in the sidebar.

## Supported Files

Works with: Python, JavaScript, TypeScript, Java, C, C++

---

**Note**: The feature intelligently searches your loaded repository to find where each code snippet comes from, making it easy to locate the code in your actual files!
