# Appendix C: Common problems

Find your symptom, try the fix, then re-run the step that failed. If nothing here
helps: `claude doctor` in your shell, `/doctor` inside a session, and the official
troubleshooting pages at https://code.claude.com/docs/en/troubleshooting.

## Install and setup

### `claude: command not found`

The install worked, but your shell can't find it. Open a **new** terminal first;
the old one doesn't know about the new command. If it still fails, put the
install folder on your PATH once:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
claude --version
```

If `which -a claude` lists more than one path, you have two installs. Session 0,
Path B, step 1, shows how to keep only the native one.

### The install command fails or prints HTML

`curl -fsSL https://claude.ai/install.sh | bash` needs direct HTTPS access to
the internet. On a network with a proxy, see "Behind a proxy" below. Then run
`claude doctor`, which checks the installation and your settings files.

### `uv: command not found`

Install it (Session 0, section 2), then **open a new terminal**. The installer
puts `uv` in `~/.local/bin`; if a new terminal still can't find it, add that
folder to your PATH with the same two lines as for `claude` above.

### `reference` branch missing

`git show reference:...` fails with `fatal: invalid object name 'reference'`.
A clone creates only `main` locally. From the repository root:

```bash
git branch --track reference origin/reference
```

If you already renamed `origin` to `upstream` (Session 5), use
`upstream/reference` instead of `origin/reference`.

### `Author identity unknown` when you commit

Git doesn't know your name yet. Set it once, then repeat the commit:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## Login

- **No browser opens** (SSH, remote machine): at the login prompt press `c` to
  copy the URL, open it in any browser, sign in, and paste the code at
  `Paste code here`.
- **`OAuth error: Invalid code`**: the code expired or was cut off when you
  copied it. Try again, and paste it soon after it appears.
- **Logged in, but requests fail with a 403**: check that your Max subscription
  is active at https://claude.ai/settings. The free plan doesn't include Claude
  Code. Behind a proxy, also see below.
- **Asked to log in again and again**: check your system clock is right (token
  checks depend on it).
- **Anything else:** reset the login. Run `/logout`, leave with `/exit`, start
  `claude` and log in again.

## Usage limits

You see a message such as `You've hit your session limit · resets 3:45pm` or
`You've hit your weekly limit`. Claude Code blocks requests until the time shown.

- Run `/usage` to see your limits and when they reset.
- If the message names one model family (`You've hit your Opus limit`), you can
  keep working by picking a different model with `/model`. Session and weekly
  limits are shared by all models, so switching doesn't help there.
- Next time, use less: `/clear` between tasks, `/effort auto` after a debugging
  stretch (high effort stays on until you change it), and fewer parallel
  subagents. Session 0, section 7, has the details.

## Permission prompts

| What happens | Why | What to do |
| :- | :- | :- |
| Claude asks before every edit and every command | That's Manual mode, as intended in this guide | Read each one. **Yes** for this one action. |
| You chose "don't ask again" for something you now regret | The rule was saved in `.claude/settings.local.json` | Run `/permissions`, find the rule and remove it. |
| Claude still asks for `uv run pytest` after you copied the team settings | Project allow rules wait until you trust the folder, and settings load at the start of a session | Start a new session in `practice/` and accept the trust prompt if it appears. |
| Claude asks again for a command you allowed | Allow rules match the start of the command. A different command doesn't match, and in a chain (`a && b`) every part must be allowed | Read it and answer; that's the prompt doing its job. |
| You pressed **No** by mistake | Claude didn't do it, and waits for your instructions | Tell it to go ahead, or what to do instead. |
| The status bar shows `auto mode on` | New sessions start in auto unless you set Manual | Redo "Make Manual your starting mode", Session 0, section 4. |

## Claude goes in circles

Signs: the same fix tried three times, the tests going red and green and red
again, or edits to files that have nothing to do with the task.

1. Press `Esc` to stop it.
2. `/rewind` (or `Esc` twice on an empty prompt) and go back to the last prompt
   before it went wrong, with **Restore code and conversation**.
3. Or start clean: `/clear`, then restate the task in one message with what you
   now know: the spec, the exact failing output, and what not to do ("do not
   modify the tests").
4. Make the step smaller, or plan it first in plan mode (`Shift+Tab`). For one hard
   question, put `ultrathink` in the prompt.

Never get out of a loop by telling Claude to "make the tests pass".

## Context full

You see `Context limit reached · /compact or /clear to continue`, or Claude
starts forgetting things you said earlier.

- `/context` shows how full the window is and what is using it.
- Same task: `/compact`, optionally saying what to keep, for example
  `/compact keep the spec and the last test failure`.
- New task: `/clear`.
- Big lookups (docs, searching the whole codebase): ask for a subagent
  (Session 4, section 3), so only its summary lands in your conversation.

## Hooks

### Hooks don't run

Run `/hooks` in the session, then go through these.

- **No hooks listed:** the session started before you copied `.claude/` into
  `practice/`, or you started Claude in another folder. Leave with `/exit` and
  run `claude` again in `practice/`. Check `ls .claude/hooks` there lists both
  scripts.
- **Started with hooks off:** a session started with
  `claude --settings '{"disableAllHooks": true}'` runs no hooks. Leave it and
  start a plain `claude`.
  Also check your personal `~/.claude/settings.json` doesn't contain
  `"disableAllHooks": true`.
- **Folder not trusted:** Claude Code runs no project hooks until you accept the
  trust prompt for the folder. Start `claude` in `practice/` and accept it if
  it appears.
- **A warning that the hook failed, or `Permission denied`:** the scripts must
  be executable. From `practice/`:

  ```bash
  ls -l .claude/hooks
  chmod +x .claude/hooks/*.sh
  ```

  The line for each script should start with `-rwx`.
- **`uv not found on PATH`** from a hook: Claude Code was started from a
  terminal where `uv` isn't on the PATH. Fix PATH (see `uv: command not found`)
  and start Claude again.

### The Stop hook keeps blocking

The Stop hook sends Claude back to work once when tests fail. If Claude tries to
stop again while they still fail, the hook lets it stop, so it can't loop forever.

- **You want a failing test for now** (test-first, red step): do that step in a
  session started with `claude --settings '{"disableAllHooks": true}'`
  (Sessions 4 and 5).
- **The tests really fail:** run `uv run pytest` yourself in your second
  terminal and read the failure. It may be a test from an earlier step that
  you never got green.
- **Claude keeps "fixing" after the push-back and you want it to stop:**
  press `Esc`, then tell it what to do.
- **Every turn is slow:** the hook runs the whole suite each time Claude
  finishes. In a project with slow tests, see "What you may need to change in
  the real project" in Session 5, section 7.

## Session 5: GitHub and review

- **`gh repo create` says it can't add remote `origin`:** your clone still has
  the guide repository as `origin`. Run `git remote rename origin upstream`,
  then the `gh repo create` command again.
- **`/security-review` fails with `ambiguous argument 'origin/HEAD...'`:**
  your clone doesn't know `origin`'s default branch. From the repository root:

  ```bash
  git fetch origin
  git remote set-head origin --auto
  ```

  Then run `/security-review` again.
- **`uv run sensorlog` prints `Failed to spawn: sensorlog`:** the
  `[project.scripts]` lines are missing from `pyproject.toml`, or you didn't run
  `uv sync` after adding them (Session 5, section 2).
- **`gh repo delete` fails with a missing scope:** run
  `gh auth refresh -s delete_repo` first.

## Behind a proxy

This guide assumes direct internet access. If your network needs a proxy, tell
Claude Code and uv where it is before you start them, and add the line to
`~/.bashrc` so every new terminal has it:

```bash
export HTTPS_PROXY=http://proxy.example.com:8080
curl -I https://api.anthropic.com
```

The `curl` line should print an HTTP status line, not a connection error. If the
proxy needs a login, put it in the URL:
`http://user:password@proxy.example.com:8080`.

If you see `SSL certificate verification failed` or
`unable to get local issuer certificate`, your network inspects HTTPS traffic
with its own certificate. Ask IT for the CA certificate file, then:

```bash
export NODE_EXTRA_CA_CERTS=/path/to/company-ca.pem
export UV_NATIVE_TLS=true
```

The first is for Claude Code; the second makes uv use the system's certificate
store (install the certificate there too, as IT describes). Don't turn
certificate checks off. Details: https://code.claude.com/docs/en/network-config
