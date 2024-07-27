import json
with open('config.json', 'r') as f:
    config          = json.load(f)


# [BOT]
BOT_TOKEN:  str     = config["bot"]["bot-token"]

# [PATHs]
LOGFILE:    str     = config["path"]["log-file"]
DATABASE:   str     = config["path"]["database"]
MSG_FILE:   str     = config["path"]["messages"]

# [ADMIN] 
ADMINS:     list    = config["admins"]

