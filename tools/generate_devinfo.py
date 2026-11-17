#!/usr/bin/env python3
"""Regenerate SignatureDevInfo.java - the figures on the Developer card.

Every Nijatva app shows the same Developer card, so the figures on it cannot be
typed in by hand in six places. This script reads them from two places that are
already true, and writes one small generated file:

  * repositories  - the public repository count on GitHub for the owner below
  * apps planned  - the length of tools/apps.json
  * with code     - apps in apps.json whose "repo" exists on GitHub

Run it before a release, or from a Gradle task:

    python3 tools/generate_devinfo.py
    python3 tools/generate_devinfo.py --out ../app/src/main/java/com/nijatva/signature/SignatureDevInfo.java

Uses GITHUB_TOKEN when it is set (avoids the 60-requests-an-hour anonymous limit);
falls back to anonymous requests otherwise. --offline writes the file using the
manifest alone and leaves the repository count at its last known value.
"""

import argparse
import datetime
import json
import os
import sys
import urllib.error
import urllib.request

API = "https://api.github.com"
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUT = os.path.join(HERE, "..", "SignatureDevInfo.java")

TEMPLATE = """package com.nijatva.signature;

/**
 * GENERATED FILE - do not edit by hand.
 *
 * Rewritten by {{@code tools/generate_devinfo.py}}, which reads the figures from
 * GitHub and from {{@code tools/apps.json}}. Edit those, then run the script.
 *
 * Repositories:  {repositories}
 * Apps planned:  {planned}
 * With code:     {with_code}
 * Figures read:  {date}
 */
public final class SignatureDevInfo {{

    /** Public repositories on github.com/{owner}. */
    public static final int REPOSITORIES = {repositories};

    /** Apps in the Nijatva suite, from tools/apps.json. */
    public static final int APPS_PLANNED = {planned};

    /** Apps that already have a repository. */
    public static final int WITH_CODE = {with_code};

    /** The day the figures above were read, as it appears on the card. */
    public static final String FIGURES_DATE = "{date}";

    /** Short codes of the apps with a repository, in manifest order. */
    public static final String[] APP_CODES = {{{codes}}};

    /**
     * The whole suite, in manifest order:
     * {{code, name, site slug, repository, Android package}}.
     *
     * <p>Blank where a value is not known yet. The Developer card lists these, so a
     * planned app and a shipped one are described by the same generated row.
     */
    public static final String[][] APPS = {{
{rows}
    }};

    private SignatureDevInfo() {{
    }}
}}
"""


def request(url, token):
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "nijatva-signature-devinfo")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def public_repos(owner, token):
    """Every public repository name for the owner, following pagination."""
    names = []
    page = 1
    while True:
        url = "{}/users/{}/repos?per_page=100&page={}".format(API, owner, page)
        try:
            batch = request(url, token)
        except urllib.error.HTTPError as error:
            raise SystemExit("GitHub said {} for {}. Set GITHUB_TOKEN and retry."
                             .format(error.code, url))
        if not batch:
            return names
        names.extend(repo["name"] for repo in batch)
        if len(batch) < 100:
            return names
        page += 1


def format_date(day):
    return "{} {}".format(day.day, day.strftime("%B %Y"))


def main():
    parser = argparse.ArgumentParser(description="Regenerate SignatureDevInfo.java")
    parser.add_argument("--out", default=DEFAULT_OUT, help="file to write")
    parser.add_argument("--manifest", default=os.path.join(HERE, "apps.json"),
                        help="the suite's app list")
    parser.add_argument("--date", default=None,
                        help="figures date as YYYY-MM-DD (default: today)")
    parser.add_argument("--offline", action="store_true",
                        help="skip GitHub; keep the repository count from the old file")
    args = parser.parse_args()

    with open(args.manifest, encoding="utf-8") as handle:
        manifest = json.load(handle)

    owner = manifest.get("owner", "vasudev-work")
    apps = manifest["apps"]

    repositories = 0
    if args.offline:
        repositories = previous_repositories(args.out)
        print("offline: keeping {} repositories from {}".format(repositories, args.out))
    else:
        repositories = len(public_repos(owner, os.environ.get("GITHUB_TOKEN")))
        print("github: {} public repositories".format(repositories))

    with_repo = [app for app in apps if app.get("repo")]
    codes = [app["code"] for app in with_repo]
    quoted = ", ".join('"{}"'.format(code) for code in codes)
    rows = "\n".join(
        '        {{"{code}", "{name}", "{site}", "{repo}", "{pkg}"}},'.format(
            code=app.get("code", ""),
            name=app.get("name", ""),
            site=app.get("site", "") or "",
            repo=app.get("repo", "") or "",
            pkg=app.get("package", "") or "",
        )
        for app in apps
    )

    day = (datetime.date.fromisoformat(args.date) if args.date else datetime.date.today())
    body = TEMPLATE.format(
        owner=owner,
        repositories=repositories,
        planned=len(apps),
        with_code=len(with_repo),
        date=format_date(day),
        codes=quoted,
        rows=rows,
    )

    out = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as handle:
        handle.write(body)
    print("wrote {} ({} apps planned, {} with code)".format(out, len(apps), len(with_repo)))


def previous_repositories(path):
    """Reads REPOSITORIES out of an existing generated file."""
    try:
        with open(path, encoding="utf-8") as handle:
            for line in handle:
                if "int REPOSITORIES" in line:
                    return int(line.split("=")[1].strip().rstrip(";"))
    except OSError:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
