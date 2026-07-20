# SCA Practice Timer — share with friends + phone apps

Single-station MRCGP SCA timer (3 min reading + 12 min consultation) as:

1. **Shareable web / PWA** — friends open a link (or install to home screen)
2. **iPhone app** — Capacitor → Xcode
3. **Android app** — Capacitor → Android Studio

## Quick start (you)

```bash
cd sca-timer
npm install
npm start
```

Open **http://localhost:4173** on your phone (same Wi‑Fi) or laptop.

## Live link (share this)

**https://sca-practice-timer.vercel.app**

Friends open that URL on any phone. On iPhone: Safari → Share → Add to Home Screen.

## iPhone install (no Xcode, no App Store)

**https://sca-practice-timer.vercel.app/ios-install.html**

Or open `SCA_Timer_iOS.mobileconfig` (also in `output/`). Safari → install profile → Home Screen app icon.

Cloud IPA/simulator build (GitHub Actions, no local Xcode): repo `saaalahy93-a11y/sca-practice-timer` → Actions → **iOS Cloud Build**.

## Share with friends (easiest)

### Option A — Send the folder / zip
1. Zip the `sca-timer/www` folder
2. AirDrop / WhatsApp / Drive the zip
3. Friend opens `index.html` in Safari/Chrome  
   (best: host it — Option B)

### Option B — Host a link (recommended)
Upload the contents of `www/` to any static host, then share the URL:

- [Netlify Drop](https://app.netlify.com/drop) — drag the `www` folder
- GitHub Pages / Cloudflare Pages / Vercel

Friends then:
- **iPhone:** Safari → Share → **Add to Home Screen**
- **Android:** Chrome → menu → **Install app** / **Add to Home screen**

Works offline after first open (PWA service worker).

## Build iPhone app (Xcode)

Needs full **Xcode** from the App Store (not only Command Line Tools) and **CocoaPods** (`brew install cocoapods`).

The `ios/` project is already created. After installing Xcode:

```bash
sudo xcode-select -s /Applications/Xcode.app/Contents/Developer
cd sca-timer
npx cap sync ios
npx cap open ios
```

In Xcode: select your team → run on a simulator or your iPhone.

To share a TestFlight build: Archive → Distribute → TestFlight (Apple Developer account required).

## Share zip (no hosting)

Ready zip: `output/SCA_Timer_Share.zip` — send that to friends. They unzip and open `index.html`, or better upload `www/` to Netlify Drop for a real link.

## Build Android app (Android Studio)

Needs **Android Studio**.

```bash
cd sca-timer
npm install
npx cap add android  # first time only
npx cap sync android
npx cap open android
```

In Android Studio: Run on emulator or device.  
Build → Generate Signed Bundle / APK to share an `.apk` / Play upload.

## App ID

- Bundle / application id: `uk.sca.practicetimer`
- Display name: **SCA Timer**

## After editing the timer UI

Edit files in `www/`, then:

```bash
npx cap sync
```

so iOS/Android pick up changes.


## Android APK (ready to install)

Prebuilt debug APK:

- `output/SCA_Timer_Android.apk`
- `sca-timer/SCA_Timer_Android.apk`

Install: send to your phone → open the file → allow install from that source.

Rebuild:

```bash
export JAVA_HOME="/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home"
export ANDROID_HOME="/opt/homebrew/share/android-commandlinetools"
cd sca-timer
npx cap sync android
cd android && ./gradlew assembleDebug
```
