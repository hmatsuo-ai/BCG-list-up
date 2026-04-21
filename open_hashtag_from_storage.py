"""
保存済み storage_state からブラウザを起動し、ハッシュタグ探索ページを開く。

既定の auth パス（--auth 省略時）:
  環境変数 BCG_LIST_UP_SECRETS_DIR があれば <そのディレクトリ>/auth.json
  なければ ユーザーホーム/.bcg-list-up-secrets/auth.json
  （いずれも Git 管理外を推奨。プロジェクト直下の .env で BCG_LIST_UP_SECRETS_DIR を指定可）

使い方:
  python open_hashtag_from_storage.py --tag photography
  python open_hashtag_from_storage.py --auth D:\\secrets\\auth.json --tag test
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

from secrets_paths import default_auth_json_path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="storage_state から復元してハッシュタグページを開く")
    p.add_argument(
        "--auth",
        type=Path,
        default=None,
        help="Playwright storage_state JSON（未指定時は secrets_paths の既定パス）",
    )
    p.add_argument(
        "--tag",
        required=True,
        help="ハッシュタグ（# は付けない。例: photography）",
    )
    p.add_argument(
        "--headless",
        action="store_true",
        help="ヘッドレスで実行（省略時はウィンドウ表示）",
    )
    p.add_argument(
        "--timeout-ms",
        type=int,
        default=60_000,
        help="ナビゲーション・操作の既定タイムアウト（ミリ秒）",
    )
    return p.parse_args()


def instagram_hashtag_url(tag: str) -> str:
    t = tag.strip().lstrip("#")
    return f"https://www.instagram.com/explore/tags/{t}/"


def main() -> int:
    args = parse_args()
    auth_path = (args.auth if args.auth is not None else default_auth_json_path()).resolve()

    if not auth_path.is_file():
        print(f"エラー: storage_state が見つかりません: {auth_path}", file=sys.stderr)
        print("先に save_auth_state.py で保存するか、--auth でパスを指定してください。", file=sys.stderr)
        print(f"既定ディレクトリ: {auth_path.parent}", file=sys.stderr)
        return 1

    tag = args.tag
    url = instagram_hashtag_url(tag)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless)
        context = browser.new_context(storage_state=str(auth_path))
        context.set_default_timeout(args.timeout_ms)
        page = context.new_page()

        page.goto(url, wait_until="domcontentloaded")

        if not args.headless:
            input("ブラウザを確認したら Enter で終了... ")

        context.close()
        browser.close()

    print(f"開いた URL: {url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
