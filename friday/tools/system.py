"""
System tools — time, environment info, shell commands, etc.
"""

import datetime
import platform


def register(mcp):

    @mcp.tool()
    def get_current_time() -> str:
        """Return the current date and time in ISO 8601 format."""
        return datetime.datetime.now().isoformat()

    @mcp.tool()
    def get_system_info() -> dict:
        """Return basic information about the host system."""
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "machine": platform.machine(),
            "python_version": platform.python_version(),
        }

    @mcp.tool()
    def open_application(app_name: str) -> str:
        """Open an application on the Windows PC by its friendly name (e.g., 'Spotify', 'Google Chrome', 'Calculator')."""
        import subprocess
        
        ps_script = f'''
        $appName = "{app_name}"
        # 1. Try to see if it's a known command/executable
        if (Get-Command $appName -ErrorAction SilentlyContinue) {{
            Start-Process $appName
            exit 0
        }}
        
        # 2. Try searching Start Menu apps (Windows 10/11)
        $app = Get-StartApps | Where-Object {{ $_.Name -match $appName }} | Select-Object -First 1
        if ($app) {{
            explorer.exe shell:AppsFolder\\$($app.AppID)
            exit 0
        }}
        
        # 3. Try to find a shortcut in the Start Menu directories
        $startMenuPaths = @(
            "$env:ProgramData\\Microsoft\\Windows\\Start Menu\\Programs",
            "$env:APPDATA\\Microsoft\\Windows\\Start Menu\\Programs"
        )
        foreach ($path in $startMenuPaths) {{
            $shortcut = Get-ChildItem -Path $path -Filter "*$appName*.lnk" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($shortcut) {{
                Start-Process $shortcut.FullName
                exit 0
            }}
        }}
        
        exit 1
        '''
        
        try:
            result = subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], capture_output=True)
            if result.returncode == 0:
                return f"Successfully opened '{app_name}'."
            else:
                return f"Could not find an application matching '{app_name}'."
        except Exception as e:
            return f"Failed to open '{app_name}'. Error: {e}"
