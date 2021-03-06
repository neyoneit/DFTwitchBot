import re
import os
from env import environ

DF_EXE_P = environ["DF_EXE_P"]
DF_DIR = environ['DF_DIR']
CFG_NAME = environ['CFG_NAME']
CFG_P = os.path.join(DF_DIR, CFG_NAME)
DUMP_NAME = "condump.txt"
DUMP_P = os.path.join(DF_DIR, DUMP_NAME)
WS_ADDRESS = environ['WS_ADDRESS']

STATE_REPORT_P = os.path.join(DF_DIR, "system", "reports", environ["SVINFO_REPORT_NAME"])
INITIAL_REPORT_P = os.path.join(DF_DIR, "system", "reports", "initialstate.txt")

BINDS = None
BLACKLISTED_WORDS = []

with open("src/blacklist.txt", "r") as word_file:
    list_of_lists = []
    for line in word_file:
        stripped_line = line.strip()
        BLACKLISTED_WORDS.append(stripped_line)


def get_bind(cmd):
    global BINDS

    return BINDS[cmd]


def get_bind_fuzzy(rx, raw=False):
    global BINDS

    if not raw:
        rx = "^.*" + re.escape(rx) + ".*$"

    for cmd, bind in BINDS.items():
        if re.search(rx, cmd):
            return bind

    raise RuntimeError("Could not find bind for " + rx)


def read_cfg():
    global BINDS
    BINDS = {}

    with open(CFG_P, "r") as cfg_f:
        cfg = cfg_f.readlines()

    for line in cfg:
        try:
            r = r"bind[ ]+?(.+?)[ ]+?\"(.+?)\""
            match = re.match(r, line)
            key = match.group(1)
            cmd = match.group(2)
            BINDS[cmd] = key
        except:
            continue

    validate_cfg()


def validate_cfg():
    global BINDS

    # Replace all binds with their proper equivalents, if necessary
    BINDS["toggleconsole"] = 29

    for (cmd, bind) in BINDS.items():
        if cmd == "toggleconsole":
            continue
        elif re.match(r"^F\d+$", bind):
            BINDS[cmd] = "{" + bind + "}"
        elif bind == "ENTER":
            BINDS[cmd] = "{Enter}"
        elif bind == "ESCAPE":
            BINDS[cmd] = "{Esc}"
        elif bind == "TAB":
            BINDS[cmd] = "{Tab}"
        else:
            pass
