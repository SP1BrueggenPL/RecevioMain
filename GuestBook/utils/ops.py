# utils/ops.py (utwórz plik modułu pomocniczego)
import threading

def run_with_timeout(func, *args, seconds=5, **kwargs):
    """
    Uruchamia func(*args, **kwargs) z maks. czasem `seconds`.
    Zwraca 'ok' | 'timeout' | 'error', a wyjątek (jeśli był) w polu 'error'.
    """
    box = {"exc": None}
    def _target():
        try:
            func(*args, **kwargs)
        except Exception as e:
            box["exc"] = e

    t = threading.Thread(target=_target, daemon=True)
    t.start()
    t.join(seconds)
    if t.is_alive():
        return "timeout"
    return "ok" if box["exc"] is None else "error"
