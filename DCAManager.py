import tkinter as tk
import os
import time
import json
from tkinter import filedialog, simpledialog

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# DCAManager is a free, open-scorce project that allows you to manage your mods for any game. LICENSED UNDER THE CC BY-NC-SA 4.0. COPYRIGHT (C) 2026 VOTDOTVR. ALL RIGHTS RESERVED.
# ------------------------------------------------------------------------------

# Makeing the root window
root = tk.Tk()

root.title("DCA Manager")
root.geometry("800x600")
root.resizable(False, False)
root.configure(bg="#1e1e1e")

# Creating the main user interface
tk.Label(root, text="DCA Manager", font=("Arial", 30), bg="#1e1e1e", fg="White").place(x=10, y=10)

# ADD MOD BUTTON (wired to add_mod)
tk.Button(root, text="Add mod", bg="Gray", width=10, height=1, command=lambda: add_mod()).place(x=10, y=80)
tk.Button(root, text="Remove mod", bg="Gray", width=10, height=1, command=lambda: remove_mod()).place(x=10, y=110)
tk.Button(root, text="Toggle mod", bg="Gray", width=10, height=1, command=lambda: toggle_mod()).place(x=10, y=140)

# Creating the log window
log_box = tk.Text(root,
                  width=60,
                  height=20,
                  bg="#2B2B2B",
                  fg="white",
                  font=("Consolas", 12),
                  wrap="none")
log_box.pack(pady=70)

log_box.configure(state="disabled")

x_scroll = tk.Scrollbar(root, orient="horizontal", command=log_box.xview)
log_box.configure(xscrollcommand=x_scroll.set)

def log(message):
    log_box.configure(state="normal")
    log_box.insert("end", message + "\n")
    log_box.configure(state="disabled")
    log_box.see("end")

def display_mods():
    with open("mods.json", "r") as f:
        data = json.load(f)

    mods = data.get("mods", [])

    for mod in mods:
        name = mod.get("name", "Unknown Mod")
        path = mod.get("path", "No Path")
        pathgame = mod.get("pathgame", "No Game Path")
        tof = mod.get("enabled", "Unkown")

        log(f"{name}, Path:{path}, Game path:{pathgame}, Enabled:{tof}")

#ADD MOD
def add_mod():
    mod_path = filedialog.askopenfilename(title="Select Mod File")
    if not mod_path:
        return

    name = simpledialog.askstring("Mod Name", "Enter mod name:")
    if not name:
        return

    pathgame = filedialog.askdirectory(title="Select Game Folder")
    if not pathgame:
        return

    try:
        with open("mods.json", "r") as f:
            data = json.load(f)
    except:
        data = {"mods": []}

    data["mods"].append({
        "name": name,
        "path": mod_path,
        "pathgame": pathgame,
        "enabled": False
    })

    with open("mods.json", "w") as f:
        json.dump(data, f, indent=4)

    log(f"{name}, Path:{mod_path}, Game path:{pathgame}, Enabled:True")

def remove_mod():
    # Ask for the mod name to remove
    name = simpledialog.askstring("Remove Mod", "Enter mod name to remove:")
    if not name:
        return

    try:
        with open("mods.json", "r") as f:
            data = json.load(f)
    except:
        print("Error: mods.json not found.")
        return

    mods = data.get("mods", [])

    new_mods = [m for m in mods if m.get("name") != name]

    if len(new_mods) == len(mods):
        print(f"No mod named '{name}' found.")
        return

    data["mods"] = new_mods
    with open("mods.json", "w") as f:
        json.dump(data, f, indent=4)

    print(f"Removed mod: {name}")
    print("Restart the program to see the changes in the log window.")

def toggle_mod():
    name = simpledialog.askstring("Toggle Mod", "Enter mod name to toggle:")
    if not name:
        return

    try:
        with open("mods.json", "r") as f:
            data = json.load(f)
    except:
        print("mods.json missing")
        return

    mods = data.get("mods", [])
    disabled_folder = os.path.join(os.getcwd(), "disabledmods")
    if not os.path.exists(disabled_folder):
        os.makedirs(disabled_folder)

    found = False

    for mod in mods:
        if mod.get("name") == name:
            found = True
            current = mod.get("enabled", True)
            new_state = not current
            mod["enabled"] = new_state

            mod_path = mod.get("path")
            game_path = mod.get("pathgame")
            filename = os.path.basename(mod_path)

            game_mod_path = os.path.join(game_path, filename)
            disabled_mod_path = os.path.join(disabled_folder, filename)

            print("JSON path:", mod_path)
            print("Disabled path:", disabled_mod_path)
            print("Game path:", game_mod_path)

            try:
                if new_state:
                    print("Trying to enable...")
                    print("Exists in disabledmods:", os.path.exists(disabled_mod_path))
                    if os.path.exists(disabled_mod_path):
                        os.replace(disabled_mod_path, game_mod_path)
                        print(name, "enabled")
                    else:
                        print("File not found in disabledmods")
                else:
                    print("Trying to disable...")
                    print("Exists in game folder:", os.path.exists(game_mod_path))
                    if os.path.exists(game_mod_path):
                        os.replace(game_mod_path, disabled_mod_path)
                        print(name, "disabled")
                    else:
                        print("File not found in game folder")
            except Exception as e:
                print("move error:", e)

            break

    if not found:
        print("mod not found:", name)
        return

    with open("mods.json", "w") as f:
        json.dump(data, f, indent=4)



display_mods()

root.mainloop()