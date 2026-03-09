# vscodesetup

A portable macOS setup script that configures VSCode to closely replicate the JetBrains IntelliJ IDEA Ultimate experience — for developers migrating away from JetBrains.

## What it does

Runs a single Python script that installs and configures everything needed to be productive in VSCode from day one:

- **Appearance** — Darcula theme, JetBrains Mono font with ligatures
- **Languages** — Full language server support for Python, Go, and Rust (Pylance, gopls, rust-analyzer)
- **Debugging** — Integrated debugger for all three languages, pytest/go test/cargo test UI, Python profiling via Austin
- **AI** — Claude Code CLI in the integrated terminal + Anthropic VSCode extension for inline chat
- **Git** — Visual branch graph, side-by-side diff, inline blame (GitLens + Git Graph)
- **Database** — SQLTools with PostgreSQL, MySQL, and SQLite drivers
- **Containers** — Podman Desktop integration with Docker socket compatibility
- **Editor behaviour** — Opinionated settings tuned to match IntelliJ defaults (inlay hints, sticky scroll, bracket guides, smart tab stops, and more)

## Requirements

- macOS
- [Homebrew](https://brew.sh) installed
- Everything else (VSCode, Go, Rust, Node.js, fonts, Podman Desktop) is installed by the script after a single confirmation prompt

## Usage

```bash
git clone https://github.com/matthew-meen/vscodesetup.git
cd vscodesetup
python3 setup.py
```

## What's in this repo

```
requirements/
  requirements.md     # Full detailed requirements and settings spec
  opus_questions.md   # Design decisions and rationale captured during planning
setup.py              # The setup script (coming soon)
```

## Background

Migrating from IntelliJ IDEA Ultimate after losing a JetBrains licence. The goal is not just to install some extensions, but to reproduce the specific workflows, keybindings, editor behaviours, and tooling integrations that make IntelliJ productive — without fighting VSCode's defaults where they're good.
