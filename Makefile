install:
	sudo ln -sf  $(PWD)/etc/pylirc-rc-1237.service /etc/systemd/system/
	sudo systemctl enable pylirc-rc-1237.service
	sudo systemctl start pylirc-rc-1237.service

uninstall:
	sudo systemctl stop pylirc-rc-1237.service
	sudo systemctl disable pylirc-rc-1237.service
	
status:
	sudo service pylirc-rc-1237 status

restart:
	sudo service pylirc-rc-1237 restart

pm2:
	pm2 start ecosystem.config.js
	pm2 save

