#!/usr/bin/env python3
"""Guard rails for the Whisper Android fork.

This script intentionally checks only runtime/user-facing Android/KMP surfaces.
It does not require renaming internal Kotlin packages or upstream module names.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_APP_LINK_PATTERNS = [
    r'android:scheme="simplex"',
    r'android:host="simplex\.chat"',
    r'android:host="smp\d+\.simplex\.im"',
    r'android:host="smp\d+\.simplexonflux\.com"',
]

FORBIDDEN_RUNTIME_PATTERNS = [
    r'https://smp\d+\.simplex\.im/a#',
    r'https://simplex\.chat(?!/blog/202|/docs/|/downloads)',
    r'github\.com/simplex-chat/simplex-chat',
    r'SimpleX Chat call service',
    r'SIMPLEX_SERVICE',
    r'"Simplex service',
    r'"SimplexService',
    r'simplex-chat\.\$ts\.zip',
]

STRING_VALUE_FORBIDDEN = re.compile(r">[^<]*(SimpleX|Simplex|simplex\.chat|simplex\.im|simplexonflux)[^<]*<")
ALLOW_STRING_LINES = (
    'core_simplexmq_version',  # protocol library name, not product/log-in surface
)

CHECK_FILES = [
    'apps/multiplatform/android/src/main/AndroidManifest.xml',
    'apps/multiplatform/android/src/main/java/chat/simplex/app/SimplexApp.kt',
    'apps/multiplatform/android/src/main/java/chat/simplex/app/SimplexService.kt',
    'apps/multiplatform/android/src/main/java/chat/simplex/app/CallService.kt',
    'apps/multiplatform/common/src/androidMain/kotlin/chat/simplex/common/platform/SimplexService.android.kt',
    'apps/multiplatform/common/src/commonMain/kotlin/chat/simplex/common/platform/Log.kt',
    'apps/multiplatform/common/src/commonMain/kotlin/chat/simplex/common/views/usersettings/SettingsView.kt',
    'apps/multiplatform/common/src/commonMain/kotlin/chat/simplex/common/views/helpers/Utils.kt',
    'apps/multiplatform/common/src/commonMain/kotlin/chat/simplex/common/views/chat/ComposeView.kt',
    'apps/multiplatform/common/src/commonMain/kotlin/chat/simplex/common/views/database/DatabaseView.kt',
    'apps/multiplatform/common/src/commonMain/kotlin/chat/simplex/common/views/migration/MigrateToDevice.kt',
]

STRING_FILES = [
    'apps/multiplatform/common/src/commonMain/resources/MR/base/strings.xml',
    'apps/multiplatform/common/src/commonMain/resources/MR/pl/strings.xml',
]


def fail(path: str, line_no: int, reason: str, line: str, failures: list[str]) -> None:
    failures.append(f'{path}:{line_no}: {reason}: {line.strip()}')


def main() -> int:
    failures: list[str] = []

    manifest = (ROOT / 'apps/multiplatform/android/src/main/AndroidManifest.xml').read_text(encoding='utf-8')
    for pattern in FORBIDDEN_APP_LINK_PATTERNS:
        for match in re.finditer(pattern, manifest):
            line_no = manifest.count('\n', 0, match.start()) + 1
            line = manifest.splitlines()[line_no - 1]
            fail('apps/multiplatform/android/src/main/AndroidManifest.xml', line_no, f'forbidden app-link pattern {pattern}', line, failures)
    if 'android:scheme="whisper"' not in manifest:
        failures.append('apps/multiplatform/android/src/main/AndroidManifest.xml: missing whisper: URI scheme')

    for rel in CHECK_FILES:
        text = (ROOT / rel).read_text(encoding='utf-8')
        for pattern in FORBIDDEN_RUNTIME_PATTERNS:
            for line_no, line in enumerate(text.splitlines(), 1):
                if re.search(pattern, line):
                    fail(rel, line_no, f'forbidden runtime pattern {pattern}', line, failures)

    for rel in STRING_FILES:
        for line_no, line in enumerate((ROOT / rel).read_text(encoding='utf-8').splitlines(), 1):
            if any(allowed in line for allowed in ALLOW_STRING_LINES):
                continue
            if STRING_VALUE_FORBIDDEN.search(line):
                fail(rel, line_no, 'user-visible string still mentions upstream SimpleX surface', line, failures)

    if failures:
        print('FAIL: Whisper rebrand guard found public SimpleX leakage:')
        print('\n'.join(failures[:200]))
        if len(failures) > 200:
            print(f'... {len(failures) - 200} more')
        return 1
    print('PASS: Whisper Android public surface has no checked SimpleX leakage.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
