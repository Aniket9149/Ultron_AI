import os

html_page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ULTRON // MAINFRAME</title>
    <style>
        body {
            margin: 0; padding: 0; height: 100vh; 
            background: #010307; /* Ultron Dark Theme Base */
            overflow: hidden;
        }
    </style>
</head>
<body>
    <!-- Yeh page abhi bilkul blank hai. Next step mein yahan naya design aayega. -->
</body>
</html>"""

with open("ultron_mainframe.html", "w", encoding="utf-8") as f:
    f.write(html_page)

import subprocess
subprocess.Popen(["python", "run_app.py"])
