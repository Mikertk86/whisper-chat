# Whisper Android release

Current status: `whisper-v6.5.6-official-5` is the valid public Android hotfix release. Use official-5 instead of official-4.

## Current release

- Release tag: `whisper-v6.5.6-official-5`
- GitHub: https://github.com/Mikertk86/whisper-chat/releases/tag/whisper-v6.5.6-official-5
- ARM64 APK: https://github.com/Mikertk86/whisper-chat/releases/download/whisper-v6.5.6-official-5/whisper-android-v6.5.6%2B360.5-arm64-v8a-release.apk
- ARMv7 APK: https://github.com/Mikertk86/whisper-chat/releases/download/whisper-v6.5.6-official-5/whisper-android-v6.5.6%2B360.5-armeabi-v7a-release.apk

## official-5 hotfix

Problem in official-4: creating/copying an invitation address could still try native-core defaults such as `smp18.whisper.li`, `smp10.whisper.li`, `smp15.whisper.li`, `smp8.whisper.li`. These hosts are not served, so Android showed a network error.

Fix in official-5:

- `Core.kt` now enforces private Whisper user servers for existing profiles at app startup.
- `ChooseServerOperators.kt` now enforces the same servers when onboarding completes for new profiles.
- The enforced custom servers are:
  - SMP: `smp://0zCvaMgX0nL95J68oW7dyWrIVpMGyhbqyqbC2ekemHA=@homebudget360.tailb34dd3.ts.net:5223`
  - XFTP: `xftp://O5SdqMMNz6c5ceFrpY5mh4kyYYuD9vUze3-uMeJ9c6o=@homebudget360.tailb34dd3.ts.net:5443`

## Verification official-5

- Gradle task: `:android:assembleRelease` → `BUILD SUCCESSFUL`.
- Package: `chat.whisper.app`.
- Label: `Whisper`.
- versionCode: `360`.
- Release signing certificate SHA-256: `0f933d0f0e828bc011fc468c4b9b728ec74c30be09f6bd898b619c8c10cf6ab4`.
- Hotfix strings verified inside APK `classes4.dex`: `enforceWhisperPrivateServers`, `homebudget360.tailb34dd3.ts.net`.
- No `smp*.whisper.li`, `smp*.simplex.im`, `xftp*.whisper.li`, or `xftp*.simplex.im` strings in APK dex/resources.
- Public DNS for `homebudget360.tailb34dd3.ts.net` resolves from 1.1.1.1, 8.8.8.8, 9.9.9.9.
- Tailscale Funnel reports TCP 5223 and 5443 enabled.

## SHA256 official-5

```text
dd5f52d21d28c91f0c39368dbb814821c546bc85eb4e1fc4481cf2b9fce6bcc7  whisper-android-v6.5.6+360.5-arm64-v8a-release.apk
8e7034e271cc280d910a3a55a8b2191f54a6ed3e23d56bfafe2fefeae1a0143c  whisper-android-v6.5.6+360.5-armeabi-v7a-release.apk
```

## Local artifacts

`/home/mike/Dokumenty/Projects/simplex-chat/dist/whisper-v6.5.6-official-5/`

## Signing

APK release keystore: `/home/mike/.config/whisper/release-signing.env` references local private keystore outside repo.
GPG signing key: `/home/mike/.config/whisper/gnupg`, fingerprint `5AED9611D6C1BDB95DFA58349BC153BAD5F1FD0E`.
Do not commit private signing material.
