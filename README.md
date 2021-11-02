# Slack-Communication-Visualization.
Slackのコミュニケーションを可視化する

## graphviz install
graphvizのインストール
```
brew install graphviz
pip install graphviz
```

## Log preparation
ログの準備

下記からエクスポートしたログをフォルダ毎jsonsディレクトリに入れる

※ワークスペース名/ディレクトリ名/YYYY-MM-DD.json で出力されるためそのまま設置する場合はscv.pyのパスを置き換えること

https://mu-club.slack.com/services/export　
（要管理者権限）

```
WorkingDirectory/
├ scv.py
├ jsons/
│ └ hoge/
│    └ hoge.json
│ └ huga/
│    └ huga.json
│
├　image/
  └ hoge
  └ hoge.svg

```
## Channel settings you want to visualize
可視化したいチャンネルの設定

複数チャンネルある場合、描画及び生成に時間がかかるため19行目のパスを変更する
>json_files = glob.glob("./logs/*/*.json") # 特定のチャンネルを確認する時はここを変更する

※9行目については社員リスト（ID:氏名）を先に生成する必要があるためそのままにしておくこと

## Execute
実行する

```
python scv.py
```

実行するとimageディレクトリに可視化対象としたチャンネルのdotファイルおよびsvgファイルが生成される
<img width="967" alt="スクリーンショット 2021-11-02 19 21 11" src="https://user-images.githubusercontent.com/42475390/139835404-a9eb4e7b-5457-42c0-a422-0749b84263c2.png">

拡張子およびレイアウトについては21行目で変更できる
>graph = Graph(format='svg', engine='sfdp')

参考：https://melborne.github.io/2013/04/02/graphviz-layouts/

すぐに結果を確認したい場合、コメントをとけば描画後ブラウザで確認ができる。
チャンネルが多いと描画が終わるたびに開かれるので注意
> graph.view() # 画像を見たい時用
