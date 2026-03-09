# VSCode Setup Requirements
## Migrating from IntelliJ IDEA Ultimate → VSCode

**Platform:** macOS only
**Portability:** Script must be fully portable (reusable on new machines)
**Source IDE:** IntelliJ IDEA Ultimate 2025.3

---

## 1. Appearance & Font

- **Theme:** Darcula Theme (`rokoroku.vscode-theme-darcula`) — direct IntelliJ port
- **Font:** JetBrains Mono, 13pt (installed via `brew install --cask font-jetbrains-mono`)
- **Ligatures:** Enabled (`->`, `!=`, `=>` etc. render as glyphs)
- **UI font size:** 13pt

---

## 2. Editor Layout & Tabs

- **Tabs:** Keep many tabs open (do not auto-close)
- **Split editors:** Supported — side-by-side (vertical) is primary, horizontal also used
- **Project tree panel:** Always visible (left sidebar open by default)
- **Tab bar:** Always visible, allow many tabs

---

## 3. Keybindings

- **Keymap:** VSCode native keybindings (no JetBrains overlay)
- No custom keybindings required — use VSCode defaults

---

## 4. Language Support & Servers

All three languages need fully working language servers with:
- Go-to-definition, find references, rename symbol
- Inline diagnostics (errors/warnings)
- Auto-import / import management
- Code completion

### Python
- **Language server:** Pylance (via Python extension)
- **Formatter/linter:** Added per-project (not global) — script should not enforce a global formatter
- **Virtual environments:** venv support required (auto-detect `.venv` / `venv` directories)
- **Version:** Python 3.10+ (currently using 3.10.13)

### Go
- **Language server:** `gopls` (via Go extension)
- **Formatter:** `gofmt` only — no additional linters
- **Go modules:** Required

### Rust
- **Language server:** `rust-analyzer` with full feature set:
  - Inline type hints (inlay hints)
  - Proc-macro expansion
  - Clippy integration for diagnostics
  - `rustfmt` for formatting
- **Cargo workspace support** required

---

## 5. Debugging

Full debugger support required for all three languages (equivalent to IntelliJ's debugger UI):
- Breakpoints, step over/into/out, variable inspection, call stack
- **Python:** Debug + profiling via **Austin VSCode** extension (`p403n1x87.austin-vscode`) — sampling profiler with flame graphs
- **Go:** Delve-based debugger
- **Rust:** LLDB-based debugger (via CodeLLDB)

### Testing
- **Python:** pytest — run via UI (play button next to test functions/classes), not just CLI
- **Go:** `go test` — run via UI
- **Rust:** `cargo test` — run via UI

---

## 6. Terminal

- **Location:** Integrated terminal inside VSCode (not external)
- **Option-as-Meta:** Enabled (matches current IntelliJ terminal config)
- Shell: zsh (macOS default)

---

## 7. Claude / AI Integration

Two components required:

1. **Claude Code CLI** — available in the integrated terminal (installed globally via npm/brew)
2. **Anthropic VSCode Extension** — for inline chat / code generation within the editor

No MCP servers required at this time.

---

## 8. Version Control (Git)

- **Visual Git log:** Required — equivalent to IntelliJ's Git log view (branch graph, commit history)
- **Visual diff viewer:** Required — side-by-side diff for staged/unstaged changes
- **GitHub account:** `matthew-meen` at github.com
- GitLens or equivalent extension for blame, history, and log UI

---

## 9. Container Support

- **Podman Desktop** — full integration (requires Podman Desktop installed)
  - Syntax highlighting for Containerfiles/Dockerfiles
  - Build/run containers from VSCode
  - View running containers, logs, exec into shells
- Configure Docker-targeting extensions to use Podman's socket transparently (`docker.host` / `podman.socketPath`)
- No devcontainer requirement

---

## 10. Database Tools

- **DataGrip-equivalent** basic functionality:
  - Connect to databases (PostgreSQL, MySQL, SQLite at minimum)
  - Browse tables/schemas
  - Run SQL queries with syntax highlighting
  - View query results in a table UI
- **Extension:** SQLTools (`mtxr.sqltools`) with driver extensions for PostgreSQL, MySQL, SQLite

---

## 11. Additional Extensions

| Category | Extension ID |
|---|---|
| File icons | `pkief.material-icon-theme` |
| EditorConfig | `editorconfig.editorconfig` |
| Dotenv | `mikestead.dotenv` |
| Mermaid | `bierner.markdown-mermaid` |
| TOML | `tamasfe.even-better-toml` |
| YAML | `redhat.vscode-yaml` |
| Podman / Docker | `ms-azuretools.vscode-docker` |
| Error Lens | `usernamehw.errorlens` |
| Git Graph | `mhutchie.git-graph` |
| Todo Tree | `gruntfuggly.todo-tree` |
| Path Intellisense | `christian-kohler.path-intellisense` |
| Darcula Theme | `rokoroku.vscode-theme-darcula` |
| Python Profiler | `p403n1x87.austin-vscode` |

---

## 12. VSCode Settings (Non-default values to configure)

| Setting | Value | Reason |
|---|---|---|
| `editor.fontFamily` | `"JetBrains Mono"` | Match IntelliJ font |
| `editor.fontSize` | `13` | Match IntelliJ size |
| `editor.fontLigatures` | `true` | Enable ligatures |
| `editor.tabSize` | `4` | Standard default |
| `editor.insertSpaces` | `true` | Spaces not tabs |
| `editor.renderWhitespace` | `"boundary"` | Visibility |
| `editor.minimap.enabled` | `false` | IntelliJ doesn't have minimap |
| `workbench.colorTheme` | Dark theme TBD | Match Darcula |
| `explorer.openEditors.visible` | `0` | Hide open editors list (tabs do this) |
| `terminal.integrated.macOptionIsMeta` | `true` | Match IntelliJ terminal config |
| `editor.inlayHints.enabled` | `"on"` | Always visible, matches IntelliJ behaviour |
| `editor.stickyScroll.enabled` | `true` | Pins current scope header while scrolling |
| `workbench.tree.enableStickyScroll` | `true` | Sticky scroll in Explorer tree too |
| `editor.stickyScroll.maxLineCount` | `5` | Max pinned scope lines |
| `workbench.editor.enablePreview` | `false` | Keep tabs open (don't replace on single click) |
| `workbench.editor.showTabs` | `"multiple"` | Always show tab bar |
| `editor.acceptSuggestionOnEnter` | `"off"` | Autocomplete only on Tab, not Enter |
| `editor.suggest.preview` | `true` | Ghost-text preview of top suggestion |
| `editor.stickyTabStops` | `true` | Backspace removes full indent level at once |
| `editor.foldingImportsByDefault` | `true` | Collapse imports on file open |
| `editor.guides.bracketPairs` | `"active"` | Guide line only for current bracket pair |
| `editor.guides.bracketPairsHorizontal` | `"active"` | Horizontal guide for bracket pairs |
| `editor.linkedEditing` | `true` | Rename opening/closing HTML tags together |
| `editor.fastScrollSensitivity` | `10` | Alt+scroll jumps 10x faster |
| `editor.rulers` | `[80, 120]` | Visual line length guides |
| `workbench.commandPalette.preserveInput` | `true` | Remember last command palette search |
| `workbench.settings.editor` | `"json"` | Cmd+, opens settings.json directly |
| `explorer.fileNesting.enabled` | `true` | Group related files under parent in Explorer |
| `explorer.fileNesting.patterns` | See below | Nest lock files, maps, configs under parents |
| `explorer.compactFolders` | `false` | Each folder on its own line (no merged paths) |
| `workbench.editor.customLabels.enabled` | `true` | Show parent folder in tab for same-named files |
| `window.title` | `"${dirty}${rootName} — ${activeEditorShort}"` | Project + file in OS window title |
| `terminal.integrated.persistentSessionReviveProcess` | `"onExitAndWindowClose"` | Restore terminal sessions after restart |
| `scm.diffDecorationsGutterWidth` | `3` | Make gutter change bars visible (default 1px) |
| `scm.diffDecorationsGutterVisibility` | `"always"` | Always show gutter diff decorations |
| `files.trimTrailingWhitespace` | `true` | Remove trailing whitespace on save |
| `files.insertFinalNewline` | `true` | Ensure files end with a newline |
| `files.trimFinalNewlines` | `true` | Remove extra blank lines at end of file |
| `editor.formatOnSave` | `false` | Formatting handled by runCommands Cmd+S keybinding |
| `editor.bracketPairColorization.enabled` | `true` | Built-in bracket colorization |
| `editor.cursorBlinking` | `"smooth"` | Smooth cursor blink like IntelliJ |
| `editor.cursorSmoothCaretAnimation` | `"on"` | Smooth caret movement |
| `editor.smoothScrolling` | `true` | Smooth scroll in editor |
| `workbench.list.smoothScrolling` | `true` | Smooth scroll in sidebars |
| `[go]` override: `editor.insertSpaces` | `false` | Go uses tabs — prevent gofmt conflicts |
| `[go]` override: `editor.tabSize` | `4` | Display tab width for Go files |

### File Nesting Patterns
```json
"explorer.fileNesting.patterns": {
  "*.ts": "${capture}.js, ${capture}.d.ts, ${capture}.js.map",
  "package.json": "package-lock.json, yarn.lock, pnpm-lock.yaml, .npmrc",
  "tsconfig.json": "tsconfig.*.json",
  "Cargo.toml": "Cargo.lock",
  "go.mod": "go.sum",
  "*.rs": "${capture}.rs.bk"
}
```

---

## 13. Advanced Keybindings

- **`runCommands` on `Cmd+S`** — Chains `editor.action.formatDocument` then `workbench.action.files.save`. This is the chosen approach over `formatOnSave: true` (avoid double-format conflict).
- **`Ctrl+U`** — Undo last multi-cursor addition without collapsing all cursors
- **`Ctrl+K Ctrl+D`** — Skip current `Ctrl+D` match, move to next occurrence
- **`Shift+Option+I`** — Place cursor at end of every selected line simultaneously
- **`Shift+Option` drag** — Column/box selection (rectangular multi-cursor)
- **Regex Find/Replace** — Enabled with `$1`/`$2` capture group backreferences in replace field

## 14. Advanced Debugging

- **Logpoints** — Right-click gutter → Add Logpoint; prints `{expression}` to Debug Console without pausing execution
- **Conditional breakpoints** — Break only when expression is true or after N hits
- **Triggered breakpoints** — Breakpoint only activates after another specific breakpoint has been hit first

## 15. SCM / Git UI

- **SCM Tree View** — Show changed files grouped by directory (not flat list)
- **Gutter diff decorations** — Width 3, always visible

## 16. Script Behaviour

The setup script should:
- **Language:** Python
- Be idempotent (safe to run multiple times)
- **Assume Homebrew is installed** — install everything else (VSCode, Claude Code CLI, Node.js, Go, Rust, JetBrains Mono font, Podman Desktop) only after showing a single confirmation prompt listing all missing dependencies
- Install VSCode extensions via `code --install-extension`
- Write `settings.json` and `keybindings.json` to `~/Library/Application Support/Code/User/`
- **Merge settings** — deep-merge with any existing `settings.json` (base wins for new keys, existing wins for already-customised keys); back up before writing
- Print a summary of what was installed/configured
- Fail gracefully with clear error messages if a step fails
