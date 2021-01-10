setup
===

1. create a user.
	* `sudo adduser --system kai`
2. create the work directory.
	* `sudo mkdir -p /var/service/kai`
3. copy the scripts.
	* `sudo cp -r src /var/service/kai/`
4. add permittion and set owner.
	* `sudo chown -R kai:kai /var/service/kai`
5. copy the systemd.
	* `sudo cp -r etc.in/systemd/system/* /etc/systemd/system`
6. edit env.
	* `sudo vim /etc/systemd/system/kai.service.d/myenv.conf`
6. run.
	* `sudo systemctl daemon-reload`
	* `sudo systemctl start kai.service`
