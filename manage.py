import sys
import os
import pip

REQUIREMENTS = [

    # Django and DRF related
    "Django == 1.10",
    "djangorestframework == 3.5.3",
    "django-cors-headers == 1.3",
    "django-oauth-toolkit == 0.11",
    "django-filter == 0.2.1",
    
    # Tornado
    "tornado == 4.4",
]

PROXY = 'kuzh.polytechnique.fr:8080'

PYTHON = 'python'

DJANGO_MANAGER = ' data-server/manage.py '

def install():
    for r in REQUIREMENTS:
        if PROXY != '':
            pip.main(['install', r, '--proxy', PROXY])
        else:
            pip.main(['install', r, '--proxy', PROXY])
    
    
    os.system(PYTHON + DJANGO_MANAGER + 'collectstatic')
    
    
def usage():
    print("Incorrect parameters, use one of the following command")
    print("  install - install deps")
    print("  django [...] - run the django manage.py using given args")
    print("  run-push-server")
    print("  run-data-server")
    
    
def main():
    argv = sys.argv
    argc = len(sys.argv)
    
    if argc > 1:
        op = argv[1]
        
        if(op == "install"):
            install()
            return
            
        elif(op == "run-push-server"):
            os.system(PYTHON + " push-server/run-server.py")
            return
            
        elif(op == "run-data-server"):
            os.system(PYTHON + " data-server/run-server.py")
            return
         
        elif(op == "django"):
            args = ' '.join(argv[2:])
            os.system(PYTHON + DJANGO_MANAGER + args)
            return
            
    usage()
    

if __name__ == '__main__':
    main()