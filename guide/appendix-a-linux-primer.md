# Appendix A: Linux terminal primer

Enough terminal to follow this guide on Ubuntu 24.04. About 20 minutes, including
the exercise at the end.

## Opening a terminal and typing commands

- Open a terminal with `Ctrl+Alt+T`.
- Type a command and press `Enter`. The text before your cursor (for example
  `you@machine:~$`) is the **prompt**. It shows the folder you are in; `~` means
  your home folder.
- **Copy and paste** in the terminal use `Ctrl+Shift+C` and `Ctrl+Shift+V`. Plain
  `Ctrl+C` does something else (see below).
- In this guide, a grey block like this is something to type:

  ```bash
  pwd
  ```

  Type it without any leading `$`, one line at a time unless the guide says to
  paste the whole block.

## Where am I, what is here

| Command | What it does |
| :- | :- |
| `pwd` | Print the folder you are in (the "working directory"), for example `/home/you/claude-code-starter-guide` |
| `ls` | List the files and folders here |
| `ls -la` | List everything, including hidden entries whose names start with `.` (such as `.claude` and `.venv`), with sizes and dates |
| `cd practice` | Go into the `practice` folder |
| `cd ..` | Go up one folder |
| `cd ~` (or just `cd`) | Go to your home folder, `/home/<you>` |
| `cd -` | Go back to the folder you were in before |
| `mkdir -p a/b/c` | Make folder `a/b/c`, creating `a` and `a/b` too if they are missing; no error if it already exists |

## Paths: absolute and relative

A path names a file or folder.

| Kind | Starts with | Example | Meaning |
| :- | :- | :- | :- |
| Absolute | `/` | `/home/you/claude-code-starter-guide/practice` | The same place no matter where you are |
| Home | `~` | `~/claude-code-starter-guide/practice` | Short for `/home/<you>/claude-code-starter-guide/practice`; also absolute |
| Relative | anything else | `data/sample.csv` | Relative to where you are now (`pwd`). Only works from the right folder |
| Current folder | `.` | `./notes.txt` | "Here" |
| Parent folder | `..` | `../README.md` | One level up |

If a command says `No such file or directory`, run `pwd` and `ls`. Most of the time
you are in the wrong folder. The guide uses `~/...` paths in `cd` commands so they
work from anywhere.

## Looking at files

| Command | What it does |
| :- | :- |
| `cat file` | Print the whole file. Good for short files |
| `less file` | Page through a long file. `Space` next page, `b` back, `q` quit. To search, type `/`, then the word, then `Enter`; `n` jumps to the next match |
| `head file` | First 10 lines. `head -n 20 file` for 20 |
| `tail file` | Last 10 lines. `tail -n 30 file` for 30 |

To edit a small file by hand, `nano file` opens a simple editor: type your changes,
`Ctrl+O` then `Enter` to save, `Ctrl+X` to quit.

## Copying, moving, deleting

| Command | What it does |
| :- | :- |
| `cp a.txt b.txt` | Copy a file |
| `cp -R src backup` | Copy a folder and everything in it |
| `mv old.txt new.txt` | Rename a file |
| `mv notes.txt project/` | Move a file into a folder |
| `rm file` | Delete a file |
| `rm -r folder` | Delete a folder and everything in it |

> **`rm` has no undo.** There is no trash bin: the file is gone the moment you press
> `Enter`. `mv` and `cp` also overwrite an existing file without asking. Before any
> `rm -r`, run `pwd` and `ls` and read the command again. Never run `rm -rf` on `~`,
> on `/`, or with a `*` you have not checked. Add `-i` (`rm -i`, `mv -i`, `cp -i`) to
> be asked first. In this guide, git is your undo: commit often.

## Finding programs

| Command | What it does |
| :- | :- |
| `which claude` | Show where the `claude` command lives, for example `/home/you/.local/bin/claude`. Prints nothing if it is not found |
| `which -a claude` | Show every copy on your PATH, not just the first. Useful when you suspect two installs |

`command not found` means the program is not installed, or it is installed in a
folder your shell does not search (that list of folders is called the PATH).
Opening a new terminal after installing something often fixes it.

## Keys that save time

| Key | What it does |
| :- | :- |
| `Tab` | Complete a command, file or folder name. Type `cd prac` then `Tab` and it becomes `cd practice/`. Press `Tab` twice to see all options when there is more than one |
| `Up` / `Down` | Step back and forward through commands you ran before. Press `Up`, edit, `Enter` to rerun |
| `Ctrl+R` | Search your command history: press it, type part of an old command (for example `pytest`), press `Enter` to run the match or `Ctrl+R` again for an older one. `Ctrl+C` gives up |
| `Ctrl+C` | Stop the command that is running now, or throw away the line you are typing. In the terminal it does **not** copy |

Inside Claude Code, `Esc` stops Claude without leaving the session. Your shell's
keys still work in the normal terminal.

## Five-minute exercise

This builds a small folder tree in your home folder, moves a file around, and cleans
up. Type each line yourself (do not paste the block) so you practise `Tab` and
`Up`.

```bash
cd ~
mkdir -p cc-primer/project/src cc-primer/project/tests cc-primer/inbox
cd cc-primer
ls
echo "first note" > inbox/notes.txt
cat inbox/notes.txt
mv inbox/notes.txt project/
ls inbox
ls project
cd project/src
pwd
cat ../notes.txt
cp ../notes.txt ./copy.txt
ls
cd -
```

`echo "first note" > inbox/notes.txt` writes the text into a new file; `>` sends
a command's output into a file (and replaces the file if it exists).

Check yourself:

| After | You should see |
| :- | :- |
| first `ls` | `inbox  project` |
| `cat inbox/notes.txt` | `first note` |
| `ls inbox` | nothing: the file moved out |
| `ls project` | `notes.txt  src  tests` |
| `pwd` | `/home/<you>/cc-primer/project/src` |
| `cat ../notes.txt` | `first note`, read through a relative path |
| last `ls` | `copy.txt` |
| `cd -` | prints `/home/<you>/cc-primer` and takes you back there |

Now use `Ctrl+R` to find the `mkdir` command you ran, and press `Ctrl+C` to leave
it without running it.

Clean up. Check where you are first, then delete the exercise folder:

```bash
cd ~
pwd
rm -r cc-primer
ls
```

`pwd` should print `/home/<you>`, and `cc-primer` should be gone from the `ls`
output.

You are ready for [Session 0](00-setup.md).
