motd = """
  ______     ______   ____ _           _      ____ _ _            _
 |  _ \\ \\   / /  _ \\ / ___| |__   __ _| |_   / ___| (_) ___ _ __ | |_
 | |_) \\ \\ / /| |_) | |   | '_ \\ / _` | __| | |   | | |/ _ \\ '_ \\| __|
 |  __/ \\ V / |  _ <| |___| | | | (_| | |_  | |___| | |  __/ | | | |_
 |_|     \\_/  |_| \\_\\\\____|_| |_|\\__,_|\\__|  \\____|_|_|\\___|_| |_|\\__|
"""

dataBaseFile = "./data/data.db"
dbInit = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS servers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    ip TEXT NOT NULL,
    port INTEGER NOT NULL
);
"""