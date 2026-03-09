#!/usr/bin/env python3
"""VSCode setup script — idempotent, macOS only."""

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CONFIG_DIR = SCRIPT_DIR / "config"
VSCODE_USER_DIR = Path.home() / "Library" / "Application Support" / "Code" / "User"

# Summary tracking
summary: list[tuple[str, str, str]] = []  # (status, label, detail)


# ---------------------------------------------------------------------------
# Dependency detection & installation
# ---------------------------------------------------------------------------

def _check_jetbrains_font() -> bool:
    font_dirs = [
        Path.home() / "Library" / "Fonts",
        Path("/Library/Fonts"),
        Path("/System/Library/Fonts"),
    ]
    for d in font_dirs:
        if d.exists() and any(d.glob("*JetBrainsMono*")):
            return True
    return False


DEPS = [
    {
        "name": "VSCode",
        "check": lambda: shutil.which("code") is not None
                         or Path("/Applications/Visual Studio Code.app").exists(),
        "brew": "brew install --cask visual-studio-code",
    },
    {
        "name": "Node.js / npm",
        "check": lambda: shutil.which("node") is not None,
        "brew": "brew install node",
    },
    {
        "name": "Go",
        "check": lambda: shutil.which("go") is not None,
        "brew": "brew install go",
    },
    {
        "name": "Rust (rustup)",
        "check": lambda: shutil.which("rustup") is not None
                         or Path.home().joinpath(".cargo/bin/rustup").exists(),
        "brew": "brew install rustup-init && rustup-init -y",
    },
    {
        "name": "JetBrains Mono font",
        "check": _check_jetbrains_font,
        "brew": "brew install --cask font-jetbrains-mono",
    },
    {
        "name": "Podman Desktop",
        "check": lambda: Path("/Applications/Podman Desktop.app").exists(),
        "brew": "brew install --cask podman-desktop",
    },
    {
        "name": "Claude Code CLI",
        "check": lambda: shutil.which("claude") is not None,
        "brew": "npm install -g @anthropic-ai/claude-code",
    },
]


def _ensure_code_on_path() -> bool:
    """After cask install, the `code` CLI may need the app bundle's bin dir."""
    if shutil.which("code"):
        return True
    app_bin = Path("/Applications/Visual Studio Code.app/Contents/Resources/app/bin")
    if app_bin.exists():
        os.environ["PATH"] = str(app_bin) + os.pathsep + os.environ.get("PATH", "")
        return shutil.which("code") is not None
    return False


def check_dependencies() -> None:
    missing = [d for d in DEPS if not d["check"]()]

    if not missing:
        print("All dependencies already installed.\n")
        return

    print("The following dependencies are missing:\n")
    col_w = max(len(d["name"]) for d in missing) + 2
    print(f"  {'Dependency':<{col_w}}  Install command")
    print(f"  {'-'*col_w}  {'-'*40}")
    for d in missing:
        print(f"  {d['name']:<{col_w}}  {d['brew']}")

    print()
    answer = input("Install all missing dependencies now? [y/N] ").strip().lower()
    if answer != "y":
        print("\nPlease install the above dependencies manually, then re-run this script.")
        sys.exit(1)

    for d in missing:
        print(f"\n▶ Installing {d['name']} …")
        cmd = d["brew"]
        ret = subprocess.run(cmd, shell=True)
        if ret.returncode != 0:
            print(f"  ERROR: failed to install {d['name']} (exit {ret.returncode})")
            print("  Fix the error above and re-run this script.")
            sys.exit(1)
        print(f"  ✓ {d['name']} installed.")

    # After installing VSCode, ensure `code` is on PATH for the rest of the run.
    _ensure_code_on_path()


# ---------------------------------------------------------------------------
# Extension installation
# ---------------------------------------------------------------------------

def _installed_extensions() -> set[str]:
    result = subprocess.run(
        ["code", "--list-extensions"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return set()
    return {line.strip().lower() for line in result.stdout.splitlines() if line.strip()}


def install_extensions() -> None:
    if not _ensure_code_on_path():
        summary.append(("❌", "Extensions", "skipped — `code` CLI not found on PATH"))
        return

    ext_file = CONFIG_DIR / "extensions.txt"
    extensions = []
    for line in ext_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            extensions.append(line)

    already = _installed_extensions()
    failures = []
    installed_count = 0

    for ext in extensions:
        if ext.lower() in already:
            installed_count += 1
            continue
        print(f"  Installing {ext} …")
        result = subprocess.run(
            ["code", "--install-extension", ext, "--force"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            installed_count += 1
        else:
            failures.append(ext)
            print(f"  WARNING: failed to install {ext}")

    total = len(extensions)
    if failures:
        detail = f"{total - len(failures)}/{total} installed ({len(failures)} failed: {', '.join(failures)})"
        summary.append(("⚠️ ", "Extensions", detail))
    else:
        summary.append(("✅", "Extensions", f"{total}/{total} installed"))


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

def deep_merge(base: dict, override: dict) -> dict:
    """Merge override into base — override keys win."""
    result = base.copy()
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = v
    return result


def write_settings() -> None:
    base = json.loads((CONFIG_DIR / "settings.json").read_text())
    dest = VSCODE_USER_DIR / "settings.json"
    dest.parent.mkdir(parents=True, exist_ok=True)

    backed_up = None
    if dest.exists():
        existing = json.loads(dest.read_text())
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        bak = dest.with_name(f"settings.json.bak.{ts}")
        shutil.copy2(dest, bak)
        backed_up = bak.name
        merged = deep_merge(base, existing)  # existing user keys win
    else:
        merged = base

    dest.write_text(json.dumps(merged, indent=2) + "\n")
    detail = f"written" + (f" (backed up to {backed_up})" if backed_up else "")
    summary.append(("✅", "settings.json", detail))


# ---------------------------------------------------------------------------
# Keybindings
# ---------------------------------------------------------------------------

def write_keybindings() -> None:
    our_bindings = json.loads((CONFIG_DIR / "keybindings.json").read_text())
    dest = VSCODE_USER_DIR / "keybindings.json"
    dest.parent.mkdir(parents=True, exist_ok=True)

    backed_up = None
    if dest.exists():
        existing_text = dest.read_text().strip()
        try:
            existing = json.loads(existing_text) if existing_text else []
        except json.JSONDecodeError:
            existing = []

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        bak = dest.with_name(f"keybindings.json.bak.{ts}")
        shutil.copy2(dest, bak)
        backed_up = bak.name

        existing_cmds = {b.get("command") for b in existing if isinstance(b, dict)}
        additions = [b for b in our_bindings if b.get("command") not in existing_cmds]
        merged = existing + additions
    else:
        merged = our_bindings

    dest.write_text(json.dumps(merged, indent=2) + "\n")
    detail = "written" + (f" (backed up to {backed_up})" if backed_up else "")
    summary.append(("✅", "keybindings.json", detail))


# ---------------------------------------------------------------------------
# Podman configuration
# ---------------------------------------------------------------------------

def configure_podman() -> None:
    socket_candidates = [
        Path(os.environ.get("XDG_RUNTIME_DIR", "")) / "podman" / "podman.sock",
        Path.home() / ".local/share/containers/podman/machine/podman.sock",
        Path.home() / ".local/share/containers/podman/machine/qemu/podman.sock",
    ]

    socket_path = next((p for p in socket_candidates if p.exists()), None)

    dest = VSCODE_USER_DIR / "settings.json"
    if not dest.exists():
        summary.append(("⚠️ ", "Podman socket", "settings.json not found — run write_settings first"))
        return

    settings = json.loads(dest.read_text())

    if socket_path:
        settings["docker.host"] = f"unix://{socket_path}"
        dest.write_text(json.dumps(settings, indent=2) + "\n")
        summary.append(("✅", "Podman socket", f"configured ({socket_path})"))
    else:
        # Remove stale entry if socket no longer exists
        if "docker.host" in settings:
            del settings["docker.host"]
            dest.write_text(json.dumps(settings, indent=2) + "\n")
        summary.append(("⚠️ ", "Podman socket", "socket not found — start Podman Desktop and re-run"))


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

def print_header() -> None:
    print("=" * 60)
    print("  VSCode Setup — IntelliJ migration")
    print("=" * 60)
    print()


def print_summary() -> None:
    print()
    print("=" * 60)
    print("  Setup Summary")
    print("=" * 60)
    col = max(len(label) for _, label, _ in summary) + 2
    for status, label, detail in summary:
        print(f"  {status}  {label:<{col}}  {detail}")
    print()
    print("  ⚠️   Manual step: SCM panel → ⋯ → View as Tree")
    print("=" * 60)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    print_header()
    check_dependencies()
    install_extensions()
    write_settings()
    write_keybindings()
    configure_podman()
    print_summary()


if __name__ == "__main__":
    main()
