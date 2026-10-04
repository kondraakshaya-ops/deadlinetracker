# 🗓️ Deadline Tracker

A smart deadline management web app built with **Streamlit** and powered by **Google Gemini AI**. Stay organized, track your tasks, and never miss an important deadline again.

---

## ✨ Features

- 📝 **Add Deadlines** — Add tasks with subject, description, due date, and priority
- 📊 **Dashboard** — View total, pending, completed, and overdue tasks at a glance
- 📈 **Progress Bar** — Visual completion progress tracker
- 🔍 **Search & Filter** — Filter tasks by status and priority
- ✅ **Mark as Completed** — One-click task completion
- 🗑️ **Delete Tasks** — Remove tasks you no longer need
- 📲 **WhatsApp Reminders** — Send deadline reminders via WhatsApp to any number
- 🤖 **AI Powered** — Integrated with Google Gemini AI (`gemini-2.0-flash`)

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/kondraakshaya-ops/deadlinetracker.git
cd deadlinetracker
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
# or
source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Create a `.streamlit/secrets.toml` file:
```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

> Get your free API key at [Google AI Studio](https://aistudio.google.com/)

### 5. Run the app
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
deadlinetracker/
├── app.py              # Main Streamlit application
├── prompt.py           # AI prompt utilities
├── requirements.txt    # Python dependencies
├── .gitignore          # Files excluded from git
└── .streamlit/
    └── secrets.toml    # API keys (not pushed to GitHub)
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| [Streamlit](https://streamlit.io/) | Web app framework |
| [Google Gemini AI](https://ai.google.dev/) | AI integration |
| Python | Backend logic |
| WhatsApp API (wa.me) | Reminder sharing |

---

## ⚙️ Requirements

- Python 3.8+
- Gemini API Key (free at [aistudio.google.com](https://aistudio.google.com/))

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

Made with ❤️ by [kondraakshaya-ops](https://github.com/kondraakshaya-ops)
