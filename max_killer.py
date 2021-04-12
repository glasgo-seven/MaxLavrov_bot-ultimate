import os
import sys

print('\t/// BOT IS STOPPING ///')
killer = open('killer.bat', 'w')
killer.write('Taskkill /PID ' + sys.argv[1] + " /F")
killer.close()
os.system('killer.bat')
print('\t/// BOT STOPPED ///')
os.remove('killer.bat')
print('\t/// killer.bat IS DELETED ///')
print('/// WORK IS DONE ///')
