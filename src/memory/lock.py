import fcntl
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def vault_lock(lock_path: Path = Path("longterm_memory/.vault.lock")):
    """Process-level advisory lock. Only one agent writes at a time.
    Reads are always safe (agents read stale-but-consistent snapshots)."""
    lock_path.touch(exist_ok=True)
    fd = open(lock_path, "w")
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        fd.close()
