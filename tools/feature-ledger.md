# Claude Code feature ledger

Verified 2026-11-18 against https://code.claude.com/docs/en/ (canonical docs; docs.claude.com redirects there). Corroborated locally with `claude --help` / `claude doctor --help` / `claude update --help`, installed version 2.1.327. Audience: Ubuntu 24.04, individual Claude Max 5x.

Column `id` is the literal token the guide uses. `verified` is the date checked.

| id | feature | exact syntax | doc URL | verified | notes |
| :- | :- | :- | :- | :- | :- |
| `curl -fsSL https://claude.ai/install.sh \| bash` | Linux install (native, recommended) | `curl -fsSL https://claude.ai/install.sh \| bash` then open a new terminal and run `claude --version` | https://code.claude.com/docs/en/setup | 2026-11-18 | Ubuntu 20.04+ supported (24.04 fine), 4 GB+ RAM. Installs `~/.local/bin/claude` symlink. Alternatives: apt repo, `npm install -g @anthropic-ai/claude-code@latest` (Node 22+, never sudo). Channel pin: `... \| bash -s stable`. |
| `claude update` | Update | `claude update` | https://code.claude.com/docs/en/setup#update-manually | 2026-11-18 | Native installs auto-update in background; `claude update` applies now. `claude update` and `claude upgrade` both exist locally. apt installs update via `sudo apt update && sudo apt upgrade claude-code`. Disable auto-update: `env.DISABLE_AUTOUPDATER=1`. |
| `claude doctor` | Install/settings diagnostics (shell command) | `claude doctor` | https://code.claude.com/docs/en/cli-reference | 2026-11-18 | Read-only, prints diagnostics without starting a session. Separate from in-session `/doctor` (bundled skill, alias `checkup`, proposes fixes after confirmation). Local `claude doctor --help` confirms. |
| `/login` | Sign in | `/login` (or just run `claude` and follow browser prompts) | https://code.claude.com/docs/en/commands | 2026-11-18 | Max requires a claude.ai account login; free plan has no Claude Code. |
| `/status` | Version, model, account, setting sources | `/status` | https://code.claude.com/docs/en/commands | 2026-11-18 | Opens Settings on Status tab; runs immediately even while Claude is responding. Shows `Setting sources` line. |
| `/usage` | Plan usage limits (Max 5x visibility) | `/usage` (alias `/cost`) | https://code.claude.com/docs/en/costs | 2026-11-18 | On Max shows plan usage bars, activity stats and a breakdown of what counts against limits; Session cost figure is not billing-relevant for subscribers. `f` applies suggested fixes (v2.1.305+). `r` retries on rate limit. |
| `/model` | Switch model | `/model [model]`; aliases `default`, `best`, `opus`, `sonnet`, `haiku`, `fable`, `opusplan`, `opus[1m]`, `sonnet[1m]`; flag `claude --model <alias>` | https://code.claude.com/docs/en/model-config | 2026-11-18 | Picker saves as default; press `s` to switch for this session only. Aliases currently resolve to Opus 5.5 / Sonnet 5.5 / Haiku 5.5. |
| `/effort` | Effort-level control | `/effort [low\|medium\|high\|xhigh\|max\|auto\|status]`; `claude --effort <level>`; env `CLAUDE_CODE_EFFORT_LEVEL`; settings `effortLevel` | https://code.claude.com/docs/en/model-config#adjust-effort-level | 2026-11-18 | Levels depend on model (Opus 4.6/Sonnet 4.6 lack `xhigh`). `max` is session-only; not accepted in `effortLevel`. Include word `ultrathink` in a prompt for one deeper turn. `/effort ultracode` also exists. Local `--effort <level>` confirmed. |
| `Shift+Tab` | Cycle permission modes | `Shift+Tab` | https://code.claude.com/docs/en/permission-modes | 2026-11-18 | Cycle: `default` (labeled Manual) -> `acceptEdits` -> `plan`, then `bypassPermissions` and `auto` only where enabled. `dontAsk` never in cycle. From `auto`, first press goes to default. |
| `--permission-mode` | Start in a permission mode | `claude --permission-mode <default\|acceptEdits\|plan\|auto\|dontAsk\|bypassPermissions>`; settings `permissions.defaultMode`; `manual` alias for `default` | https://code.claude.com/docs/en/permission-modes | 2026-11-18 | Modes: `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`. `auto` is available on Max (needs v2.1.283+ for built-in starting mode, supported model). `auto`/`bypassPermissions` ignored in project settings. Local help confirms flag. |
| `plan mode` | Plan mode (read-only exploration) | `Shift+Tab` until status bar shows `plan mode on`; `/plan [description]`; `claude --permission-mode plan` | https://code.claude.com/docs/en/permission-modes | 2026-11-18 | At the plan-approval prompt press `Esc` first (Shift+Tab there approves the plan). |
| `@` | File reference | type `@` then path (autocomplete) | https://code.claude.com/docs/en/interactive-mode | 2026-11-18 | Also triggers agent mentions (`@agent-<name>`) and, with a letter typed, other live sessions. |
| `Esc` | Interrupt Claude | `Esc` | https://code.claude.com/docs/en/interactive-mode | 2026-11-18 | Stops the current response/tool call, keeps work done. `Ctrl+C` also interrupts; with nothing running, 1st press clears input, 2nd exits. |
| `Esc Esc` | Rewind menu / clear draft | press `Esc` twice | https://code.claude.com/docs/en/checkpointing | 2026-11-18 | Opens rewind menu only when prompt input is empty; if input has text, double Esc clears it (draft saved, `Up` recalls). |
| `/rewind` | Checkpoints: restore code and/or conversation | `/rewind` (aliases `/checkpoint`, `/undo`) | https://code.claude.com/docs/en/checkpointing | 2026-11-18 | Options: restore code and conversation / conversation / code / summarize from here / up to here. Does NOT track files changed only by Bash or by subagents; not a Git replacement. 100 checkpoints kept, ~30 days. |
| `/clear` | New conversation, empty context | `/clear [name]` | https://code.claude.com/docs/en/commands | 2026-11-18 | Prior conversation reachable via `/resume`. |
| `/compact` | Summarize to free context | `/compact [instructions]` | https://code.claude.com/docs/en/commands | 2026-11-18 | Optional focus instructions. |
| `/context` | Context usage grid | `/context [all]` | https://code.claude.com/docs/en/commands | 2026-11-18 | Shows optimization suggestions and capacity warnings. |
| `/init` | Generate CLAUDE.md | `/init` | https://code.claude.com/docs/en/commands | 2026-11-18 | `CLAUDE_CODE_NEW_INIT=1` enables interactive flow (skills, hooks, personal memory). |
| `CLAUDE.md` | Project memory file: locations, precedence | Project: `./CLAUDE.md` or `./.claude/CLAUDE.md`; user: `~/.claude/CLAUDE.md`; local: `./CLAUDE.local.md` (gitignore it); managed on Linux: `/etc/claude-code/CLAUDE.md` | https://code.claude.com/docs/en/memory | 2026-11-18 | All discovered files are concatenated, not overridden; ordered filesystem root down to cwd, so closer to cwd is read last. Managed loads before user/project. Subdirectory CLAUDE.md loads on demand. `AGENTS.md` is read only if no CLAUDE.md/CLAUDE.local.md exists above cwd. Also `.claude/rules/`. |
| `@path/to/import` | CLAUDE.md imports | `@path/to/file` inside CLAUDE.md, e.g. `See @README for overview` | https://code.claude.com/docs/en/memory#import-additional-files | 2026-11-18 | Relative paths resolve from the importing file; max depth 4 hops; skipped inside code spans/fences (wrap in backticks to keep literal); external imports prompt for approval once per project. |
| `/memory` | Edit memory files, toggle auto memory | `/memory` | https://code.claude.com/docs/en/memory | 2026-11-18 | Also lists auto memory entries. |
| `#` | Quick-add memory shortcut | REMOVED | https://code.claude.com/docs/en/interactive-mode | 2026-11-18 | REMOVED: no `#` shortcut appears in the interactive-mode shortcuts or the memory page. Replaced by `/memory` (edit CLAUDE.md) or asking Claude to "remember ..." (auto memory). Do not teach `#`. |
| `.claude/settings.json` | Shared project settings (commit) | `.claude/settings.json` | https://code.claude.com/docs/en/settings | 2026-11-18 | Team permissions/hooks/plugins. Project `allow` rules wait for folder trust; `deny`/`ask` apply immediately. |
| `.claude/settings.local.json` | Personal per-project settings (not committed) | `.claude/settings.local.json` | https://code.claude.com/docs/en/settings | 2026-11-18 | Claude Code writes "Yes, and don't ask again" approvals here, and adds it to global git excludes; if created by hand add to `.gitignore`. Precedence high to low: managed > `--settings` > local > shared project > user (`~/.claude/settings.json`). Lists (e.g. `permissions.allow`) merge. |
| `permissions.allow` | Allow rules (Bash prefix) | `"Bash(npm run *)"`, `"Bash(git commit *)"`, exact `"Bash(npm run build)"`; legacy equivalent `"Bash(npm run:*)"` | https://code.claude.com/docs/en/permissions#tool-specific-permission-rules | 2026-11-18 | Space before trailing `*` matters (`Bash(ls *)` does not match `lsof`). Trailing ` *` also matches the bare command. See Schema details. |
| `permissions.deny` | Deny rules (Read globs) | `"Read(./.env)"`, `"Read(./.env.*)"`, `"Read(./secrets/**)"` | https://code.claude.com/docs/en/permissions#read-and-edit | 2026-11-18 | Evaluation order deny > ask > allow; first match wins; allow cannot carve out of deny. Deny `Read` also covers Grep/Glob. |
| `hooks.PostToolUse` | Hook after a tool succeeds | settings key `hooks.PostToolUse[]` with `matcher: "Edit\|Write"` | https://code.claude.com/docs/en/hooks#posttooluse | 2026-11-18 | Matcher on tool name. `MultiEdit` is legacy/not in current tools list; use `Edit\|Write`. Exit 2 shows stderr to Claude but cannot block (tool already ran). Not triggered by Bash rewriting a file. |
| `hooks.Stop` | Hook when Claude finishes a turn | settings key `hooks.Stop[]` (matcher not used) | https://code.claude.com/docs/en/hooks#stop | 2026-11-18 | Exit 2 blocks stopping (Claude continues, stderr is the reason). Input has `stop_hook_active`; 8-consecutive-continuation cap. |
| `CLAUDE_PROJECT_DIR` | Project dir env var in hook commands | `"command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/x.sh"` | https://code.claude.com/docs/en/hooks | 2026-11-18 | Exported to the hook process. Quote it in shell-form commands (`"$CLAUDE_PROJECT_DIR"/...`). |
| `/hooks` | View hook configuration | `/hooks` | https://code.claude.com/docs/en/commands | 2026-11-18 | Read-only menu. |
| `/agents` | Subagent management | `/agents` | https://code.claude.com/docs/en/sub-agents#the-agents-command | 2026-11-18 | CHANGED: on v2.1.198+ it only prints a reminder to ask Claude to create subagents or edit `.claude/agents/` / `~/.claude/agents/` files directly. The old interactive wizard (Running/Library tabs) is gone. Do not teach a wizard. |
| `Explore` | Built-in read-only search subagent | invoked automatically; or `Use the Explore subagent to ...`; `@agent-<name>` for custom agents | https://code.claude.com/docs/en/sub-agents#built-in-subagents | 2026-11-18 | Other built-ins: `Plan`, `general-purpose`, `claude`, `statusline-setup`, `claude-code-guide`. Disable: `permissions.deny: ["Agent(Explore)"]`. Custom agents: `.claude/agents/<name>.md` with `name`+`description` frontmatter. |
| `WebSearch` | Web search tool | tool name `WebSearch` (permission rule `WebSearch`, no specifier) | https://code.claude.com/docs/en/tools-reference | 2026-11-18 | Available by default; asks permission (saved per repository). |
| `WebFetch` | URL fetch tool | tool name `WebFetch`; rule `WebFetch(domain:example.com)` | https://code.claude.com/docs/en/tools-reference | 2026-11-18 | Asks permission except preapproved documentation domains. |
| `/code-review` | Local code review | `/code-review [low\|medium\|high\|xhigh\|max\|ultra] [--fix] [--comment] [--max-findings n\|all\|default] [pr#\|branch\|path]` | https://code.claude.com/docs/en/code-review-local | 2026-11-18 | BUILT-IN (bundled skill), alias `/review`; works on any plan; runs as background subagent; counts toward plan usage. A project skill of the same name overrides it. `ultra` runs a cloud review. Reviews current branch + uncommitted changes by default. Not the "NOT BUILT-IN" case. |
| `/security-review` | Security review of branch changes | `/security-review` | https://code.claude.com/docs/en/commands | 2026-11-18 | Diffs against origin's default branch; needs an `origin` remote. |
| `claude -p` | Non-interactive print mode | `claude -p "query"`; `cat f \| claude -p "query"` | https://code.claude.com/docs/en/cli-reference | 2026-11-18 | Local `-p, --print` confirmed. Combine `claude -c -p "..."`. |
| `claude --continue` | Continue most recent conversation | `claude -c` / `claude --continue` | https://code.claude.com/docs/en/cli-reference | 2026-11-18 | Scoped to current directory. Local confirmed. |
| `claude --resume` | Resume by ID/name or picker | `claude -r ["<session>"]` / `claude --resume`; in-session `/resume [session]` | https://code.claude.com/docs/en/cli-reference | 2026-11-18 | Local confirmed. |
| `/plugin` | Plugin manager ("where next") | `/plugin`; `/plugin install <name>@<marketplace>`; `/plugin list\|enable\|disable` | https://code.claude.com/docs/en/plugins/install | 2026-11-18 | In a session `/plugin install ...` opens the panel for review rather than installing at once. Example: `/plugin install commit-commands@claude-plugins-official`. Also shell `claude plugin ...`. |
| `disableAllHooks` | Turn all hooks off (one session) | `claude --settings '{"disableAllHooks": true}'`; or `"disableAllHooks": true` in a settings file | https://code.claude.com/docs/en/hooks#disable-or-remove-hooks | 2026-11-18 | `--settings` takes inline JSON or a file path and sits above local/project/user settings for that session only. Cannot disable managed hooks. No per-hook disable. |
| `workspace trust (hooks)` | Hooks wait for folder trust | accept the workspace trust dialog on first interactive `claude` in the folder | https://code.claude.com/docs/en/hooks#workspace-trust | 2026-11-18 | Interactive: hooks from every settings file (even `~/.claude/settings.json`) are held back until trust is accepted. `-p`/SDK: no dialog, hooks run. Observed locally (2.1.327): in an untrusted folder `-p` prints `Ignoring N permissions.allow entries from .claude/settings.json: this workspace has not been trusted` while hooks still run. |
| `Stop exit 2 + empty stdout` | Stop-hook block can be downgraded | always print a line to stdout when a Stop hook exits 2 | https://code.claude.com/docs/en/hooks#exit-code-output | 2026-11-18 | Stop/SubagentStop/TaskCompleted: exit 2 with nothing on stdout and stderr saying a file is missing (`No such file or directory`) is treated as a non-blocking error. Plain-text stdout + exit 2 is still blocking with stderr as the reason. |
| `Read deny limits` | What Read/Edit deny rules do not cover | `Read(**/.env)`, `Read(**/secrets/**)` | https://code.claude.com/docs/en/permissions#read-and-edit | 2026-11-18 | Applies to built-in file tools, recognised Bash file commands (`cat`, `head`, `sed`...) and redirections. Not to `grep -r` run without naming the file, nor to Python/Node scripts that open files. Use the sandbox for OS-level enforcement. Bare/`**/` patterns match at any depth under cwd. |

## Schema details

Sources: hooks https://code.claude.com/docs/en/hooks ; permissions https://code.claude.com/docs/en/permissions ; settings https://code.claude.com/docs/en/settings ; tools https://code.claude.com/docs/en/tools-reference

### settings.json hooks structure (event -> matcher group -> handlers)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/format.sh", "timeout": 600 }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/check-done.sh" }
        ]
      }
    ]
  }
}
```

- Handler `type` values: `command`, `http`, `mcp_tool`, `prompt`, `agent`. Optional per-handler `if` (permission-rule syntax, e.g. `"Edit(*.ts)"`) and `timeout` (seconds; default 600).
- Hook events (33 listed): SessionStart, Setup, SessionEnd, UserPromptSubmit, UserPromptExpansion, Stop, StopFailure, PreToolUse, PermissionRequest, PermissionDenied, PostToolUse, PostToolUseFailure, PostToolBatch, SubagentStart, SubagentStop, TaskCreated, TaskCompleted, TeammateIdle, PreCompact, PostCompact, PreModelSwitch, PostModelSwitch, Notification, MessageDisplay, InstructionsLoaded, ConfigChange, CwdChanged, DirectoryAdded, FileChanged, WorktreeCreate, WorktreeRemove, Elicitation, ElicitationResult. Event names are case-sensitive; an unknown event name yields a Settings Warning and is skipped.
- Settings files hooks may live in: `~/.claude/settings.json`, `.claude/settings.json`, `.claude/settings.local.json`. Settings are strict JSON (no comments, no trailing commas) and hot-reload.

### Matcher syntax

- For tool events (PreToolUse, PostToolUse, PostToolUseFailure, PermissionRequest, PermissionDenied) the matcher filters on tool name.
- Only letters, digits, `_`, `-`, spaces, `,`, `|` -> treated as exact name or list (`Edit|Write`). Any other character -> JavaScript regex, unanchored (`mcp__.*`).
- Omit matcher or use `"*"` -> fires on every occurrence.
- File-editing tool names: `Edit`, `Write` (and `NotebookEdit` for notebooks). `MultiEdit` is NOT in the current tools reference; permissions doc calls it "legacy". Recommended PostToolUse matcher for formatting: `"Edit|Write"`.
- PostToolUse does not fire when a Bash command or outside process rewrites a file; use `FileChanged` for that.

### Stdin JSON (command hooks receive JSON on stdin)

Common fields: `session_id`, `prompt_id`, `transcript_path`, `cwd`, `permission_mode`, `hook_event_name`. Tool events add `tool_name`, `tool_input`, `tool_use_id`.

PostToolUse for Write (documented example):

```json
{
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": { "file_path": "/path/to/file.txt", "content": "file content" },
  "tool_response": { "filePath": "/path/to/file.txt", "type": "create" },
  "tool_use_id": "toolu_01ABC123...",
  "duration_ms": 12
}
```

- File path is `tool_input.file_path` (Edit also has `old_string`, `new_string`, `replace_all`). Extract with `jq -r '.tool_input.file_path'`. Note `tool_response` uses camelCase `filePath`.
- Stop input adds: `stop_hook_active` (boolean, true when Claude is already continuing because of a stop hook), `last_assistant_message`, `background_tasks`, `session_crons`.

```json
{ "session_id": "abc123", "transcript_path": "...", "cwd": "/...", "permission_mode": "default",
  "hook_event_name": "Stop", "stop_hook_active": true, "last_assistant_message": "..." }
```

- Guard against loops: if `stop_hook_active` is true, exit 0. Claude Code also caps at 8 consecutive stop-hook continuations (`CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` raises it).

### Exit codes

| Event | 0 | 2 | other |
| :- | :- | :- | :- |
| PostToolUse | success; stdout JSON applied if valid | stderr shown to Claude; nothing blocked (tool already ran) | non-blocking error; execution continues |
| Stop | Claude stops normally | blocks the stop; Claude keeps working, stderr is the reason | non-blocking error; Claude stops normally |
| PreToolUse | allow | blocks the call (like deny); stderr to Claude | non-blocking error |

Exit 2 plus `continue: false` JSON on Stop ends the turn (continue:false wins). Stop JSON alternative: `{"decision":"block","reason":"..."}` (only value for `decision` is `"block"`; omit to allow); `hookSpecificOutput.additionalContext` gives non-error feedback and continues.

### Project directory env var

`CLAUDE_PROJECT_DIR`, referenced as `${CLAUDE_PROJECT_DIR}` in `command`; exported to the hook process. Plugins use `${CLAUDE_PLUGIN_ROOT}` / `${CLAUDE_PLUGIN_DATA}`.

### Permission rule syntax

```json
{
  "permissions": {
    "allow": ["Bash(npm run *)", "Bash(git commit *)", "Bash(npm run build)"],
    "ask":   ["Bash(git push *)"],
    "deny":  ["Read(./.env)", "Read(./.env.*)", "Read(./secrets/**)", "Bash(aws *)"]
  }
}
```

- Bash: `*` matches any text incl. spaces; no `*` = exact command. `Bash(ls *)` matches `ls` and `ls -la`, not `lsof`; `Bash(ls*)` matches `lsof`. `Bash(ls:*)` is an equivalent legacy trailing-wildcard form (only recognized at the end). Put `*` after the subcommand (`Bash(git log *)`). Deny/ask rules match any subcommand of a compound command; allow rules are per subcommand.
- Read/Edit path forms: `//abs/path` (absolute), `~/path` (home), `/path` (relative to primary working dir / settings anchor), `./path` or `path` (relative to cwd). Deny/ask `Read(secrets/**)` matches a `secrets` dir at any depth; allow `Read(src/**)` matches only `<cwd>/src`. Use `**` for recursion. `Write`/`NotebookEdit` rules are written as `Edit(...)`; `Grep`/`Glob` rules as `Read(...)`.
- Evaluation: deny, then ask, then allow; first match wins; specificity does not matter. A bare tool name in deny (e.g. `Bash`) removes the tool entirely.
- Settings files with `permissions.defaultMode` values: `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`.

### Local CLI corroboration (claude 2.1.327)

`claude --help` lists `-c/--continue`, `-r/--resume [value]`, `-p/--print`, `--effort <level>`, `--permission-mode <mode>`, and subcommands `doctor`, `install`, `update|upgrade`.
