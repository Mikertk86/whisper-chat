# Whisper Android release

Whisper is a private messenger build based on the SimpleX Chat source code, prepared for public Android distribution by Michal/Mikertk86.

## Official download

- Repo: https://github.com/Mikertk86/whisper-chat
- Releases: https://github.com/Mikertk86/whisper-chat/releases
- Latest: https://github.com/Mikertk86/whisper-chat/releases/latest
- Current release: https://github.com/Mikertk86/whisper-chat/releases/tag/whisper-v6.5.6-official-3

## Android package

- Application ID: `chat.whisper.app`
- App name: `Whisper`
- Version: `6.5.6`, versionCode `358`
- Release tag: `whisper-v6.5.6-official-3`
- Release artifacts:
  - `whisper-android-v6.5.6+358.3-arm64-v8a-release.apk`
  - `whisper-android-v6.5.6+358.3-armeabi-v7a-release.apk`
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
b9c0a68d86a5c1d69e9e351fa964aff4785a092c1181ffae3fb7334c8489fc73  whisper-android-v6.5.6+358.3-arm64-v8a-release.apk
60ff16ecaf7c677505403909031d32afb3d3dd09900fb5a05942036d6fe031fd  whisper-android-v6.5.6+358.3-armeabi-v7a-release.apk
```

Acceptance gate for the current APKs:

- `./gradlew :android:assembleRelease --no-daemon` with signing env → `BUILD SUCCESSFUL`.
- Gradle release signing reads `WHISPER_*` env variables so signing passwords are not passed in process arguments.
- Gradle task `:android:patchWhisperNativeLibs` runs before Android CMake/native packaging.
- `aapt dump badging`:
  - `package: name='chat.whisper.app'`
  - `application-label:'Whisper'`
  - native-code: `arm64-v8a` / `armeabi-v7a`
- `apksigner verify --verbose --print-certs`:
  - APK Signature Scheme v2: `true`
  - signer DN: `CN=Whisper, OU=Hermes, O=Whisper, L=Rzeszow, ST=Podkarpackie, C=PL`
- Whole-APK binary scan: no checked upstream/private-default relay/support strings:
  - no `smp*.simplex.im`
  - no `xftp*.simplex.im`
  - no `simplexonflux.com`
  - no `100.84.65.50`
  - no `SimpleX Chat Relay`, `Ask SimpleX Team`, `SimpleX Status`
  - no `SimpleX Directory`, `SimpleX network mission`, `chat@simplex.chat`
- Whole-APK scan confirms `tailb34dd3.ts.net` / `*.tailb34dd3.ts.net` private relay domains are present in the packaged native runtime. The full public bridge/Funnel hostname is `homebudget360.tailb34dd3.ts.net`.
- `sha256sum -c SHA256SUMS.txt` → OK for APKs, notes and public key.
- `gpg --verify SHA256SUMS.txt.asc SHA256SUMS.txt` → valid signature.

## Protocol vs infrastructure

Whisper is not a new wire protocol. The protocol/client core remains a fork of the SimpleX protocol/client codebase, with AGPL source and protocol compatibility preserved.

The product and infrastructure layer is Whisper:

- Android package and launcher label: Whisper / `chat.whisper.app`
- Default operator branding in the fork: Whisper
- Support/bot profile: Asystent
- Default relay infrastructure: Whisper SMP/XFTP relay public bridge on `homebudget360.tailb34dd3.ts.net:5223` and `homebudget360.tailb34dd3.ts.net:5443`; packaged native runtime carries equal-length `*.tailb34dd3.ts.net` relay domains until a full native rebuild can encode the full hostname everywhere.
- Tailscale Funnel is enabled for public TCP access on `5223` and `5443`.
- Local hairpin for this host maps `homebudget360.tailb34dd3.ts.net` to `127.0.0.1` in `/etc/hosts`, so the local bridge can create queues through the same public hostname while external clients use Funnel.
- Public upstream relay presets are removed from the checked Android runtime/native package surface.

Android native note:

- The Android project consumes prebuilt `libsimplex.so` artifacts.
- Canonical Haskell source defaults live in `src/Simplex/Chat/Operators/Presets.hs`.
- `scripts/whisper_patch_native_libs.py` is wired into Gradle to reproducibly apply equal-length byte replacements to prebuilt native artifacts before packaging. This avoids shipping upstream default relay presets and visible upstream support strings while preserving ELF layout.
- A full from-source Android native rebuild via upstream Nix/Hydra is a separate heavy build path.

## Source and license

This project is based on SimpleX Chat and is distributed under AGPL-3.0. Publish corresponding source code for every APK release.

Corresponding source for the current APK release:

https://github.com/Mikertk86/whisper-chat/tree/whisper-v6.5.6-official-3

## Asystent contact

Current Whisper/Asystent contact link uses the public Tailscale Funnel relay host `homebudget360.tailb34dd3.ts.net` and is recorded in the local Ghost runbook. The old public `smp12.simplex.im` support link is obsolete.

## Notice

Whisper Android is an independent build based on SimpleX Chat source code. It is not an official SimpleX Chat Ltd release.
