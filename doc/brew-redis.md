To have launchd start redis at login:
  ln -sfv /usr/local/opt/redis/*.plist q
Then to load redis now:
  launchctl load ~/Library/LaunchAgents/homebrew.mxcl.redis.plist
Or, if you don't want/need launchctl, you can just run:
  redis-server /usr/local/etc/redis.conf
==> Summary
🍺  /usr/local/Cellar/redis/3.0.5: 9 files, 892K


/opt/local/etc/LaunchDaemons/org.macports.redis/org.macports.redis.plist
/opt/local/bin/redis-server /opt/local/etc/redis-daemon.conf
/opt/local/bin/daemondo --label=redis --start-cmd /opt/local/etc/LaunchDaemons/org.macports.redis/redis.wrapper start ; --stop-cmd /opt/local/etc/LaunchDaemons/org.macports.redis/redis.wrapper stop ; --restart-cmd /opt/local/etc/LaunchDaemons/org.macports.redis/redis.wrapper restart ; --pid=none


scrapy startproject books
