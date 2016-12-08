import random
import string
import sys

#*********************************************************************************************#
#**                                  Useful methods                                         **#
#*********************************************************************************************#
    
    
primary_keys = {}
def JSONizer(model, obj, sep=True):
    """
        Compute the primary key for the element and returns a JSON representation
    """
    global primary_keys
    if model not in primary_keys:
        primary_keys[model] = 1
    else:
        primary_keys[model] += 1
        
    json = ',' if sep else ''
    json += ' {"model": "%s", "pk": %d, "fields": { \n' % (model, primary_keys[model])
    
    first = True
    for field in obj:
        if not first:
            json += ', \n'
        else:
            first = False
            
        if isinstance(obj[field], str):
            obj[field] = '"%s"' % obj[field]
        elif isinstance(obj[field], bool):
            obj[field] = ('true' if obj[field] else 'false')
        else:
            obj[field] = '%d' % obj[field]
            
        json += '    "%s": %s' % (field, obj[field])
        
    json += '\n} }'
    return json
    
    
def randomlower(length):
    """
        Return a random lowercase string of given length
    """
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))
    
    
    
#*********************************************************************************************#
#**                                Random model generators                                  **#
#*********************************************************************************************#

def superUser():
    user = {}
    user["password"] = "pbkdf2_sha256$24000$023IXGyjNKJm$V2EYuhPjLnergchTULv4WNVgjUMUBqhYxkt6UP7Pd/0="
    user["email"] = "admin@sigma.fr"
    user["lastname"] = randomlower(8)
    user["firstname"] = randomlower(8)
    user["join_date"] = "2016-05-08T15:35:59.028Z"
    user["is_active"] = True
    user["is_superuser"] = True
    user["is_staff"] = True
    return JSONizer('sigma_core.user', user, False)
        
def randomUser():
    user = {}
    user["password"] = "pbkdf2_sha256$24000$9Z4lf8RjlRPh$OGIP7SSJIzxqtjbCCDL8J7+O4SnBPx3jd6/kOnqBRww="
    user["email"] = randomlower(20) + "@sigma.fr"
    user["lastname"] = randomlower(8)
    user["firstname"] = randomlower(8)
    user["join_date"] = "2016-05-08T15:35:59.028Z"
    user["is_active"] = True
    user["is_superuser"] = False
    user["is_staff"] = False
    return JSONizer('sigma_core.user', user)
        
        
    
#*********************************************************************************************#
#**                                          Main                                           **#
#*********************************************************************************************#
    

def generateFixtures(filepath, UserNum, GroupNum):
    f = open(filepath, 'w')
    f.write('[')
    
    f.write( superUser() )          # Generate admin
    for i in range(UserNum):        # Generate users
        f.write( randomUser() )
        
    f.write(']')

    

if __name__ == '__main__':
    generateFixtures(sys.argv[1], 10, 5)