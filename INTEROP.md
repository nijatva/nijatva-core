# Interop: how the apps work together without depending on each other

The rule in one line: **apps talk over intents, never over artifacts.**

No app may add another app as a dependency. Nijatva Camera must not link Nijatva
Gallery; it must not import its classes, its resources or its AAR. What they share
is a *contract* — action strings, extras, MIME types and result codes — and that
contract lives in `nijatva-core`, which every app already depends on.

Two things follow, and both are the point:

- Every app installs alone and works alone. Uninstalling one never breaks another.
- When a sibling *is* installed, the two apps feel like one product.

## 1. Standard intents first

Before inventing anything, use what Android already defines. A standard intent
means **any** app can serve the request — the user's own gallery, their own
viewer — not only ours. That is better for the user and less code for us.

| Job | Use |
|---|---|
| Open a photo or video | `ACTION_VIEW`, `image/*` or `video/*` |
| Pick a photo | `ACTION_PICK` / `ACTION_GET_CONTENT` / Photo Picker |
| Share anything | `ACTION_SEND` with the right MIME type |
| Open a document | `ACTION_VIEW`, `application/pdf` |
| Dial a number | `ACTION_DIAL` (never `ACTION_CALL` without a tap) |
| Send a message | `ACTION_SENDTO`, `smsto:` |
| Add a contact | `ACTION_INSERT`, `ContactsContract.Contacts.CONTENT_TYPE` |
| Add a calendar event | `ACTION_INSERT`, `CalendarContract.Events.CONTENT_TYPE` |
| Open a link | `ACTION_VIEW`, `https` |
| Install an app | `ACTION_VIEW` on the APK, or the Appstore |

If a Nijatva app is installed and declares the same intent, it appears in the
chooser next to the others. Nothing extra to build.

## 2. Custom actions, only where Android has none

These exist because the platform does not define them. All live in the
`in.nijatva.action` namespace and are declared as constants in `nijatva-core`.

| Action | Served by | Extras |
|---|---|---|
| `in.nijatva.action.VIEW_MEDIA` | Gallery | `data: Uri` of the folder or item |
| `in.nijatva.action.PICK_MEDIA` | Gallery | `EXTRA_MIME_TYPES`, returns `data: Uri` |
| `in.nijatva.action.EDIT_PHOTO` | Photo Editor | `data: Uri`, returns `data: Uri` |
| `in.nijatva.action.SCAN_CODE` | QR Scanner | returns `EXTRA_TEXT` |
| `in.nijatva.action.RECORD_AUDIO` | Recorder | returns `data: Uri` |
| `in.nijatva.action.BROWSE` | Browser | `data: Uri`, plus `EXTRA_CONTAINER` |

Every one of them is `CATEGORY_DEFAULT` and carries a version:

```kotlin
// nijatva-core
object Interop {
    const val EXTRA_CONTRACT_VERSION = "in.nijatva.extra.CONTRACT_VERSION"
    const val EXTRA_SOURCE_PACKAGE  = "in.nijatva.extra.SOURCE_PACKAGE"
    const val CONTRACT_VERSION = 1

    const val ACTION_PICK_MEDIA = "in.nijatva.action.PICK_MEDIA"
    // ...
}
```

The receiver ignores a version it does not know and answers `RESULT_CANCELED`.
That is how an old app and a new app can be installed side by side without a
crash: the contract degrades, it does not explode.

## 3. Declaring what you can see

Android 11 and later hide other packages unless you ask. Every app that wants to
*offer* a handoff declares the intent, not the package:

```xml
<queries>
  <intent><action android:name="in.nijatva.action.VIEW_MEDIA" /></intent>
  <intent><action android:name="in.nijatva.action.PICK_MEDIA" /></intent>
</queries>
```

Intent-based queries are better than `<package>` entries: they keep working when
a new app starts serving the same action, and they do not hardcode a sibling.

## 4. The fallback is not optional

Every handoff has a local answer. If the sibling is missing, the app does the job
itself or shows the system chooser. It never shows a dead button and it never
crashes.

| Handoff | If the sibling is missing |
|---|---|
| Camera → Gallery | `ACTION_VIEW` on the system chooser |
| Files → PDF Viewer | `ACTION_VIEW` with `application/pdf` |
| Dialer → Contacts | the dialer's own T9 search |
| Messages → Contacts | type the number |
| Anything → Appstore | the release page on GitHub |
| QR → Browser | copy the link to the clipboard |

`ActivityNotFoundException` is caught at the call site, always. A missing sibling
is an expected state, not an error.

## 5. Showing each other, without nagging

The "support dikhana" part: one shared composable in `nijatva-core`, used on each
app's settings screen.

- A short list of the siblings that are **installed**, each a one-tap handoff.
- Siblings that are not installed are shown as a single line, not a wall of
  install prompts: "4 more Nijatva apps" → opens the Appstore or the site.
- No badge counting, no notifications, no "rate us", no popup on launch. The
  apps are not allowed to advertise at each other's users.

The list is a constant in `nijatva-core`; the installed/not-installed state comes
from `PackageManager` at render time, cached for the session.

## 6. Security

All Nijatva apps are signed with the same key, so a signature permission is the
cheap, correct boundary:

```xml
<permission android:name="in.nijatva.permission.INTEROP"
            android:protectionLevel="signature" />
```

Content providers and any activity that returns data use it. An app that is not
signed with the suite key cannot read another app's data by pretending to be a
sibling. Anything that crosses the boundary also stamps
`EXTRA_SOURCE_PACKAGE`, which the receiver verifies against the calling UID.

## 7. What is forbidden

- `implementation(project(":nijatva-gallery"))` in another app. Never.
- Copying a sibling's classes or resources into your app.
- Starting a sibling's activity by explicit `ComponentName` without a try/catch.
- Making a core feature depend on a sibling being installed.
- A silent network call between apps. There is no server to call.

## 8. The check

`no-gms-check` can grow a second rule for this: fail the build if an app module
declares a dependency on another `nijatva-*` app module. The rule is easy to
enforce mechanically, so it should be enforced mechanically rather than by
memory.
