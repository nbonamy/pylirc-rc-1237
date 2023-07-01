install:
	sudo ln -sf  $(PWD)/etc/pylirc-rc-1237.service /etc/systemd/system/
	sudo systemctl enable pylirc-rc-1237.service
	sudo systemctl start pylirc-rc-1237.service
	