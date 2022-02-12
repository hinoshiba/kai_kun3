setup
===

1. 動作ディレクトリの作成
	* `sudo mkdir -p /var/service/kai`
2. 本リポジトリの内容を全て設置
	* `sudo cp -r <repository>/* /var/service/kai/`
3. systemdファイルの設置
	1. コピー
		* `sudo cp -r etc.in/systemd/system/* /etc/systemd/system`
	2. 環境変数の設定
		* `sudo vim /etc/systemd/system/kai.service.d/myenv.conf`
	3. 読み込みと有効化
		* `sudo systemctl daemon-reload`
		* `sudo systemctl enable kai.service`
4. docker-composeのbuild
	* `docker-compose down && docker-compose build`
5. 起動と有効化
	* `sudo systemctl start kai.service`

## アップデート

手順、4.から5. を、ファイルを設置した上で実施する
