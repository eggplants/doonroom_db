"""https://qiita.com/nnsnodnb/items/9e99e7f0ca3f82bf2171"""

import sys


def chk_header(line: str) -> bool:
    """Check existance of header lines."""
    return any(
        (
            line.startswith("PRAGMA"),
            line.startswith("BEGIN TRANSACTION;"),
            line.startswith("COMMIT;"),
            line.startswith("DELETE FROM sqlite_sequence;"),
            line.startswith('INSERT INTO "sqlite_sequence"'),
        )
    )


def replace_sqlite_to_mysql(line: str) -> str:
    """Replace explessions of bools and auto increment."""
    return (
        line.replace("AUTOINCREMENT", "AUTO_INCREMENT")
        .replace("DEFAULT 't'", "DEFAULT '1'")
        .replace("DEFAULT 'f'", "DEFAULT '0'")
        .replace(",'t'", ",'1'")
        .replace(",'f'", ",'0'")
    )


def replace_quotes(line: str) -> str:
    """Fix differences of escape quotes."""
    in_string = False
    newLine = ""
    for c in line:
        if not in_string and c == "'":
            in_string = True
        elif not in_string and c == '"':
            newLine += "`"
            continue
        elif c == "'":
            in_string = False

        newLine += c

    return newLine


def main() -> None:
    """Main."""
    print("SET sql_mode='NO_BACKSLASH_ESCAPES';")
    for line in sys.stdin.read().splitlines():
        if not chk_header(line):
            print(replace_quotes(replace_sqlite_to_mysql(line)))


if __name__ == "__main__":
    main()
