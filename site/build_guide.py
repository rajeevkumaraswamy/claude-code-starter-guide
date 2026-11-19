"""Build the single-page HTML version of the guide from README.md and guide/*.md.

From the repository root:

    uv run --no-project --with markdown-it-py python site/build_guide.py

writes site/claude-code-starter-guide.html (pass another path to write elsewhere).
The page is self-contained apart from Google Fonts; open it in a browser or publish it.
"""

import html
import re
import sys
from pathlib import Path

from markdown_it import MarkdownIt

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
BLOB = "https://github.com/rajeevkumaraswamy/claude-code-starter-guide/blob/main/"

# (file, section id, eyebrow, short nav label)
PARTS = [
    ("README.md", "start", "Start here", "Overview"),
    ("guide/00-setup.md", "s0", "Session 0 · day 1", "0 · Setup"),
    ("guide/01-working-with-claude.md", "s1", "Session 1 · day 1 or 2", "1 · Working with Claude"),
    ("guide/02-test-first.md", "s2", "Session 2 · day 2", "2 · Test-first features"),
    ("guide/03-debugging-and-checks.md", "s3", "Session 3 · day 3", "3 · Debugging and checks"),
    ("guide/04-research.md", "s4", "Session 4 · day 4", "4 · Research"),
    ("guide/05-review-and-baseline.md", "s5", "Session 5 · day 5", "5 · Review and baseline"),
    ("guide/appendix-a-linux-primer.md", "a", "Appendix A", "A · Linux primer"),
    ("guide/appendix-b-cheat-sheet.md", "b", "Appendix B", "B · Cheat sheet"),
    ("guide/appendix-c-troubleshooting.md", "c", "Appendix C", "C · Common problems"),
]  # fmt: skip
SECTION_OF = {f: sid for f, sid, _, _ in PARTS}


def slug(text: str) -> str:
    """GitHub-style heading slug."""
    text = text.strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def resolve(href: str, src: str, prefix: str) -> str:
    """Turn a Markdown link into an in-page anchor or a GitHub file link."""
    if re.match(r"[a-z]+:", href):
        return href
    if href.startswith("#"):
        return f"#{prefix}-{href[1:]}"
    path, _, frag = href.partition("#")
    full = str(Path(src).parent / path).replace("\\", "/")
    full = re.sub(r"^\./", "", full)
    if full in SECTION_OF:
        sid = SECTION_OF[full]
        return f"#{sid}-{frag}" if frag else f"#{sid}"
    return BLOB + full  # a file in the repository


def render(text: str, src: str, prefix: str) -> tuple[str, list[tuple[str, str]]]:
    md = MarkdownIt("commonmark", {"html": True}).enable("table")
    tokens = md.parse(text)
    toc = []
    for i, tok in enumerate(tokens):
        if tok.type == "heading_open":
            inline = tokens[i + 1]
            plain = "".join(
                c.content for c in inline.children if c.type in ("text", "code_inline")
            )
            hid = f"{prefix}-{slug(plain)}"
            tok.attrSet("id", hid)
            if tok.tag == "h2":
                toc.append((hid, plain))
        if tok.type == "inline":
            for c in tok.children or []:
                if c.type == "link_open":
                    c.attrSet("href", resolve(c.attrGet("href"), src, prefix))
    out = md.renderer.render(tokens, md.options, {})
    out = out.replace("<table>", '<div class="tbl"><table>')
    out = out.replace("</table>", "</table></div>")
    out = out.replace("<pre><code", '<pre tabindex="0"><code')
    out = re.sub(r"<p>Pass:", '<p class="pass"><b class="chip-pass">Pass</b>', out)
    out = re.sub(
        r"<p><strong>Why:</strong>", '<p class="why"><b class="chip-why">Why</b>', out
    )
    return out, toc


def build(repo: Path = REPO) -> str:
    sections, nav = [], []
    for src, sid, eyebrow, label in PARTS:
        text = (repo / src).read_text()
        m = re.match(r"# (.+)\n", text)
        title = m.group(1) if m else label
        body = text[m.end() :] if m else text
        title = re.sub(r"^(Session \d|Appendix [A-C]): ", "", title)
        if src == "README.md":
            title = "How the guide works"
        rendered, toc = render(body, src, sid)
        contents = ""
        if src != "README.md" and len(toc) > 2:
            items = "".join(
                f'<li><a href="#{h}">{html.escape(t)}</a></li>' for h, t in toc
            )
            contents = (
                '<nav class="toc" aria-label="In this part">'
                f'<span class="eyebrow">In this part</span><ol>{items}</ol></nav>'
            )
        sections.append(
            f'<section class="doc" id="{sid}"><div class="doc-head">'
            f'<span class="eyebrow">{eyebrow}</span>'
            f"<h2>{html.escape(title)}</h2></div>{contents}{rendered}</section>"
        )
        nav.append(f'<li><a href="#{sid}">{html.escape(label)}</a></li>')
    page = (HERE / "guide_template.html").read_text()
    return page.replace("{{NAV}}", "\n".join(nav)).replace(
        "{{SECTIONS}}", "\n".join(sections)
    )


def main() -> None:
    out = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else HERE / "claude-code-starter-guide.html"
    )
    page = build()
    out.write_text(page)
    print(f"wrote {out} ({len(page)} bytes)")


if __name__ == "__main__":
    main()
