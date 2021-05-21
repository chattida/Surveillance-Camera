import subprocess

local = '/home/pi/Surveillance-Camera/record'
remote = 'gdrive:Surveillance-Camera'

command = 'rclone copy --update --verbose --transfers 30 --checkers 8 --contimeout 60s --timeout 300s --retries 3 --low-level-retries 10 --stats 1s "%s" "%s"' % (local, remote)

subprocess.call(command, shell=True)
