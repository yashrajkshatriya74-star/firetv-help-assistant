# Android / Fire OS shell

A very small Kotlin app. It opens the hosted web app in a full-screen `WebView` and forwards the
remote's **Back** and **Menu** buttons to the page (`window.tvBack()` and `window.tvMenu()`).

Tested on the Android Studio **Television (1080p), API 30 (Android 11)** emulator, which matches Fire OS 8.

## Build and run

1. Android Studio > New Project > **Empty Views Activity**, name `FireTVHelper`, package
   `com.example.firetvhelper`, Kotlin, minimum SDK 30 or lower.
2. Replace `MainActivity.kt` and `AndroidManifest.xml` with the files in this folder
   (or open this `android` folder after adding the standard Gradle files that the wizard generates).
3. In `MainActivity.kt`, set `startUrl` to your own hosted copy of `../web`.
4. Pick the TV emulator (or a Fire OS device) and press Run. The app also appears as
   "Help Assistant" in the TV home Apps row.

The manifest declares `LEANBACK_LAUNCHER` and marks touchscreen and leanback as not required, so the app
shows up on Android TV and Fire OS launchers.
