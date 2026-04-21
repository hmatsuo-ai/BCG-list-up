"""
手動ログイン後に storage_state を保存する。

既定の保存先（--out 省略時）:
  BCG_LIST_UP_SECRETS_DIR/auth.json または ~/.bcg-list-up-secrets/auth.json
  親ディレクトリは存在しなければ作成する。

使い方:
  python save_auth_state.py
  python save_auth_state.py --out D:\\secrets\\auth.json
"""

from __future__ import annotations

import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright

from secrets_paths import default_auth_json_path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="手動ログイン後に storage_state を保存")
    p.add_argument(
        "--out",
        type=Path,
        default=None,
        help="保存先（未指定時は Git 外の既定パス）",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    out: Path = (args.out if args.out is not None else default_auth_json_path()).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.instagram.com/accounts/login/", wait_until="domcontentloaded")

        input("ログインが完了したら Enter を押して storage_state を保存... ")

        context.storage_state(path=str(out))
        print(f"保存しました: {out}")

        context.close()
        browser.close()


if __name__ == "__main__":
    main()
