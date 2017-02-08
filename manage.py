import sys
import os
import errno
import argparse

import settings

#*********************************************************************************************#
#**                                     Useful shortcuts                                    **#
#*********************************************************************************************#

def joinParams(params):
    if isinstance(params, list) or isinstance(params, tuple):
        params = ' '.join(params)
    return params

def runPython(params):
    params = joinParams(params)
    return os.system(settings.ENV['PYTHON'] + ' ' + params)
    
def runPip(params):
    params = joinParams(params)
    return os.system(settings.ENV['PIP'] + ' ' + params)

def runDjango(params):
    params = joinParams(params)
    return os.system(settings.ENV['PYTHON'] + ' ' + settings.PATH['DJANGO_MANAGER'] + ' ' + params)

    

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
    install_deps()
    init()
    fixtures()
        
def install_deps():
    for r in settings.REQUIREMENTS:
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
    runPython([settings.PATH['FIXTURES_GENERATOR'], settings.PATH['FIXTURES_FILE']])
    runDjango(['loaddata', settings.PATH['FIXTURES_FILE']])
    
    
    
#*********************************************************************************************#
#**                                           Main                                          **#
#*********************************************************************************************#

def usage():
    print("Incorrect parameters, use one of the following command")
    print("  install - alias for install_deps + init + fixtures")
    print("  install-deps - install dependencies")
    print("  init - collect static and initialize database")
    print("  fixtures - load random fixtures into the database, as well as the frontend client, and the superuser")
    print("  reset - drop an recreate an all new database")
    print("  django [...] - run the django manage.py using given args")
    print("  run-push-server")
    print("  run-data-server")
    print("")
    print("To quickly start django, use :")
    print("  install (or reset if previously installed)")
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
            
        elif(op == "install-deps"):
            return install_deps()
            
        elif(op == "init"):
            return init()
        
        elif(op == "fixtures"):
            return fixtures()
            
        elif(op == "reset"):
            return reset()
            
        elif(op == "run-ws-server"):
            return runPython('ws_server/run-server.py')
            
        elif(op == "run-data-server"):
            return runDjango('runserver 127.0.0.1:8080')
         
        elif(op == "django"):
            return runDjango(argv[2:])
            
    usage()
    

if __name__ == '__main__':
    main()
