# Using the signature in every Nijatva app

Two routes. Pick per app.

- **Module route (recommended)** — one dependency line, no copied code, no manifest edits.
- **Patch route** — for the seven apps that already have a patch, when you would rather not
  add a Gradle dependency.

---

## A. Module route — 4 steps

**1. Let the app resolve the module** — `settings.gradle.kts`. CI and every app on
another machine use GitHub Packages; `mavenLocal()` stays for a quick local loop.

```kotlin
dependencyResolutionManagement {
    repositories {
        google(); mavenCentral()
        maven {
            name = "NijatvaGitHubPackages"
            url = uri("https://maven.pkg.github.com/nijatva/nijatva-core")
            credentials {
                username = System.getenv("GITHUB_ACTOR")
                password = System.getenv("GITHUB_TOKEN")
            }
        }
        mavenLocal()   // local iteration only; never the CI path
    }
}
```

`publish.yml` in `nijatva-core` publishes `:signature` on a release, using the tag
as the version. To publish by hand: `./gradlew :signature:publish
-PreleaseVersion=1.0.1` with `GITHUB_ACTOR` and `GITHUB_TOKEN` exported.

**2. Add the dependency** — `app/build.gradle.kts`:

```kotlin
dependencies { implementation("com.nijatva:signature:1.0.0") }
```

**3. Open the screens** from wherever the app keeps its settings:

```java
startActivity(Signature.appearance(this));   // Appearance: theme + accent + dynamic colour
startActivity(Signature.developer(this));    // Developer card
```

That is all. The two activities and the family `<queries>` are declared in the **library**
manifest, so the app's own `AndroidManifest.xml` is untouched — manifest merging adds them.

Optional, so the app's own chrome follows the accent the user picked:

```java
int accent = SignatureTheme.accent(this);
boolean dark  = SignatureTheme.isDark(this);
```

---

## B. Patch route — 7 apps

From a clean checkout of the app:

```bash
git checkout -b signature-screens
git am /path/to/patches/nijatva-<repo>.patch
```

`files/` in the same zip holds the same result as plain files, for editing by hand.

---

## Per app

| App | Stack | Route | What to do |
| --- | --- | --- | --- |
| **Photos** `com.nijatva.photos` | Kotlin · Compose | Module — Developer only | Add the dependency. Point the Settings → "About Nijatva Photos" row at `Signature.developer(this)`. **Keep its own Compose Appearance screen** — it re-themes live; the kit's Appearance would be a second, dumber copy. |
| **Gallery** `com.nijatva.gallery` | Kotlin · Compose | Patch **or** module | Patch does it all. By hand: add the dependency, Settings row → `Signature.developer(context)`, delete `ui/DeveloperPage.kt` and the `Route.Developer` / `Host.openDeveloper()` references. Its own Appearance sheet stays. |
| **Camera** `com.nijatva.camera` | Kotlin · Compose | Patch **or** module | Same as Gallery: menu → kit Developer, delete `ui/DeveloperPage.kt`. The camera's own Appearance sheet stays. |
| **Photo Editor** `com.nijatva.photo.editor` | Kotlin | Module | Add the dependency, add a Settings row that calls both intents. No patch exists. |
| **Video Player** `com.nijatva.videoplayer` | Kotlin | Module | Add the dependency, Settings row → both intents. No patch exists. |
| **Music Player** `com.nijatva.music.player` | Kotlin Multiplatform | Module — **androidMain only** | `composeApp/build.gradle.kts`: put the dependency in `androidMain.dependencies { … }`. The kit is Android-only, so desktop and any other target must not reference it. Open from Compose with `LocalContext.current.startActivity(Signature.developer(ctx))`. |
| **File Manager** `com.nijatva.file` | Java | Patch **or** module | Patch turns its `AppearanceActivity` / `DeveloperActivity` into thin subclasses. By hand: add the dependency and make those two classes extend the kit's screens, or replace the menu entries with the kit intents. |
| **Browser** `in.nijatva.browser` | Kotlin | Module | Add the dependency, Settings row → both intents. No patch exists. |
| **Browser Mini X** `com.nijatva.mini.x` | Kotlin | Module | Same as Browser. |
| **WTRLab** `com.nijatva.wtrlab` | Kotlin | Module | Same as Browser. |
| **Contacts** `com.nijatva.contacts` | Java | Patch | Patch adds the kit, both activities and a Nijatva section in Settings. |
| **Dialer** `com.nijatva.dialer` | Java | Patch | Patch makes its two activities thin subclasses and removes the old screens. |
| **Messages** `com.nijatva.messages` | Java | Patch | Patch adds the kit and a Settings sheet with Appearance / Developer / set-as-default SMS. |

---

## Things that bite

- **Same signing key everywhere.** The Developer card prints the APK certificate's SHA-256
  (first 16 hex). Two apps showing the same fingerprint is the proof they came from one hand —
  that only works if every app is signed with the same keystore. Debug builds will show the
  debug key's fingerprint.
- **Do not ship two Appearance screens.** In Gallery and Camera the app's own sheet stays and
  the kit's Appearance activity is still present. Either hide one entry, or drop the kit's
  Appearance from those two and keep the app's.
- **Figures are generated, not typed.** `tools/generate_devinfo.py` rewrites
  `SignatureDevInfo.java` from `tools/apps.json`. Re-run it when the suite's counts change, or
  the card keeps claiming old numbers.
- **No `INTERNET` permission is added.** The card reads the manifest and prints "No INTERNET
  permission" only when that is actually true.
- **Bump the version when the kit changes** (`version = "1.0.0"` in
  `signature/build.gradle.kts`), publish, and every app picks it up on its next build.
