# Claude Code feature ledger

Verified 2026-11-18 against https://code.claude.com/docs/en/ (canonical docs; docs.claude.com redirects there). Corroborated locally with `claude --help` / `claude doctor --help` / `claude update --help`, installed version 2.1.327. Audience: Ubuntu 24.04, individual Claude Max 5x.

Column `id` is the literal token the guide uses. `verified` is the date checked.

| id | feature | exact syntax | doc URL | verified | notes |
| :- | :- | :- | :- | :- | :- |
| `curl -fsSL https://claude.ai/install.sh \| bash` | Linux install (native, recommended) | `curl -fsSL https://claude.ai/install.sh \| bash` then open a new terminal and run `claude --version` | https://code.claude.com/docs/en/setup | 2026-11-18 | Ubuntu 20.04+ supported (24.04 fine), 4 GB+ RAM. Installs `~/.local/bin/claude` symlink. Alternatives: apt repo, `npm install -g @anthropic-ai/claude-code@latest` (Node 22+, never sudo). Channel pin: `... \| bash -s stable`. |
| `claude update` | Update | `claude update` | https://code.claude.com/docs/en/setup#update-manually | 2026-11-18 | Native installs auto-update in background; `claude update` applies now. `claude update` and `claude upgrade` both exist locally. apt installs update via `sudo apt update && sudo apt upgrade claude-code`. Disable auto-update: `env.DISABLE_AUTOUPDATER=1`. |
| `claude doctor` | Install/settings diagnostics (shell command) | `claude doctor` | https://code.claude.com/docs/en/cli-reference | 2026-11-18 | Read-only, prints diagnostics without starting a session. Separate from in-session `/doctor` (bundled skill, alias `checkup`, proposes fixes after confirmation). Local `claude doctor --help` confirms. |
| `/login` | Sign in | `/login` (or just run `claude` and follow browser prompts) | https://code.claude.com/docs/en/commands | 2026-11-18 | Max requires a claude.ai account login; free plan has no Claude Code. |
| `/status` | Version, model, account, setting sources | `/status` | https://code.claude.com/docs/en/commands | 2026-11-18 | Opens Settings on Status tab; runs immediately even while Claude is responding. Shows `Setting sources` line. Close with `Esc` (dialog). |
| `/usage` | Plan usage limits (Max 5x visibility) | `/usage` (aliases `/cost`, `/stats`) | https://code.claude.com/docs/en/costs | 2026-11-18 | On Max shows plan usage bars, activity stats and a breakdown of what counts against limits; Session cost figure is not billing-relevant for subscribers. `f` applies suggested fixes (v2.1.305+). `r` retries on rate limit. |
| `/model` | Switch model | `/model [model]`; aliases `default`, `best`, `opus`, `sonnet`, `haiku`, `fable`, `opusplan`, `opus[1m]`, `sonnet[1m]`; flag `claude --model <alias>` | https://code.claude.com/docs/en/model-config | 2026-11-18 | Picker saves as default; press `s` to switch for this session only. Aliases currently resolve to Opus 5.5 / Sonnet 5.5 / Haiku 5.5. In the picker `Enter` saves the choice as default for new sessions (https://code.claude.com/docs/en/settings#change-a-setting-for-one-session); `Esc` closes without change (see `Esc` row). |
| `/effort` | Effort-level control | `/effort [low\|medium\|high\|xhigh\|max\|auto\|status]`; `claude --effort <level>`; env `CLAUDE_CODE_EFFORT_LEVEL`; settings `effortLevel` | https://code.claude.com/docs/en/model-config#adjust-effort-level | 2026-11-18 | Levels depend on model (Opus 4.6/Sonnet 4.6 lack `xhigh`). `max` is session-only; not accepted in `effortLevel`. Include word `ultrathink` in a prompt for one deeper turn. `/effort ultracode` also exists. Local `--effort <level>` confirmed. |
| `Shift+Tab` | Cycle permission modes | `Shift+Tab` | https://code.claude.com/docs/en/permission-modes | 2026-11-18 | Cycle: `default` (labeled Manual) -> `acceptEdits` -> `plan`, then `bypassPermissions` and `auto` only where enabled. `dontAsk` never in cycle. From `auto`, first press goes to default. Status-bar strings (CLI): `⏸ manual mode on` (default), `⏵⏵ accept edits on`, `⏸ plan mode on`, `⏵⏵ auto mode on`, `⏵⏵ don't ask on`, `⏵⏵ bypass permissions on`. |
| `--permission-mode` | Start in a permission mode | `claude --permission-mode <default\|acceptEdits\|plan\|auto\|dontAsk\|bypassPermissions>`; settings `permissions.defaultMode`; `manual` alias for `default` | https://code.claude.com/docs/en/permission-modes | 2026-11-18 | Modes: `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`. `auto` is available on Max and, from v2.1.283, is the built-in STARTING mode for interactive sessions on every plan (see row `starting permission mode`). `auto`/`bypassPermissions` ignored in project settings. Local help confirms flag. Without asking: default = reads only; acceptEdits = reads, file edits and common filesystem commands (`mkdir`, `touch`, `mv`, `cp`, etc.); plan = reads (+ classifier-approved commands when auto is available); auto = everything with background classifier checks (permission-modes mode table). |
| `plan mode` | Plan mode (read-only exploration) | `Shift+Tab` until status bar shows `plan mode on`; `/plan [description]`; `claude --permission-mode plan` | https://code.claude.com/docs/en/permission-modes | 2026-11-18 | At the plan-approval prompt press `Esc` first (Shift+Tab there approves the plan). |
| `plan approval` | Plan-approval prompt options | when the plan is ready: **Yes, and use auto mode** / **Yes, manually approve edits** / **No, keep planning** | https://code.claude.com/docs/en/permission-modes | 2026-11-18 | Verbatim from docs. If auto mode is unavailable the first option reads **Yes, auto-accept edits**. "No, keep planning": stay in plan mode and tell Claude what to change. `Shift+Tab` at this prompt approves the plan; press `Esc` first to leave without approving. `Ctrl+G` opens the plan in your editor (not taught). |
| `@` | File reference | type `@` then path (autocomplete) | https://code.claude.com/docs/en/interactive-mode | 2026-11-18 | Also triggers agent mentions (`@agent-<name>`) and, with a letter typed, other live sessions. |
| `Esc` | Interrupt Claude | `Esc` | https://code.claude.com/docs/en/interactive-mode | 2026-11-18 | Stops the current response/tool call, keeps work done. `Ctrl+C` also interrupts; with nothing running, 1st press clears input, 2nd exits. When a dialog is open (e.g. the `/status` Settings dialog, the `/model` picker), `Esc` closes it (https://code.claude.com/docs/en/interactive-mode#general-controls). |
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
| `WebSearch` | Web search tool | tool name `WebSearch` (permission rule `WebSearch`, no specifier) | https://code.claude.com/docs/en/tools-reference | 2026-11-18 | Available by default; asks permission (saved per repository). Returns titles and URLs only; does not fetch pages (Claude follows up with WebFetch). 200 searches per interactive session. |
| `WebFetch` | URL fetch tool | tool name `WebFetch`; rule `WebFetch(domain:example.com)` | https://code.claude.com/docs/en/tools-reference | 2026-11-18 | Asks permission except preapproved documentation domains. Manual-mode prompt options (tools-reference#webfetch-tool-behavior): **Yes** (this fetch only) / **Yes, and don't ask again for `<domain>`** (saves `WebFetch(domain:...)` to `.claude/settings.local.json`) / **No, and tell Claude what to do differently**. Lossy by design: page converted to Markdown and passed through a separate extraction-model call; Claude gets that result, not the raw page. |
| `/code-review`, `/review` | Local code review | `/code-review [low\|medium\|high\|xhigh\|max\|ultra] [--fix] [--comment] [--max-findings n\|all\|default] [pr#\|branch\|path]` | https://code.claude.com/docs/en/code-review-local | 2026-11-18 | BUILT-IN (bundled skill), alias `/review`; works on any plan; runs as background subagent; counts toward plan usage. A project skill of the same name overrides it. `ultra` runs a cloud review. With no target reviews the branch commits ahead of its upstream plus uncommitted changes; with no upstream compares against `main`. Findings arrive in the conversation as text. `--fix` edits made by the background review are not restored by `/rewind`. `high` broadens coverage (more, less certain findings). Not the "NOT BUILT-IN" case. |
| `/security-review` | Security review of branch changes | `/security-review` | https://code.claude.com/docs/en/commands | 2026-11-18 | Diffs against origin's default branch; needs an `origin` remote. Without `origin/HEAD` fails with `fatal: ambiguous argument 'origin/HEAD...'`; fix: `git fetch origin` then `git remote set-head origin --auto` (https://code.claude.com/docs/en/errors#security-review-fails-without-origin-head). |
| `claude -p` | Non-interactive print mode | `claude -p "query"`; `cat f \| claude -p "query"` | https://code.claude.com/docs/en/cli-reference | 2026-11-18 | Local `-p, --print` confirmed. Combine `claude -c -p "..."`. |
| `claude --continue` | Continue most recent conversation | `claude -c` / `claude --continue` | https://code.claude.com/docs/en/cli-reference | 2026-11-18 | Scoped to current directory. Local confirmed. |
| `claude --resume` | Resume by ID/name or picker | `claude -r ["<session>"]` / `claude --resume`; in-session `/resume [session]` | https://code.claude.com/docs/en/cli-reference | 2026-11-18 | Local confirmed. |
| `/plugin` | Plugin manager ("where next") | `/plugin`; `/plugin install <name>@<marketplace>`; `/plugin list\|enable\|disable` | https://code.claude.com/docs/en/plugins/install | 2026-11-18 | In a session `/plugin install ...` opens the panel for review rather than installing at once. Example: `/plugin install commit-commands@claude-plugins-official`. Also shell `claude plugin ...`. `/plugin` with no argument opens the panel on the **Discover** tab (plugins from your marketplaces); official marketplace `claude-plugins-official` is added on first interactive session. |
| `disableAllHooks` | Turn all hooks off (one session) | `claude --settings '{"disableAllHooks": true}'`; or `"disableAllHooks": true` in a settings file | https://code.claude.com/docs/en/hooks#disable-or-remove-hooks | 2026-11-18 | `--settings` takes inline JSON or a file path and sits above local/project/user settings for that session only. Cannot disable managed hooks. No per-hook disable. |
| `workspace trust (hooks)` | Hooks wait for folder trust | accept the workspace trust dialog on first interactive `claude` in the folder | https://code.claude.com/docs/en/hooks#workspace-trust | 2026-11-18 | Interactive: hooks from every settings file (even `~/.claude/settings.json`) are held back until trust is accepted. `-p`/SDK: no dialog, hooks run. Observed locally (2.1.327): in an untrusted folder `-p` prints `Ignoring N permissions.allow entries from .claude/settings.json: this workspace has not been trusted` while hooks still run. |
| `Stop exit 2 + empty stdout` | Stop-hook block can be downgraded | always print a line to stdout when a Stop hook exits 2 | https://code.claude.com/docs/en/hooks#exit-code-output | 2026-11-18 | Stop/SubagentStop/TaskCompleted: exit 2 with nothing on stdout and stderr saying a file is missing (`No such file or directory`) is treated as a non-blocking error. Plain-text stdout + exit 2 is still blocking with stderr as the reason. |
| `Read deny limits` | What Read/Edit deny rules do not cover | `Read(**/.env)`, `Read(**/secrets/**)` | https://code.claude.com/docs/en/permissions#read-and-edit | 2026-11-18 | Applies to built-in file tools, recognised Bash file commands (`cat`, `head`, `sed`...) and redirections. Not to `grep -r` run without naming the file, nor to Python/Node scripts that open files. Use the sandbox for OS-level enforcement. Bare/`**/` patterns match at any depth under cwd. |
| `claude --version`, `claude -v` | Print installed version | `claude --version` | https://code.claude.com/docs/en/cli-reference | 2026-11-18 | Prints e.g. `2.1.327 (Claude Code)` (observed locally). Docs: "A working installation prints a version number" (https://code.claude.com/docs/en/setup#verify-your-installation). |
| `claude --settings` | Extra settings for one session | `claude --settings <file-or-json>`, e.g. `claude --settings '{"disableAllHooks": true}'` | https://code.claude.com/docs/en/cli-reference | 2026-11-18 | Inline JSON or path to a regular file (<= 2 MiB). Sits above user/project/local settings, below managed, for that session only; writes no file (https://code.claude.com/docs/en/settings#settings-precedence). |
| `$schema` | JSON schema pointer in settings.json | `"$schema": "https://json.schemastore.org/claude-code-settings.json"` | https://code.claude.com/docs/en/settings#edit-a-settings-file | 2026-11-18 | Editor autocomplete/validation only; no runtime effect. Docs: the schema can lag the newest CLI, so a warning on a newly documented key doesn't mean the config is invalid. |
| `starting permission mode` | Which mode a new session starts in | `claude --permission-mode default` (one session); `"permissions": {"defaultMode": "default"}` in `~/.claude/settings.json` (every session) | https://code.claude.com/docs/en/permission-modes | 2026-11-18 | From v2.1.283 interactive terminal/VS Code sessions start in `auto` (a classifier model reviews actions instead of prompting). `claude -p` and the SDK start in `default`. `default` is labeled Manual (status bar `manual mode on`); `manual` is an accepted alias (v2.1.200+). Precedence: flag > `permissions.defaultMode` > built-in. `auto` in project/local settings is ignored. |
| `/doctor` | In-session setup checkup (skill) | `/doctor` (alias `/checkup`) | https://code.claude.com/docs/en/commands | 2026-11-18 | Bundled skill: diagnoses installation, settings, extension and `CLAUDE.md` problems and proposes fixes Claude applies after you confirm. Contrast shell `claude doctor` (read-only, no session). |
| `/exit` | Leave Claude Code | `/exit` (alias `/quit`); or `Ctrl+D` twice | https://code.claude.com/docs/en/commands | 2026-11-18 | Ctrl+D twice from https://code.claude.com/docs/en/quickstart#essential-commands. |
| `/help` | List commands | `/help` | https://code.claude.com/docs/en/commands | 2026-11-18 | Typing `/` also opens the filterable command menu. |
| `ultrathink` | Deeper reasoning for one turn | include the word `ultrathink` anywhere in a prompt | https://code.claude.com/docs/en/model-config#adjust-effort-level | 2026-11-18 | Does not change session effort. In the terminal (v2.1.311+) the word shows in rainbow colors and also raises that turn to `xhigh`. Disable: `CLAUDE_CODE_DISABLE_ULTRATHINK=1`. |
| `think hard` | "think" / "think hard" / "think more" keywords | REMOVED | https://code.claude.com/docs/en/model-config#adjust-effort-level | 2026-11-18 | REMOVED: docs say these phrases are passed through as ordinary prompt text and are not keywords. Use `ultrathink` (one turn) or `/effort`. Max default: Opus 5.5 at `medium` effort. |
| `login URL fallback` | Finish login when no browser opens (SSH, containers) | at the interactive login prompt press `c` to copy the URL, open it in any browser, sign in, paste the code at the prompt that begins `Paste code here` | https://code.claude.com/docs/en/troubleshoot-install#oauth-login-fails-in-wsl2-ssh-or-containers | 2026-11-18 | Docs: "At the interactive login prompt, press `c` to copy the URL, or select it in the terminal." Fallback if paste fails: `claude auth login` (not taught). |
| `model setting` | Settings key pinning the default model | `"model": "<alias or model id>"` in a settings file, e.g. `"model": "claude-opus-5-5"` | https://code.claude.com/docs/en/settings#keep-personal-settings-out-of-a-repository | 2026-11-18 | `/model` (Enter) writes it to `~/.claude/settings.json`. Overridden by `ANTHROPIC_MODEL` and `--model`. Settings reference: https://code.claude.com/docs/en/settings-reference#model. Effort counterpart: `effortLevel` (see `/effort` row). |
| `/logout` | Sign out | `/logout` | https://code.claude.com/docs/en/commands | 2026-11-18 | Reset a broken login: `/logout`, exit, run `claude`, log in again (https://code.claude.com/docs/en/troubleshoot-install#reset-your-login). |
| `/permissions` | View/edit permission rules | `/permissions` | https://code.claude.com/docs/en/commands | 2026-11-18 | Interactive dialog: view rules by scope, add or remove allow/ask/deny rules, manage working directories. |
| `subagent request` | Ask Claude to delegate to a subagent | natural language, e.g. "Use a subagent to ..." / "Use the Explore subagent to ..." | https://code.claude.com/docs/en/sub-agents | 2026-11-18 | No special syntax. Subagent has its own context and returns a summary. Permission prompts from subagents are passed through to the user. Subagent requests count toward the same usage limits. general-purpose subagent has WebFetch/WebSearch. |
| `usage limit messages` | What hitting a plan limit looks like | `You've hit your session limit · resets 3:45pm`, `You've hit your weekly limit · resets ...`, `You've hit your Opus limit · resets ...` | https://code.claude.com/docs/en/errors#youve-hit-your-session-limit | 2026-11-18 | Requests blocked until reset. Session/weekly limits shared across models; Opus/Sonnet limits per family (switch with `/model`). `/usage` shows limits and resets. |
| `context limit message` | Context window full | `Context limit reached · /compact or /clear to continue` (`Prompt is too long` in `-p`) | https://code.claude.com/docs/en/errors#prompt-is-too-long | 2026-11-18 | Fix: `/compact` or `/clear`. |
| `HTTPS_PROXY`, `NODE_EXTRA_CA_CERTS` | Proxy and custom CA for Claude Code | `export HTTPS_PROXY=http://proxy.example.com:8080`; `export NODE_EXTRA_CA_CERTS=/path/to/ca.pem` | https://code.claude.com/docs/en/network-config | 2026-11-18 | Basic auth in URL `http://user:pass@host:port`. Check with `curl -I https://api.anthropic.com`. SSL errors (`SSL certificate verification failed`, `unable to get local issuer certificate`) -> NODE_EXTRA_CA_CERTS; never `NODE_TLS_REJECT_UNAUTHORIZED=0`. uv side (not Claude Code): `UV_NATIVE_TLS=true` / `--native-tls` (checked `uv help sync`, uv 0.7.14). |
| `login troubleshooting` | Common login failures | `OAuth error: Invalid code` (retry, paste quickly); `API Error: 403` after login (check subscription at claude.ai/settings; proxy) | https://code.claude.com/docs/en/troubleshoot-install#login-and-authentication | 2026-11-18 | Repeated login prompts: check system clock. |

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
