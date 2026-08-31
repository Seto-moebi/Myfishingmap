# 共有マップのデプロイ手順

このアプリは今まで各端末のブラウザ内（IndexedDB）に写真を保存していたため、PCとスマホで別々の地図になっていました。
今回、写真とピン情報をサーバー側（Cloudinary）に保存するように変更したので、**同じサーバーにアクセスすれば誰でも同じ地図・同じピンが見える**ようになります。
（いったんログイン機能は無効化してあり、URLを知っている人なら誰でもそのまま地図を見られます。パスワード制にしたくなったら教えてください。）

## 全体構成
- **Render**（無料）: このFlaskアプリを動かすサーバー
- **Cloudinary**（無料）: アップロードされた写真本体と、GPS・題名などのメタ情報を保存する場所
  - Renderの無料プランはディスクが一時的（再起動で消える）なため、写真はCloudinary側に永続保存します

## 1. Cloudinaryアカウントを作る
1. https://cloudinary.com/users/register/free にアクセスし、無料アカウントを作成
2. ログイン後のダッシュボード（Settings → Access Keys、または最初のホーム画面）で以下をメモする
   - Cloud name
   - API Key
   - API Secret

## 2. コードをGitHubに置く
Renderからデプロイするために、このフォルダ（`photo_gps_map`）をGitHubリポジトリにpushしてください。
```
cd photo_gps_map
git init
git add .
git commit -m "shared fishing map"
```
GitHub上に新規リポジトリを作り、`git remote add origin ...` して `git push -u origin main` してください。
（`.env` はコミットしないよう `.gitignore` に入れてあります）

## 3. Renderにデプロイする
1. https://render.com にアクセスし、GitHubアカウントで無料登録
2. 「New +」→「Web Service」→ 先ほどのGitHubリポジトリを選択
3. 設定項目
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn server:app`（`Procfile` があるので自動検出される場合もあります）
   - Instance Type: Free
4. 「Environment」タブで以下の環境変数を追加（`APP_PASSWORD`はログイン機能を無効化中のため現状使われません）
   | Key | Value |
   |---|---|
   | `FLASK_SECRET_KEY` | ランダムな長い文字列（下記コマンドで生成） |
   | `CLOUDINARY_CLOUD_NAME` | Cloudinaryでメモした値 |
   | `CLOUDINARY_API_KEY` | Cloudinaryでメモした値 |
   | `CLOUDINARY_API_SECRET` | Cloudinaryでメモした値 |

   `FLASK_SECRET_KEY` の生成例（手元のPCで実行）:
   ```
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
5. 「Create Web Service」をクリックすると自動でビルド・デプロイが始まります。数分待つと `https://xxxxx.onrender.com` のようなURLが発行されます。

## 4. スマホ・PCからアクセス
発行されたURL（`https://xxxxx.onrender.com`）を開けば、ログイン不要でそのまま同じ地図・同じ写真・同じピンが見られます。

URLはブックマークやホーム画面追加（iPhoneなら共有→ホーム画面に追加）しておくと便利です。

## 注意点
- Render無料プランは15分アクセスがないとスリープし、次のアクセス時に起動まで数十秒かかります（データは消えません。消えるのは常駐プロセスだけです）。
- Cloudinary無料プランは画像1枚あたり最大10MB程度の制限があります（アカウント設定次第で変わる場合があります）。スマホの高解像度写真でも通常は収まりますが、超える場合はアップロードが失敗します。
- 現在はログイン不要の設定にしています。URLを知っていれば誰でも見られる状態なので、公開範囲を絞りたくなったらいつでもログインを再度有効化できます。

## ローカルでの動作確認
Cloudinaryの環境変数を設定した状態で、以下でローカル起動できます。
```
cd photo_gps_map
pip install -r requirements.txt
set FLASK_SECRET_KEY=devsecret
set CLOUDINARY_CLOUD_NAME=...
set CLOUDINARY_API_KEY=...
set CLOUDINARY_API_SECRET=...
python server.py
```
`http://localhost:5000` を開き、パスワードでログインして動作確認してください。
