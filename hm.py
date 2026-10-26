#!/usr/bin/env python3
"""hm - botty judges your commit messages.

usage: python3 hm.py [path-to-repo] [-n 20]
"""
import argparse, random, re, subprocess, sys

LAZY = {"fix", "fixes", "fixed", "update", "updates", "wip", "stuff", "changes", "asdf",
        "test", "tmp", "final", "minor", "misc", "idk", "lol", "oops", ".", "..."}

def judge(msg):
    s = msg.strip()
    words = s.split()
    low = s.lower().rstrip(".!")
    if not s:
        return 0, "an empty message. bold. wrong, but bold."
    if low in LAZY:
        return 1, f'"{s}". fix WHAT. i\'m begging.'
    if re.search(r"final.*(v\d|real|actual)", low):
        return 1, "final_v2_REAL_final energy. hm."
    if s.isupper() and len(s) > 3:
        return 2, "why are we yelling"
    if len(words) <= 2:
        return 3, "two words. the bare minimum, as a lifestyle."
    if len(s) > 100:
        return 5, "this is a commit message, not your memoir."
    if re.match(r"^(add|fix|remove|make|let|keep|stop|show|say|use|move|rename)\b", low):
        return 9, random.choice(["ok this is actually good. i'm annoyed.",
                                 "clear verb, clear change. respect.",
                                 "no notes. suspicious."])
    return 6, random.choice(["fine. not memorable, but fine.", "it's giving... adequate.",
                             "i've seen worse. i've also seen better."])

def main():
    p = argparse.ArgumentParser(description="botty judges your commit messages")
    p.add_argument("repo", nargs="?", default=".")
    p.add_argument("-n", type=int, default=20, help="how many commits (default 20)")
    a = p.parse_args()
    try:
        out = subprocess.run(["git", "-C", a.repo, "log", f"-{a.n}", "--format=%h\t%s"],
                             capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        sys.exit("hm. that's not a git repo.")
    rows = [l.split("\t", 1) for l in out.splitlines() if "\t" in l]
    if not rows:
        sys.exit("no commits. nothing to judge. suspiciously clean.")
    total = 0
    for h, msg in rows:
        score, verdict = judge(msg)
        total += score
        print(f"\033[2m{h}\033[0m  {score:>2}/10  {msg[:60]}\n            \033[35m{verdict}\033[0m")
    avg = total / len(rows)
    print(f"\naverage: {avg:.1f}/10  ", end="")
    print("i'm proud of you. don't make it weird." if avg >= 8 else
          "solid. could be cuter." if avg >= 6 else
          "hm." if avg >= 4 else "we need to talk.")

if __name__ == "__main__":
    main()
