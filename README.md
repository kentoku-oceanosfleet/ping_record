# ping_record

ISO8601形式でタイムスタンプを取得するシンプルなツール

## get_timestamp.shの使い方

```bash
./get_timestamp.sh
```

実行すると、以下のような形式でタイムスタンプが出力されます：
```
2024-03-29T12:34:56+09:00
```

## get_ping.shの使い方

```bash
./get_ping.sh <destination_ip>
```

実行すると、指定したIPアドレスに対して1回pingを実行し、以下のようなJSON形式で結果を出力します：
```
{'dst':'8.8.8.8','response_ms':20.1}
```

### パラメータ
- destination_ip: ping送信先のIPアドレス（例：8.8.8.8）

### 出力形式
- dst: 宛先IPアドレス
- response_ms: pingの応答時間（ミリ秒）

## テスト方法

このプロジェクトのテストはDockerコンテナ内で実行されます。以下の手順でテストを実行できます：

1. test/ディレクトリに移動
```bash
cd test
```

2. Dockerイメージをビルドしてテストを実行
```bash
docker build -t timestamp-test -f Dockerfile.test .. && docker run timestamp-test
```

### テストの内容

テストでは以下の3つの観点を確認しています：

1. スクリプトが正常に実行できること
2. 出力がISO8601形式であること
3. タイムスタンプが現在時刻に近い値であること（60秒以内）

## 要件

- Docker
  - テストを実行する場合のみ必要です
- シェルスクリプトを実行できる環境
  - macOSまたはLinux環境