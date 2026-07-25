# Whisper Android release

Whisper is a private messenger build based on the SimpleX Chat source code, prepared for public Android distribution by Michal/Mikertk86.

## Official download

- Repo: https://github.com/Mikertk86/whisper-chat
- Releases: https://github.com/Mikertk86/whisper-chat/releases
- Latest: https://github.com/Mikertk86/whisper-chat/releases/latest
- Current release: https://github.com/Mikertk86/whisper-chat/releases/tag/whisper-v6.5.6-official-2

## Android package

- Application ID: `chat.whisper.app`
- App name: `Whisper`
- Version: `6.5.6`, versionCode `358`
- Release tag: `whisper-v6.5.6-official-2`
- Release artifacts:
  - `whisper-android-v6.5.6+358.2-arm64-v8a-release.apk`
  - `whisper-android-v6.5.6+358.2-armeabi-v7a-release.apk`
- Checksum file: `SHA256SUMS.txt`
- Checksum signature: `SHA256SUMS.txt.asc`
- GPG public key: `WHISPER_RELEASE_SIGNING_PUBLIC_KEY.asc`

## Verification

Official release APKs must be release-signed and must not contain `debug` in the filename.

Release APK signing certificate SHA-256:

`0f933d0f0e828bc011fc468c4b9b728ec74c30be09f6bd898b619c8c10cf6ab4`

GPG release signing key fingerprint:

`5AED9611D6C1BDB95DFA58349BC153BAD5F1FD0E`

SHA-256 for current APKs:

```text
87696dae75650388804bfe02cdf1607c65adcd4cf5408ab0c98d1ffb2eebbe09  whisper-android-v6.5.6+358.2-arm64-v8a-release.apk
7500fe17c8cfac069e2e25f2afb2273e33bd48371868531d393bb837be8a6901  whisper-android-v6.5.6+358.2-armeabi-v7a-release.apk
```

Acceptance gate for the current APKs:

- `./gradlew :android:assembleRelease` → `BUILD SUCCESSFUL`
- Gradle task `:android:patchWhisperNativeLibs` runs before Android CMake/native packaging.
- `aapt dump badging`:
  - `package: name='chat.whisper.app'`
  - `application-label:'Whisper'`
  - native-code: `arm64-v8a` / `armeabi-v7a`
- `apksigner verify --verbose --print-certs`:
  - APK Signature Scheme v2: `true`
  - signer DN: `CN=Whisper, OU=Hermes, O=Whisper, L=Rzeszow, ST=Podkarpackie, C=PL`
- Whole-APK binary scan: no checked upstream default relay hosts or support labels:
  - no `smp*.simplex.im`
  - no `xftp*.simplex.im`
  - no `simplexonflux.com`
  - no `SimpleX Chat Relay`, `Ask SimpleX Team`, `SimpleX Status`
- `sha256sum -c SHA256SUMS.txt` → OK for APKs, notes and public key.
- `gpg --verify SHA256SUMS.txt.asc SHA256SUMS.txt` → valid signature.

## Protocol vs infrastructure

Whisper is not a new wire protocol. The protocol/client core remains a fork of the SimpleX protocol/client codebase, with AGPL source and protocol compatibility preserved.

The product and infrastructure layer is Whisper:

- Android package and launcher label: Whisper / `chat.whisper.app`
- Default operator branding in the fork: Whisper
- Support/bot profile: Asystent
- Default relay infrastructure: private Whisper SMP/XFTP relay on `100.84.65.50:5223` and `100.84.65.50:5443`
- Public upstream relay presets are removed from the checked Android runtime/native package surface.

Android native note:

- The Android project consumes prebuilt `libsimplex.so` artifacts.
- Canonical Haskell source defaults live in `src/Simplex/Chat/Operators/Presets.hs`.
- `scripts/whisper_patch_native_libs.py` is wired into Gradle to reproducibly apply equal-length byte replacements to prebuilt native artifacts before packaging. This avoids shipping upstream default relay presets while preserving ELF layout.
- A full from-source Android native rebuild via upstream Nix/Hydra is a separate heavy build path.

## Source and license

This project is based on SimpleX Chat and is distributed under AGPL-3.0. Publish corresponding source code for every APK release.

Corresponding source for the current APK release:

https://github.com/Mikertk86/whisper-chat/tree/whisper-v6.5.6-official-2

## Asystent contact

Current private Whisper/Asystent contact link uses the private Tailscale relay host `100.84.65.50` and is recorded in the local Ghost runbook. The old public `smp12.simplex.im` support link is obsolete.

## Notice

Whisper Android is an independent build based on SimpleX Chat source code. It is not an official SimpleX Chat Ltd release.
