"""Regenerate the README index from the notes in each topic folder."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
START, END = "<!-- index:start -->", "<!-- index:end -->"


def build() -> str:
    notes = sorted(p for p in ROOT.glob("*/*.md"))
    topics: dict[str, list[Path]] = {}
    for p in notes:
        topics.setdefault(p.parent.name, []).append(p)
    lines = [f"**{len(notes)} notes** across {len(topics)} topics", ""]
    for topic, files in sorted(topics.items()):
        lines.append(f"### {topic}")
        for f in files:
            title = f.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
            lines.append(f"- [{title}]({topic}/{f.name})")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    head, _, rest = text.partition(START)
    _, _, tail = rest.partition(END)
    readme.write_text(f"{head}{START}\n{build()}\n{END}{tail}", encoding="utf-8")


if __name__ == "__main__":
    main()
