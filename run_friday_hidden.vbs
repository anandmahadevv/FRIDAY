Set WshShell = CreateObject("WScript.Shell")

' Start the MCP server (Brain) hidden
WshShell.Run "cmd.exe /c set PYTHONUTF8=1 && cd /d c:\Users\anand\Downloads\friday && python -m uv run friday", 0, False

' Wait 5 seconds for the server to initialize
WScript.Sleep 5000

' Start the Voice Agent hidden
WshShell.Run "cmd.exe /c set PYTHONUTF8=1 && cd /d c:\Users\anand\Downloads\friday && python -m uv run friday_voice", 0, False
