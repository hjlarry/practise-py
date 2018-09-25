import subprocess

completed = subprocess.run(['ls', '-l'])
print('return code:',completed.returncode)