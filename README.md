# BCG-list-up

Playwright（Python）によるブラウザ自動化の仕様・スクリプト集。  
リポジトリ: [github.com/hmatsuo-ai/BCG-list-up](https://github.com/hmatsuo-ai/BCG-list-up)

## セットアップ

```bash
pip install -r requirements.txt
playwright install chromium
```

秘密情報は **`BCG_LIST_UP_SECRETS_DIR`**（未設定時は `~/.bcg-list-up-secrets`）に置き、`.env` は `.env.example` をコピーして作成する。Git にコミットしないこと。

詳細は `仕様書_ブラウザ自動化_Python.md` を参照。
