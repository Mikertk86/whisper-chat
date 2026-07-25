# Whisper Android v6.5.6 official-6

Status: current private-relay hotfix. Use official-6 instead of official-4/official-5.

## APKs

- ARM64: `dist/whisper-v6.5.6-official-6/whisper-android-v6.5.6+361.6-arm64-v8a-release.apk`
- ARMv7: `dist/whisper-v6.5.6-official-6/whisper-android-v6.5.6+361.6-armeabi-v7a-release.apk`

## Private relay

- SMP: `smp://0zCvaMgX0nL95J68oW7dyWrIVpMGyhbqyqbC2ekemHA=@homebudget360.tailb34dd3.ts.net:5223`
- XFTP: `xftp://O5SdqMMNz6c5ceFrpY5mh4kyYYuD9vUze3-uMeJ9c6o=@homebudget360.tailb34dd3.ts.net:5443`

## Fix vs official-5

- App startup rewrites the active user server groups to exactly one operator: `Whisper Private`.
- Settings > Network and servers also runs the private relay enforcement before rendering.
- The UI model conditions are overridden to one accepted private operator, not SimpleX/Flux.

## SHA256

```text
7c9984a2ae44f62f34f93091bb5ac508fc7fd5122ea5c21270bd852cfd661a50  whisper-android-v6.5.6+361.6-arm64-v8a-release.apk
2e00d370c843743c56a2806ee2bcfb4aa1d334c3b9e50a0de8491adc07d7e570  whisper-android-v6.5.6+361.6-armeabi-v7a-release.apk
```

## Verification

- Gradle: `:android:assembleRelease` BUILD SUCCESSFUL.
- APK package: `chat.whisper.app`.
- APK label: `Whisper`.
- versionCode: `361`.
- Signed with Whisper release certificate SHA-256 digest `0f933d0f0e828bc011fc468c4b9b728ec74c30be09f6bd898b619c8c10cf6ab4`.
- APK dex contains `Whisper Private`, `enforceWhisperPrivateServers`, and `homebudget360.tailb34dd3.ts.net`.
- No ADB device was attached for live UI verification.
