"""
秘密情報（storage_state・将来の API キー用パス等）の保存先を解決する。

既定は Git 作業ツリーの外:
  - 環境変数 VEXUM_SECRETS_DIR があればその絶対パス
  - なければ ユーザーホーム下の ~/.vexum_secrets（Windows も同様）

プロジェクト直下の .env（Git 対象外）を読み込むには python-dotenv を入れておく。
"""

from __future__ import annotations

import os
from pathlib import Path

_ROOT = Path(__file__).resolve().parent


def _try_load_dotenv() -> None:
    env_file = _ROOT / ".env"
    if not env_file.is_file():
        return
    try:
        from dotenv import load_dotenv

        load_dotenv(env_file)
    except ImportError:
        # python-dotenv 未導入時は、OS の環境変数または手動で VEXUM_SECRETS_DIR を設定する
        pass


_try_load_dotenv()


def get_secrets_dir() -> Path:
    raw = (os.environ.get("VEXUM_SECRETS_DIR") or "").strip()
    if raw:
        return Path(raw).expanduser().resolve()
    return (Path.home() / ".vexum_secrets").resolve()


def default_auth_json_path() -> Path:
    """Playwright storage_state（Instagram 等）の既定ファイルパス。"""
    return get_secrets_dir() / "auth.json"
