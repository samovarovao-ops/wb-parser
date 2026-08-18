import webbrowser
import threading
import time
from web_app import app


def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://localhost:8080")


if __name__ == "__main__":
    threading.Thread(target=open_browser, daemon=True).start()
    print("=" * 50)
    print("  WB Parser — Парсер Wildberries")
    print("  Откроется в браузере автоматически...")
    print("  Для остановки закройте это окно")
    print("=" * 50)
    app.run(debug=False, host="0.0.0.0", port=8080, use_reloader=False)
