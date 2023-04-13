import os
import re
import openpyxl

# Define the patterns to search for
patterns = [
    {"name": "Steam ID", "regex": "STEAM_[0-9]+:[0-9]+:[0-9]+", "risk": 2},
    {"name": "HTTP server call", "regex": "http\\.(Post|Fetch)", "risk": 4},
    {"name": "Dynamic code execution", "regex": "(CompileString|RunString)", "risk": 2},
    {"name": "Ban management function", "regex": "(removeip|removeid|banip|writeid)", "risk": 2},
    {"name": "File system operation", "regex": "file\\.(Read|Delete)", "risk": 1},
    {"name": "Obfuscated/encrypted code", "regex": "(0[xX][0-9a-fA-F]+|\\\\[0-9]+\\\\[0-9]+|\\\\[xX][0-9a-fA-F][0-9a-fA-F])", "risk": 3},
    {"name": "Miscellaneous Lua function", "regex": "(getfenv|_G\\[)", "risk": 1},
    {"name": "Client-side HTTP request", "regex": "http\\.Fetch", "risk": 4},
    {"name": "Server-side HTTP request", "regex": "http\\.Post", "risk": 5},
    {"name": "Shell command execution", "regex": "os\\.execute", "risk": 5},
    {"name": "Windows API call", "regex": "system\\.Windows", "risk": 5},
    {"name": "Loadstring call", "regex": "loadstring", "risk": 3},
    {"name": "Backdoor function", "regex": "(backdoor|executeserver|executeclient|clientcommand|serverside|clientside|virus|trojan)", "risk": 5},
    {"name": "Binary data in Lua code", "regex": "[\\x00-\\x08\\x0B-\\x0C\\x0E-\\x1F\\x7F-\\xFF]", "risk": 4},
    {"name": "IP address in Lua code", "regex": "\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}", "risk": 2},
    {"name": "Eval call", "regex": "eval", "risk": 3},
    {"name": "Metatable manipulation", "regex": "getmetatable\\(\\w+\\)\\.__newindex", "risk": 3},
    {"name": "CVar manipulation", "regex": "cvars\\.AddChangeCallback", "risk": 2},
    {"name": "Garbage collection control", "regex": "gcinfo|collectgarbage", "risk": 3},
    {"name": "Websocket connection", "regex": "WebSocket\\(", "risk": 4},
    {"name": "TCP/UDP socket connection", "regex": "(net\\.(TCP|UDP)|Socket)", "risk": 4},
    {"name": "System function call", "regex": "(system\\.(open|exec)|os\\.execute)", "risk": 5},
    {"name": "Windows Registry access", "regex": "(registry\\.(OpenKey|QueryValue)|winapi\\.RegOpenKey)", "risk": 5},
    {"name": "Encryption/decryption function", "regex": "(crypt\\.(encrypt|decrypt)|openssl)", "risk": 4},
    {"name": "Debug library function", "regex": "(debug\\.(getinfo|getupvalue)|__debug)", "risk": 3},
    {"name": "File I/O function", "regex": "(io\\.(open|popen)|file\\.(Read|Write))", "risk": 2},
    {"name": "Serialized data", "regex": "loadstring\\(string\\.dump\\(", "risk": 3},
    {"name": "Lua bytecode", "regex": "\\x1B\\x4C\\x75\\x61", "risk": 4},
    {"name": "Custom net message", "regex": "net\\.Receive\\(\\s*[\"'](\\w+)[\"']", "risk": 3},
    {"name": "DLL function call", "regex": "ffi\\.C\\.(\\w+)", "risk": 5},
    {"name": "Manipulation of environment variables", "regex": "(os\\.setenv|os\\.unsetenv)", "risk": 2},
    {"name": "External file download", "regex": "http\\.Fetch.+file%.(Write|Flush)", "risk": 5},

]

# Define the path to the GMod addons folder
gmod_addons_path = r"C:\Users\raghu\Downloads\zeros_methlab02_1.1.2"

# Create a new Excel workbook
workbook = openpyxl.Workbook()

# Add a new sheet to the workbook
sheet = workbook.active
sheet.title = "Backdoor Results"
sheet.append(["Filepath", "Pattern Name", "Risk", "Line Number", "Line Content"])

# Search for patterns in all Lua files in the GMod addons folder
for root, dirs, files in os.walk(gmod_addons_path):
    for file in files:
        if file.endswith(".lua"):
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                for pattern in patterns:
                    matches = re.findall(pattern["regex"], content)
                    if matches:
                        lines = content.split("\n")
                        for i, line in enumerate(lines):
                            for match in re.findall(pattern["regex"], line):
                                sheet.append([filepath, pattern["name"], pattern["risk"], i+1, line])

# Save the workbook to a file
workbook.save("backdoor_results.xlsx")
