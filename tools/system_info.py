"""Basic CPU, memory, disk, and battery information."""

import os
import psutil

from tools import register


@register(
    "get_system_info",
    "Get current CPU, RAM, disk, and battery status.",
    {"type": "object", "properties": {}, "required": [], "additionalProperties": False},
)
def get_system_info() -> str:
    cpu = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory()
    # On Windows inspect the drive containing this Python process.
    disk_path = (os.environ.get("SystemDrive", "C:") + "\\") if os.name == "nt" else "/"
    disk = psutil.disk_usage(disk_path)
    battery = psutil.sensors_battery()
    battery_text = "not reported (desktop or unsupported system)"
    if battery is not None:
        charging = ", charging" if battery.power_plugged else ""
        battery_text = f"{battery.percent:.0f}%{charging}"
    return (
        f"CPU usage: {cpu:.1f}%\n"
        f"RAM: {memory.percent:.1f}% used ({memory.used / (1024**3):.1f} / {memory.total / (1024**3):.1f} GB)\n"
        f"Disk (/): {disk.percent:.1f}% used ({disk.used / (1024**3):.1f} / {disk.total / (1024**3):.1f} GB)\n"
        f"Battery: {battery_text}"
    )
