# 🚀 TODO MASTER - Quick Start Guide

## ⚡ Launch the App

### Windows Users
**Double-click** `run.bat` or run in terminal:
```bash
run.bat
```

### All Platforms
```bash
python -m todo_app.main
```

## 📝 Basic Workflow

### 1. Add Your First Task
```
Choose: 2 (Add New Task)
Title: Buy groceries
Description: Milk, eggs, bread
Priority: medium
Tags: shopping, personal
Due Date: (press Enter to skip)
Recurrence: none
```

### 2. View Your Tasks
```
Choose: 1 (View All Tasks)
```

You'll see a beautiful table with:
- Task ID
- Status (⏳ Pending / ✅ Done)
- Priority (🔴 HIGH / 🟡 MEDIUM / 🟢 LOW)
- Title
- Tags
- Due Date

### 3. Complete a Task
```
Choose: 5 (Complete Task)
Enter task ID: 1
```

### 4. Search Tasks
```
Choose: 6 (Search Tasks)
Enter keyword: groceries
```

### 5. Filter Tasks
```
Choose: 7 (Filter Tasks)
Select: 1 (Status)
Enter: pending
```

## 🎯 Pro Tips

### Priority Levels
- Use **high** for urgent tasks (shows as 🔴 HIGH)
- Use **medium** for normal tasks (shows as 🟡 MEDIUM)
- Use **low** for someday tasks (shows as 🟢 LOW)

### Tags
- Use tags to organize: `work, personal, urgent, meeting`
- Search and filter by tags later
- Separate multiple tags with commas

### Due Dates
- Format: `YYYY-MM-DD HH:MM`
- Example: `2025-12-31 17:00`
- Overdue tasks show in red with ⚠️

### Recurring Tasks
- **daily**: Perfect for habits and daily routines
- **weekly**: Good for weekly meetings
- **monthly**: For monthly bills or reviews
- When completed, a new instance is auto-created!

## 🎨 Understanding the Colors

| Color | Meaning |
|-------|---------|
| 🟢 Green | Success, completed, low priority |
| 🟡 Yellow | Pending, medium priority |
| 🔴 Red | High priority, overdue, errors |
| 🔵 Blue | Information, headers |
| 💜 Magenta | Special highlights |
| 🩵 Cyan | Menu borders, titles |

## ⚠️ Troubleshooting

### App won't start or shows errors?

1. **Check Python version:**
   ```bash
   python --version
   ```
   Must be 3.10 or higher!

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Use the right terminal:**
   - ✅ Windows Terminal (Windows)
   - ✅ Terminal.app (macOS)
   - ✅ GNOME Terminal, Konsole (Linux)
   - ❌ Old cmd.exe (Windows) - emojis may not work

### Can't input anything?

Make sure you're running in an **interactive terminal**, not:
- IDE output window
- Background process
- Redirected input/output

### Emojis showing as boxes or ???

Run `run.bat` on Windows to set UTF-8 encoding, or use Windows Terminal.

## 📚 Learn More

- See `README.md` for full documentation
- Check `.claude/skills/` for technical details
- View `specs/001-cli-todo-app/` for specifications

---

**Ready? Let's get productive! 🎉**
