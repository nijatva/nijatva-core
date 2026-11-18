package com.nijatva.signature;

/**
 * GENERATED FILE - do not edit by hand.
 *
 * Rewritten by {@code tools/generate_devinfo.py}, which reads the figures from
 * GitHub and from {@code tools/apps.json}. Edit those, then run the script.
 *
 * Repositories:  22
 * Apps planned:  25
 * With code:     11
 * Figures read:  18 November 2026
 */
public final class SignatureDevInfo {

    /** Public repositories on github.com/vasudev-work. */
    public static final int REPOSITORIES = 22;

    /** Apps in the Nijatva suite, from tools/apps.json. */
    public static final int APPS_PLANNED = 25;

    /** Apps that already have a repository. */
    public static final int WITH_CODE = 11;

    /** The day the figures above were read, as it appears on the card. */
    public static final String FIGURES_DATE = "18 November 2026";

    /** Short codes of the apps with a repository, in manifest order. */
    public static final String[] APP_CODES = {"Br", "Ca", "Cm", "Co", "Di", "Fi", "Ga", "Mu", "Me", "Tr", "Va"};

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
        {"Ca", "Calculator", "calc", "nijatva-calc", "com.nijatva.calc"},
        {"Cl", "Calendar", "calendar", "", ""},
        {"Cm", "Camera", "camera", "nijatva-camera", "com.nijatva.camera"},
        {"Ck", "Clock", "clock", "", ""},
        {"Co", "Contacts", "contacts", "nijatva-contacts", "com.nijatva.contacts"},
        {"Di", "Dialer", "dialer", "nijatva-dialer", "com.nijatva.dialer"},
        {"De", "Device Info", "deviceinfo", "", ""},
        {"Ex", "Expenses", "expenses", "", ""},
        {"Fi", "Files", "files", "nijatva-file", "com.nijatva.file"},
        {"Ga", "Gallery", "gallery", "nijatva-gallery", "com.nijatva.gallery"},
        {"Kb", "Keyboard", "keyboard", "", ""},
        {"La", "Launcher", "launcher", "", ""},
        {"Mu", "Music", "music", "nijatva-music-player", "com.nijatva.music.player"},
        {"No", "Notes", "notes", "", ""},
        {"Pd", "PDF", "pdf", "", ""},
        {"Qr", "QR Code", "qr", "", ""},
        {"Re", "Recorder", "recorder", "", ""},
        {"Rs", "RSS", "rss", "", ""},
        {"Me", "Messages", "sms", "nijatva-messages", "com.nijatva.messages"},
        {"Ta", "Tasks", "tasks", "", ""},
        {"Tr", "Translate", "translate", "nijatva-translate", "com.nijatva.translate"},
        {"Va", "Vault", "vault", "nijatva-drive", ""},
        {"We", "Weather", "weather", "", ""},
    };

    private SignatureDevInfo() {
    }
}
