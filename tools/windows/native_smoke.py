"""Native Windows imports and Qt smoke check. No credentials or model calls."""
import os
from pathlib import Path
import platform
import subprocess
import sys

def main():
    if sys.platform != "win32":
        print("Native Windows required; this check cannot pass on another OS.")
        return 1
    if os.environ.get("QT_QPA_PLATFORM", "windows") != "windows":
        print("The native Windows Qt platform is required.")
        return 1
    root = Path(__file__).resolve().parents[2]
    print(f"Native host: {platform.platform()}; Python {platform.python_version()}", flush=True)
    result = subprocess.run([sys.executable, str(root / "launcher.py"), "--check"],
                            cwd=root, timeout=180)
    if result.returncode:
        return result.returncode
    from PyQt6.QtCore import QTimer
    from PyQt6.QtWidgets import QApplication, QWidget
    app = QApplication([])
    if app.platformName() != "windows":
        raise RuntimeError("Qt did not load its Windows plugin")
    window = QWidget()
    window.setWindowTitle("Jarvis-Blue native Windows smoke")
    window.show()
    app.processEvents()
    if not window.isVisible():
        raise RuntimeError("Native Qt window did not open")
    QTimer.singleShot(250, app.quit)
    code = app.exec()
    window.close()
    print("Native Qt window opened and event loop completed.", flush=True)
    return code

if __name__ == "__main__":
    raise SystemExit(main())
