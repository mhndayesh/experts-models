"""spawn.py - bundled llama-server lifecycle (the --gguf mode).

Makes factbank self-contained: no LM Studio/Ollama needed — point it at a
GGUF and it runs its own OpenAI-compatible backend on a private localhost
port, health-waited on the way up and ALWAYS torn down on the way out
(atexit + explicit stop; a finished run must never squat on VRAM — owner
rule, 2026-07-12).
"""

import atexit
import os
import shutil
import socket
import subprocess
import time
import urllib.request


class SpawnError(RuntimeError):
    pass


def find_llama(bin_arg: str | None = None) -> str:
    cands = []
    if bin_arg:
        cands.append(bin_arg)
    cands += ["llama-server", "llama-server.exe",
              os.path.expanduser("~/tools/llama-cpp/llama-server.exe")]
    for c in cands:
        if os.path.sep in c or (os.altsep and os.altsep in c):
            if os.path.exists(c):
                return c
        else:
            hit = shutil.which(c)
            if hit:
                return hit
    raise SpawnError(
        "llama-server not found — pass --llama-bin PATH or put "
        "llama-server on PATH (https://github.com/ggml-org/llama.cpp "
        "releases)")


def free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


class LlamaServer:
    """One spawned llama-server. base_url is OpenAI-compatible."""

    def __init__(self, gguf: str, bin_path: str | None = None,
                 port: int | None = None, ctx: int = 16384, ngl: int = 99,
                 alias: str = "factbank-local", embedding: bool = False,
                 log: str | None = None, timeout: float = 300.0):
        if not os.path.exists(gguf):
            raise SpawnError(f"gguf not found: {gguf}")
        self.gguf = gguf
        self.alias = alias
        self.port = port or free_port()
        cmd = [find_llama(bin_path), "-m", gguf,
               "--host", "127.0.0.1", "--port", str(self.port),
               "-ngl", str(ngl), "-c", str(ctx), "--alias", alias]
        if embedding:
            cmd += ["--embedding", "--pooling", "mean"]
        self._log_fh = open(log, "ab") if log else None
        self.proc = subprocess.Popen(
            cmd, stdout=self._log_fh or subprocess.DEVNULL,
            stderr=subprocess.STDOUT)
        atexit.register(self.stop)
        self._wait(timeout)

    @property
    def base_url(self) -> str:
        return f"http://127.0.0.1:{self.port}/v1"

    def _wait(self, timeout: float):
        end = time.time() + timeout
        url = f"http://127.0.0.1:{self.port}/health"
        while time.time() < end:
            if self.proc.poll() is not None:
                raise SpawnError(
                    f"llama-server exited rc={self.proc.returncode} while "
                    f"loading {os.path.basename(self.gguf)}"
                    + (" — see its log" if self._log_fh else
                       " — rerun with a log path for detail"))
            try:
                with urllib.request.urlopen(url, timeout=2) as r:
                    if r.status == 200:
                        return
            except Exception:
                pass
            time.sleep(0.5)
        self.stop()
        raise SpawnError(f"llama-server never became healthy in "
                         f"{timeout:.0f}s ({os.path.basename(self.gguf)})")

    def stop(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(10)
            except subprocess.TimeoutExpired:
                self.proc.kill()
        if self._log_fh:
            try:
                self._log_fh.close()
            except Exception:
                pass
            self._log_fh = None
