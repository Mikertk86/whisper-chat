#!/usr/bin/env python3
"""Patch prebuilt Android libsimplex.so artifacts for the Whisper fork.

The Android/KMP project consumes prebuilt native Haskell libraries from
apps/multiplatform/common/src/commonMain/cpp/android/libs/<abi>/libsimplex.so.
A full Android cross-build of these libraries is Nix/Hydra based and can take
many hours. This release-side patch is intentionally conservative: it only
performs equal-length byte replacements so ELF offsets/sections are not moved.

Canonical source defaults live in src/Simplex/Chat/Operators/Presets.hs. This
script is the reproducible transformation applied when packaging Android APKs
from prebuilt upstream native libraries.
"""
from __future__ import annotations

from pathlib import Path
import hashlib
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
LIB_ROOT = ROOT / "apps/multiplatform/common/src/commonMain/cpp/android/libs"

REPLACEMENTS: dict[bytes, bytes] = {
    b"simplexonflux.com": b"tailb34dd3.ts.net",
    b"simplex.im": b"whisper.li",
    b"Ask SimpleX Team": b"Whisper Support ",
    b"SimpleX Status": b"Whisper Status",
    b"SimpleX Chat Relay 1": b"Whisper Relay One   ",
    b"SimpleX Chat Relay 2": b"Whisper Relay Two   ",
    b"SimpleX Chat Relay 3": b"Whisper Relay Three ",
    b"SimpleX Chat Ltd": b"Whisper Relay   ",
}

FORBIDDEN = [
    re.compile(rb"smp[0-9]+\.simplex\.im"),
    re.compile(rb"smp[0-9]+\.simplexonflux\.com"),
    re.compile(rb"xftp[0-9]+\.simplex\.im"),
    re.compile(rb"xftp[0-9]+\.simplexonflux\.com"),
    re.compile(rb"simplexonflux\.com"),
    re.compile(rb"SimpleX Chat Relay"),
    re.compile(rb"Ask SimpleX Team"),
    re.compile(rb"SimpleX Status"),
]


def validate_replacement_lengths() -> None:
    for old, new in REPLACEMENTS.items():
        if len(old) != len(new):
            raise RuntimeError(f"Replacement length mismatch: {old!r} -> {new!r}")


def patch_file(path: Path) -> tuple[bool, str, str, dict[str, int]]:
    original = path.read_bytes()
    before = hashlib.sha256(original).hexdigest()
    patched = original
    counts: dict[str, int] = {}
    for old, new in REPLACEMENTS.items():
        count = patched.count(old)
        if count:
            patched = patched.replace(old, new)
            counts[old.decode("utf-8", "replace")] = count
    after = hashlib.sha256(patched).hexdigest()
    if patched != original:
        path.write_bytes(patched)
    return patched != original, before, after, counts


def scan_forbidden(path: Path) -> list[str]:
    data = path.read_bytes()
    hits: list[str] = []
    for pattern in FORBIDDEN:
        if pattern.search(data):
            hits.append(pattern.pattern.decode("ascii"))
    return hits


def main() -> int:
    validate_replacement_lengths()
    libs = sorted(LIB_ROOT.glob("*/libsimplex.so"))
    if not libs:
        print(f"FAIL: no Android libsimplex.so files under {LIB_ROOT}", file=sys.stderr)
        return 2

    failed = False
    for lib in libs:
        changed, before, after, counts = patch_file(lib)
        rel = lib.relative_to(ROOT)
        if changed:
            print(f"PATCHED {rel}: {before[:16]} -> {after[:16]} replacements={counts}")
        else:
            print(f"OK unchanged {rel}: sha256={after[:16]}")
        hits = scan_forbidden(lib)
        if hits:
            print(f"FAIL {rel}: forbidden upstream native strings remain: {hits}", file=sys.stderr)
            failed = True
    if failed:
        return 3
    print("PASS: Whisper native Android libs contain no checked upstream relay/support strings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
