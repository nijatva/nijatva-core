package com.nijatva.signature;

/**
 * GENERATED FILE - do not edit by hand.
 *
 * Rewritten by {@code tools/generate_devinfo.py}, which reads the figures from
 * GitHub and from {@code tools/apps.json}. Edit those, then run the script.
 *
 * Repositories:  22
 * Apps planned:  28
 * With code:     14
 * Figures read:  18 November 2026
 */
public final class SignatureDevInfo {

    /** Public repositories on github.com/nijatva. */
    public static final int REPOSITORIES = 22;

    /** Apps in the Nijatva suite, from tools/apps.json. */
    public static final int APPS_PLANNED = 28;

    /** Apps that already have a repository. */
    public static final int WITH_CODE = 14;

    /** The day the figures above were read, as it appears on the card. */
    public static final String FIGURES_DATE = "18 November 2026";

    /** Short codes of the apps with a repository, in manifest order. */
    public static final String[] APP_CODES = {"Br", "Cm", "Co", "Di", "Fi", "Ga", "Me", "Mx", "Mu", "No", "Pe", "Ph", "Va", "Vi"};

    /**
     * The whole suite, in manifest order:
     * {code, name, site slug, repository, Android package}.
     *
     * <p>Blank where a value is not known yet. The Developer card lists these, so a
     * planned app and a shipped one are described by the same generated row.
     */
    public static final String[][] APPS = {
        {"Ap", "App Manager", "appmanager", "", ""},
        {"Br", "Browser", "browser", "nijatva-browser", "in.nijatva.browser"},
        {"Ca", "Calculator", "calc", "", ""},
        {"Cl", "Calendar", "calendar", "", ""},
        {"Cm", "Camera", "camera", "nijatva-camera", "com.nijatva.camera"},
        {"Ck", "Clock", "clock", "", ""},
        {"Co", "Contacts", "contacts", "nijatva-contacts", "com.nijatva.contacts"},
        {"De", "Device Info", "deviceinfo", "", ""},
        {"Di", "Dialer", "dialer", "nijatva-dialer", "com.nijatva.dialer"},
        {"Ex", "Expenses", "expenses", "", ""},
        {"Fi", "Files", "files", "nijatva-file", "com.nijatva.file"},
        {"Ga", "Gallery", "gallery", "nijatva-gallery", "com.nijatva.gallery"},
        {"Kb", "Keyboard", "keyboard", "", ""},
        {"La", "Launcher", "launcher", "", ""},
        {"Me", "Messages", "sms", "nijatva-messages", "com.nijatva.messages"},
        {"Mx", "Mini X", "minix", "nijatva-browser-mini-x", "com.nijatva.mini.x"},
        {"Mu", "Music", "music", "nijatva-music-player", "com.nijatva.music.player"},
        {"No", "Notes", "notes", "nijatva-notes", "com.nijatva.notes"},
        {"Pd", "PDF", "pdf", "", ""},
        {"Pe", "Photo Editor", "editor", "nijatva-photo-editor", "com.nijatva.photo.editor"},
        {"Ph", "Photos", "photos", "nijatva-photos", "com.nijatva.photos"},
        {"Qr", "QR Code", "qr", "", ""},
        {"Re", "Recorder", "recorder", "", ""},
        {"Rs", "RSS", "rss", "", ""},
        {"Ta", "Tasks", "tasks", "", ""},
        {"Va", "Vault", "vault", "nijatva-drive", ""},
        {"Vi", "Video Player", "video", "nijatva-video-player", "com.nijatva.videoplayer"},
        {"We", "Weather", "weather", "", ""},
    };

    private SignatureDevInfo() {
    }
}
