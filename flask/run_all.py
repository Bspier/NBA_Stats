import subprocess
import time
import os
import sys

# Get the folder where this script is running
base_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
scripts = [
    "team_options.py",
    "player_options.py",
    "user_function.py",
    "top_five_players.py",
    "NBA_web_scrape.py",  # Optional
    "nba_UI.py"  # CLI interface (runs last)
]

processes = []

for script in scripts[:-1]:  # Start background services
    script_path = os.path.join(base_dir, script)
    print(f"Starting: {script_path}")
    p = subprocess.Popen(["python", script_path])
    processes.append((script, p))
    time.sleep(1)

# Launch UI script in foreground
ui_path = os.path.join(base_dir, scripts[-1])
print("\nLaunching main interface...")
subprocess.call(["python", ui_path])