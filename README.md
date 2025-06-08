# 🏀 NBA Stats CLI App

A modular, microservice-based command-line application that lets you explore NBA player statistics across multiple seasons. Built using Python and ZeroMQ, this app supports player lookups, stat comparisons, and top scorer rankings. Includes a launcher for one-click startup and supports scraping fresh data via the NBA Stats API.

---

## 📦 Features

- 🧠 Interactive CLI interface with menu selection
- 🔌 Microservices architecture with ZeroMQ
- 📊 View individual player stats or top 5 leaders in any category
- 🔄 On-demand scraping with NBA Stats API
- 🛠 Optional `.exe` launcher to start all services and UI at once

---

## 🚀 Getting Started

### 🔧 Requirements

- Python 3.10+
- Install dependencies:
  ```bash
  pip install pyzmq pandas requests
  ```

---

## ▶️ How to Run

### ✅ Option 1: One-Click Launcher

From the project root:

```bash
python run_all.py
```

Or double-click `run_all.exe` if you’ve built it.

---

### 🧪 Option 2: Manual Run (for debugging)

Open separate terminals and run:

```bash
python team_options.py
python player_options.py
python user_function.py
python top_five_players.py
python NBA_web_scrape.py     # Optional: scrape new data
python nba_UI.py             # Main CLI interface
```

---

## 🗃 Project Structure

```
├── run_all.py               # Launcher: starts all services and UI
├── nba_UI.py                # CLI interface
├── choose_player_ui.py      # Manual player selector
├── NBA_web_scrape.py        # Scrapes data from NBA.com
├── nba_stats_data.json      # JSON file with player stats
│
├── team_options.py          # Microservice: returns season/team/type options
├── player_options.py        # Microservice: returns players by team
├── user_function.py         # Microservice: returns menu options
├── top_five_players.py      # Microservice: calculates top 5 by stat
├── player_stats.py          # [Legacy] detailed player stat handler
```

---

## 🧠 How It Works

Each microservice listens on a ZeroMQ port:

- `team_options.py` → `tcp://*:9755`
- `player_options.py` → `tcp://*:9756`
- `user_function.py` → `tcp://*:5558`
- `top_five_players.py` → `tcp://*:5559`

The CLI (`nba_UI.py`) coordinates between them by sending/receiving messages to gather data and present options.

---

## 📌 Known Warnings

If you build the app with PyInstaller, you may see some non-critical warnings like:

- `missing module named 'org.python'`
- `missing module named 'posix'`

These are platform-specific and safe to ignore (see `warn-run_all.txt`).

---

## 📷 Screenshot (Optional)

Add a screenshot of your CLI menu here if desired:

```
assets/screenshot.png
```

---

## 👨‍💻 Author

**Brian Spier**  
[github.com/Bspier](https://github.com/Bspier)

_"Dig deep. Build smarter."_ 🐇

---

## 💡 Future Plans

- Convert CLI into a Flask/React web app
- Add visual graphs and player/team comparisons
- Dockerize services for cloud deployment
- Implement unit testing with pytest
