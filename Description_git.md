# Description git
バージョン管理ツールGit,GitHubの使い方

## Gitとは？
プログラムのソースなどの変更履歴を記録・追跡するためのシステム

各ユーザのワーキングディレクトリに、全履歴を含むリポジトリの複製が作られるため、ネットワークにアクセスできない状況においても、履歴の調査や変更の記録といった作業を行うことができる。

## Gitを使うメリット
- 過去にコミットした内容に戻すことが簡単にできる
  - 変更前のコピーをとって、戻したい時に大量のファイルから特定のファイルを探しだすことを防ぐことができる
- 開発メンバーごとにブランチを切って、あとから一斉にマージすると言ったことができる
- GitHubを使えばグループでソースの管理などを行えてとても便利

## Gitのインストール
- Linux

  ```
  $ sudo apt install git
  ```

- Windows

  [Git for Windows](https://gitforwindows.org/)などのインストーラーでインストールする

## Gitの大まかな流れ
1. `git init`でリポジトリを作成
1. ファイルの追加や変更などをする
1. `git add`で変更したファイルをステージングエリアに追加する
1. `git commit`でステージングエリアにあるファイルをコミットする

この手順を繰り返してソースの管理を行う

## 実際に使ってみる
1. リポジトリを作成する

  `git init`でそのディレクトリをgitで管理できるようになる
  ```bash
  $ mkdir test
  $ cd test
  $ git init
  ```

1. 変更を加えて管理するファイルを追加する ( ステージングエリアにファイルを追加 )

  ```bash
  $ touch test.txt
  $ git add test.txt
  ```

1. 変更した内容をコミットする

  ```bash
  $ git commit -m "履歴につけるメッセージ(何でもいい)"
  ```

## GitHubの使い方
GitHubを使うことでオンライン上でソースの管理を行うことができる

GitHubでリポジトリを作成するときは、`New repository`でリポジトリを作成する

## リモートリポジトリにファイルの変更を反映させてみる
1. testリポジトリをGitHub上に作っておく

1. testリポジトリで`Clone or download`で`https://github.com/username/test.git`となっている。このURLをコピーする

1. ローカルのtestディレクトリで`git add remote origin https://github.com/username/test.git`を実行する

1. `git push origin master`で変更した内容をリモートリポジトリにプッシュする

1. ページの更新を行うと`test.txt`が追加され、コミット時につけたメッセージが表示される

## Gitのコマンド
### よく使うGitコマンド

|コマンド|説明|
|:---|:---|
|git init|ローカルリポジトリを新規作成する|
|git rm -f ファイル名|Gitで管理されているファイルの削除|
|git mv ファイル名 ファイル名|gitで管理されているファイルの名前変更・ディレクトリの変更|
|git add ファイル名|指定したファイルをコミットの対象にする(ステージングエリアに移す)|
|git commit -m "コメント"|変更した内容をコミットする|
|git log|コミットのログを確認する|
|git diff コミットID コミットID|2つのコミットの差異を表示する|
|git rm --cached ファイル名|ファイルを残したまま外す|
|git status|現在の変更・追加などの状態を表示する|
|git clone アドレス|リモートリポジトリをローカルにコピーする|
|git pull|リモートリポジトリの変更をローカルに反映させる|
|git push|ローカルリポジトリの変更をリモートリポジトリに反映させる|

`git add`のオプション

|コマンド|説明|
|:---|:---|
|git add * またはgit add -A|リポジトリ内のすべてのファイルを管理対象に加える(何も考えずにやるならこれ)|
|git add -u|変更があったものだけステージングエリアに移す（追加したものは管理対象にならない）|

### 設定用のコマンド
|コマンド|説明|
|:---|:---|
|git config --list|設定内容の一覧を表示する|
|git config --global user.email アドレス|メールアドレスの設定|
|git config --global user.name "名前"|名前の設定|
|git config --global gui.encoding charcterset|文字コード設定|
|git config --global core.quotepath false|日本語ファイル名の表示設定|
|git config --global color.diff auto|diffの色設定|
|git config --global color.status auto|statusの色設定|
|git config --global color.branch auto|branchの色設定|
|git config --global http.proxy address:port|プロキシ設定|

`--global`オプションはシステム全体で設定する場合につける

リポジトリごとに設定をしたい場合は`--local`をつけると良い(例えばプロキシの設定)

設定を削除したい場合`--unset`オプションをつける

最低限設定しておくと良いコマンド
```bash
$ git config --global user.email アドレス
$ git config --global user.name 名前
$ git config --global gui.encoding utf-8
$ git config --global core.quotepath false
$ git config --global color.diff auto
$ git config --global color.status auto
$ git config --global color.branch auto
```

### pushしたときに名前とパスワードが聞かれる時の対処

`~/.netrc`ファイルに以下の内容を書き込むだけで良いらしい

```
machine github.com
login myname
password xxxxxxxxxx
```

## ブランチを切って作業する

masterブランチをそのまま編集してコミットしていくのはあまり良くない

開発フローは色々あるがチームで好きなものを決めて開発するとよい(個人的には`GitFlow`)

Gitサーバとか構築してるなら`GitFlow`モデルが良いと思われる

1. 開発用ブランチ(`develop`が多い)を切ってそこで作業する
    - 基本的に`develop`は`feature`のmerge commitだけにしたほうがいいらしい

1. 個別の機能を開発する場合は`feature/1`,`feature-1`などつけてそこで実装する

1. `feature`で実装したら`develop`にcheckoutしてmergeする

---
GitHubを使って開発する場合

Githubを使う場合は`Github Flow`なる開発フローがいいらしい

1. Github上に空のリポジトリを作成

1. 作成したリポジトリをcloneする

1. `develop`ブランチを切る

1. 機能追加する場合`feature`ブランチを切って開発

1. 実装できたら`develop`ブランチにmerge

1. 安定版がリリースできたら`master`ブランチにmerge

### ブランチ操作

|コマンド|説明|
|:---|:---|
|git branch|ブランチの一覧を表示|
|git branch `branch-name`|ブランチの作成|
|git branch -d `branch-name`|指定したブランチの削除|
|git branch -m `old-branch` `new-branch`|ブランチ名を変更する|
|git branch -m `new-branch`|現在のブランチ名を変更する|
|git checkout `branch-name`|指定したブランチに移動|
|git checkout -b `branch-name`|ブランチを作成してcheckout|
|git merge `branch`|現在のブランチに指定したブランチをマージ|


### 参考

- [サルでもわかるGit入門 ~バージョン管理を使いこなそう~](https://backlog.com/ja/git-tutorial/)
- [【初心者向け】gitのbranch運用入門【git flow もどき】 ](http://ism1000ch.hatenablog.com/entry/2014/03/31/152441)
- [Gitを使った有名な開発フロー、GitFlowとGitHub Flowについて ](https://2017.l2tp.org/archives/470)  
