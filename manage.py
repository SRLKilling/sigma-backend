import sys
import os
import errno
import argparse

from settings import Settings


#*********************************************************************************************#
#**                                     Useful shortcuts                                    **#
#*********************************************************************************************#

def joinParams(params):
    if isinstance(params, list) or isinstance(params, tuple):
        params = ' '.join(params)
    return params

def runPython(params):
    params = joinParams(params)
    return os.system(Settings.ENV['PYTHON'] + ' ' + params)
    
def runPip(params):
    params = joinParams(params)
    return os.system(Settings.ENV['PIP'] + ' ' + params)

def runDjango(params):
    params = joinParams(params)
    return os.system(Settings.ENV['PYTHON'] + ' ' + Settings.PATH['DJANGO_MANAGER'] + ' ' + params)

    

def silent_remove(filename):
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise
    
    
#*********************************************************************************************#
#**                                         Actions                                         **#
#*********************************************************************************************#
    
def install():
    for r in Settings.REQUIREMENTS:
        if hasattr(Settings, 'PROXY') and Settings.PROXY != '':
            runPip(['install', '"'+r+'"', '--proxy', Settings.PROXY])
        else:
            runPip(['install', '"'+r+'"'])
    
def init():
    runDjango('collectstatic')
    runDjango('makemigrations')
    runDjango('migrate')
    
def reset():
    silent_remove('db.sqlite3')
    runDjango('makemigrations')
    runDjango('migrate')
    fixtures()
    
def fixtures():
    runPython([Settings.PATH['FIXTURES_GENERATOR'], Settings.PATH['FIXTURES_FILE']])
    runDjango(['loaddata', Settings.PATH['FIXTURES_FILE']])
    
    
    
#*********************************************************************************************#
#**                                           Main                                          **#
#*********************************************************************************************#

def usage():
    print("Incorrect parameters, use one of the following command")
    print("  install - install deps")
    print("  django [...] - run the django manage.py using given args")
    print("  run-push-server")
    print("  run-data-server")
    
    
def main():
    # TODO : add argparse support
    # parser = argparse.ArgumentParser(description='Used to easily manage the backend.')
    
    argv = sys.argv
    argc = len(sys.argv)
    
    if argc > 1:
        op = argv[1]
        
        if(op == "install"):
            return install()
            
        elif(op == "init"):
            return init()
        
        elif(op == "fixtures"):
            return fixtures()
            
        elif(op == "reset"):
            return reset()
            
        elif(op == "run-push-server"):
            return runPython('push-server/run-server.py')
            
        elif(op == "run-data-server"):
            return runPython('data-server/run-server.py')
         
        elif(op == "django"):
            return runDjango(argv[2:])
            
    usage()
    

if __name__ == '__main__':
    main()