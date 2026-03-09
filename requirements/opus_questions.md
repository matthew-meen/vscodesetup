# Opus Review — Questions & Suggestions

## Open Questions

### Theme
1. **Which dark theme specifically?** The requirement says "Dark (equivalent to IntelliJ Darcula)" but there are several strong candidates: "One Dark Pro", "Darcula Theme" (direct port), "Tokyo Night", or VSCode's built-in "Dark Modern". Do you have a preference, or should the script install a few and let you pick? The direct Darcula port will feel most familiar but some consider it dated compared to modern alternatives.

### Inlay Hints — Contradictory Settings
2. **Section 4 (Rust) says inlay hints should be enabled for rust-analyzer**, but Section 12 sets `editor.inlayHints.enabled` to `"offUnlessPressed"` globally. This means Rust inlay hints will be hidden by default and only appear when you hold Ctrl+Alt. Is that intentional? Options:
   - Keep `"offUnlessPressed"` globally (all languages, show on demand)
   - Set `"on"` globally (always visible — matches IntelliJ behaviour)
   - Set `"offUnlessPressed"` globally but override to `"on"` for Rust specifically via `[rust]` language scope

### Python Profiling
3. **What profiling tool do you use in IntelliJ?** The built-in cProfile/yappi profiler, or py-spy, or the PyCharm performance profiler? VSCode doesn't have a direct equivalent of PyCharm's integrated profiler. The closest options are:
   - **Austin VSCode** extension (sampling profiler with flame graphs)
   - **py-spy** via terminal (no VSCode integration but excellent tool)
   - **Python Profiler** extension (wraps cProfile with a UI)
   - **Scalene** via terminal (CPU + memory + GPU profiler)

   Which approach would you accept? This is the biggest feature gap vs IntelliJ.

### Podman Integration
4. **What level of Podman integration do you need?** The requirement says "basic integration" but there are different levels:
   - Just syntax highlighting for Containerfiles/Dockerfiles
   - Building/running containers from VSCode
   - Viewing running containers, logs, exec into shells
   - Full Podman Desktop integration (requires Podman Desktop installed)

   Also: should the script configure the Docker extension to use Podman's socket (`podman.socketPath`) so Docker-targeting extensions work transparently with Podman?

### Database — SQLTools vs Alternatives
5. **SQLTools is functional but fairly basic compared to DataGrip.** Have you considered:
   - **Database Client JDBC** (by Weijan Chen) — much closer to DataGrip with schema browsing, query history, autocomplete, ERD diagrams
   - **SQLTools** — lighter weight, open source, decent for simple queries

   Which trade-off do you prefer: closer to DataGrip (heavier extension) or lightweight and good-enough?

### Script Language
6. **What should the setup script be written in?** Options:
   - **Bash/zsh** — simplest, no dependencies, most natural for macOS setup scripts
   - **Python** — you already have Python, more readable for complex logic (JSON merging, etc.)
   - **Makefile** — common for dev setup, easy to run individual targets

   The JSON merging requirement (don't overwrite existing settings.json) is non-trivial in pure bash but straightforward in Python.

### Claude Code Installation
7. **How should Claude Code CLI be installed?** Currently it's available via:
   - `npm install -g @anthropic-ai/claude-code`
   - Direct download from Anthropic

   Should the script assume Node.js/npm is already installed, or should it install that too? Same question for Homebrew — should the script install Homebrew if not present, or assume it exists?

### Go Tab Size
8. **Go convention is tabs, not spaces, with `tabSize: 4` for display.** The global setting has `editor.insertSpaces: true`. Should the script add a Go-specific override?
   ```json
   "[go]": {
     "editor.insertSpaces": false,
     "editor.tabSize": 4
   }
   ```
   Without this, `gofmt` will fight your editor on every save.

---

## Suggestions

### Missing Settings I'd Add

9. **`files.trimTrailingWhitespace: true`** — Removes trailing whitespace on save. Standard in IntelliJ and almost universally desired.

10. **`files.insertFinalNewline: true`** — Ensures files end with a newline (POSIX standard, prevents git diffs on last line).

11. **`files.trimFinalNewlines: true`** — Removes extra blank lines at end of file.

12. **`editor.formatOnSave: true`** — Since per-project formatters are expected, having format-on-save enabled globally means they activate automatically when configured. Without this, the `runCommands` keybinding for Cmd+S is the only way to format. Both approaches work but `formatOnSave` is simpler and more conventional.
    - Note: This potentially conflicts with the `runCommands` Cmd+S keybinding in Section 13. Pick one approach.

13. **`editor.bracketPairColorization.enabled: true`** — Section 11 mentions "Built-in VSCode bracket colorization (enable it)" but it's not in the settings table. Should be added explicitly.

14. **`editor.cursorBlinking: "smooth"`** and **`editor.cursorSmoothCaretAnimation: "on"`** — Subtle but makes the editor feel more polished. IntelliJ has smooth caret movement by default.

15. **`editor.smoothScrolling: true`** and **`workbench.list.smoothScrolling: true`** — Smooth scroll in editor and sidebars. IntelliJ scrolls smoothly by default.

### Missing Extensions

16. **Error Lens** (`usernamehw.errorlens`) — Shows errors/warnings inline at the end of the line, similar to how IntelliJ shows them. Much more visible than just squiggly underlines. This is one of the most popular extensions for IntelliJ refugees.

17. **Git Graph** (`mhutchie.git-graph`) — Better visual git log than GitLens alone. Shows a proper branch graph like IntelliJ's Git log tab. GitLens has a graph too but it's a paid feature in newer versions.

18. **TODO Highlight** or **Todo Tree** (`gruntfuggly.todo-tree`) — Aggregates TODO/FIXME/HACK comments into a tree view. IntelliJ has this built-in.

19. **Path Intellisense** (`christian-kohler.path-intellisense`) — Autocompletes file paths in imports/strings. IntelliJ does this natively.

### Potential Issues

20. **`workbench.editor.showTabs: "multiple"` is not a valid value.** The valid values are `"multiple"`, `"single"`, `"none"`. Actually `"multiple"` is valid in recent VSCode versions — disregard if targeting latest VSCode.

21. **The `runCommands` keybinding for Cmd+S** (Section 13) will override the default save behaviour. This is fine but should be documented clearly — if a user has `formatOnSave` enabled AND this keybinding, the file gets formatted twice on every save.

22. **Font installation** — JetBrains Mono needs to be installed on the system. The script should either:
    - Install it via `brew install --cask font-jetbrains-mono` (requires Homebrew + cask-fonts tap)
    - Check if it's already installed and warn if not
    - Bundle it

23. **The Anthropic VSCode Extension** — the exact extension ID should be pinned. Currently it's `anthropic.claude-code` but this may change. The script should document which extension ID it installs.

### Architecture Suggestion

24. **Consider a two-layer approach:**
    - `settings.base.json` — the opinionated settings from this requirements doc
    - `settings.json` — merged result of base + any existing user settings

    This makes it easy to update the base settings later without re-running the full script. The script's merge logic becomes: read base, read existing, deep-merge (base wins for new keys, existing wins for already-customised keys), write result.
