import random
import string
import sys


USER_NUM = 500
GROUP_NUM = 300
CHAT_NUM = 30
MEMBER_NUM = (5, 50)

ACKNOW_NUM = 700
ACKNOW_INV_NUM = 500

EVENT_NUM = 100
PUBLICATION_NUM = 300
SHARED_NUM = 4
PARTICIPATION_NUM = 50
COMMENT_NUM = 10
LIKE_NUM = 50
TAG_NUM = 20

GROUP_FIELD_NUM = (1, 5)

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

def randombool(p=0.5):
    """
        Return True with probability p, and False with 1-p
    """
    return bool(random.getrandbits(1))


def randint_norepeat(l, a, b):
    """
        Select a random int beetwen a and b, that is not already in list l
    """
    c = random.randint(a, b)
    while c in l:
        c = random.randint(a, b)
    return c

def randomdate():
    s=[str(random.randint(1,9)) for i in range(12)]
    p=[str(random.randint(0,5)) for i in range(2)]
    d="20"+s[0]+s[1]+"-0"+s[2]+"-0"+s[3]+"T1"+s[4]+":"+p[0]+s[6]+":"+p[1]+s[8]+".008Z"
    return d

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
    user["join_date"] = randomdate()
    user["is_active"] = True
    user["is_superuser"] = False
    user["is_staff"] = False
    user['school'] = "1"
    return JSONizer('sigma_core.user', user)



def randomGroup():
    group = {}
    group['name'] = randomlower(15)
    group['description'] = randomlower(50)
    group['is_protected'] = False
    group['can_anyone_ask'] = randombool()
    group['need_validation_to_join'] = randombool()
    group['members_visibility'] = random.randint(0, 2)
    group['group_visibility'] = random.randint(0, 2)
    return JSONizer('sigma_core.group', group)

def polytechnique():
    group = {}
    group['name'] = "polytechnique"
    group['description'] = "l'ecole de denis merigoux"
    group['is_protected'] = True
    group['can_anyone_ask'] = False
    group['need_validation_to_join'] = True
    group['members_visibility'] = 0
    group['group_visibility'] = 0
    return JSONizer('sigma_core.group', group)

def randomEvent(user):
    event = {}
    event['name'] = randomlower(10)
    event['description'] = randomlower(50)
    event['date_start'] = randomdate()
    event['date_end'] = randomdate()
    event['place_name'] = randomlower(20)
    event['author'] = user
    return JSONizer('sigma_core.event', event)

def randomParticipation(user, event):
    part = {}
    part['user'] = user
    part['event'] = event
    part['status'] = random.randint(0, 1)
    return JSONizer('sigma_core.participation', part)

def randomPublication(user, group, event = 0):
    publication = {}
    publication['author'] = user
    if event:
        publication['related_event'] = event
    publication['date'] = randomdate()
    publication['title'] = randomlower(15)
    publication['content'] = randomlower(100)
    publication['internal'] = randombool(0.8)
    publication['last_commented'] = randomdate()
    return JSONizer('sigma_core.publication', publication)

def generateGroupChat(group):
    chat = {}
    chat['group'] = group
    chat['is_full_group_chat'] = True
    return JSONizer('sigma_core.chat', chat)

def generateNoGroupChat():
    chat = {}
    chat['is_full_group_chat'] = False
    return JSONizer('sigma_core.chat', chat)

def generateChatMember(user, chat):
    chatmember = {}
    chatmember['chat']=chat
    chatmember['user']=user
    chatmember['join_date']=randomdate()
    return JSONizer('sigma_core.chatmember', chatmember)

def randomChatMessage(user, chat):
    chatmessage = {}
    chatmessage['chat']=chat
    chatmessage['user']=user
    chatmessage['message']="Salut, c'est cool"
    chatmessage['created_date'] = randomdate()
    return JSONizer('sigma_core.chatmessage', chatmessage)

def randomTag(user, publication):
    tag = {}
    tag['user'] = user
    tag['publication'] = publication
    tag['tagged'] = random.randint(1, USER_NUM)
    return JSONizer('sigma_core.tag', tag)

def randomLike(user, publication):
    like = {}
    like['user'] = user
    like['publication'] = publication
    return JSONizer('sigma_core.like', like)

def randomComment(user, publication):
    comment = {}
    comment['publication'] = publication
    comment['user'] = user
    comment['date'] = randomdate()
    comment['comment'] = randomlower(random.randint(50, 1000))
    return JSONizer('sigma_core.comment', comment)


def share(publication, group, user):
    shared = {}
    shared['group'] = group
    shared['publication'] = publication
    shared['author'] = user
    shared['date'] = randomdate()
    date = randomdate()
    return JSONizer('sigma_core.sharedpublication', shared)

def randomGroupField(group):
    group_field = {}
    group_field['group'] = group
    group_field['name'] = randomlower(8)
    group_field['type'] = random.randint(0, 3)
    group_field['accept'] = ""
    group_field['protected'] = randombool(0.5)
    group_field['multiple_values_allowed'] = randombool(0.2)
    return JSONizer('sigma_core.groupfield', group_field)

def generateMember(group, user, sa):
    member = {}
    member['group'] = group#generate chat members
    member['user'] = user
    member['created'] = randomdate()
    member['hidden'] = randombool()
    member['is_super_administrator'] = sa
    member['is_administrator'] = member['is_super_administrator'] or randombool(0.1)
    member['has_invite_right'] = member['is_administrator'] or randombool(0.2)
    member['has_contact_right'] = member['is_administrator'] or randombool(0.2)
    member['has_publish_right'] = member['is_administrator'] or randombool(0.2)
    member['has_kick_right'] = member['is_administrator'] or randombool(0.2)

    return JSONizer('sigma_core.groupmember', member)

def randomGroupFieldValue(member, field):
    group_field_value = {}
    group_field_value['membership'] = member
    group_field_value['field'] = field
    group_field_value['value'] = randomlower(8)
    return JSONizer('sigma_core.groupfieldvalue', group_field_value)



unique_akn = set()
def randomAknowledgment():
    global unique_akn
    A, B = random.randint(1, GROUP_NUM), random.randint(1, GROUP_NUM)
    while (A, B) in unique_akn:
        A, B = random.randint(1, GROUP_NUM), random.randint(1, GROUP_NUM)
    unique_akn.add( (A, B) )

    akn = {}
    akn['acknowledged'] = A
    akn['acknowledged_by'] = B
    akn['date'] = randomdate()
    return JSONizer('sigma_core.acknowledgment', akn)


unique_akn_inv = set()
def randomAknowledgmentInvitation():
    global unique_akn_inv
    A, B = random.randint(1, GROUP_NUM), random.randint(1, GROUP_NUM)
    while (A, B) in unique_akn_inv:
        A, B = random.randint(1, GROUP_NUM), random.randint(1, GROUP_NUM)
    unique_akn_inv.add( (A, B) )

    akn_inv = {}
    akn_inv['acknowledged'] = A
    akn_inv['acknowledged_by'] = B
    akn_inv['issued_by_invitee'] = randombool()
    akn_inv['date'] = randomdate()
    return JSONizer('sigma_core.acknowledgmentinvitation', akn_inv)


def generateOAuthClient():
    client = {}
    client['client_id'] = "bJeSCIWpvjbYCuXZNxMzVz0wglX8mHR2ZTKHxaDv"
    client['user'] = 1
    client['redirect_uris'] = ""
    client['client_type'] = "confidential"
    client['authorization_grant_type'] = "password"
    client['client_secret'] = "XjbfZS6Apq05PDTSL4CoFHGo7NsKVAa1XMVrVElk5N1t0dOSyqxrHPff6okAi6X6Du9XxrK4dl0mLQ0YlscJsjnL5IKhQagQdGv2SgumhYRFaMi6LtHNPXicmMr8oLdy"
    client['name'] = "frontend"
    client['skip_authorization'] = False

    return JSONizer('oauth2_provider.application', client)

#*********************************************************************************************#
#**                                          Main                                           **#
#*********************************************************************************************#

def generateFixtures(filepath):
    global primary_keys

    print('Generating fixtures :')
    f = open(filepath, 'w')
    f.write('[')

    print('  Generating superuser... ', end='')
    f.write( superUser() )                                              # Generate admin

    f.write(polytechnique())

    print('OK\n  Generating users... ', end='')
    for i in range(USER_NUM):                                           # Generate users
        f.write( randomUser() )

    print('OK\n  Generating groups... ', end='')
    for i in range(GROUP_NUM-1):                                          # Generate groups
        f.write( randomGroup() )


    print('OK\n  Generating group fields.. ', end='')
    group_fields = {}
    for i in range(1, GROUP_NUM):
        group_fields_num = random.randint(GROUP_FIELD_NUM[0], GROUP_FIELD_NUM[1])
        group_fields[i] = []
        for j in range(group_fields_num):                                     # Generate group_fields
            f.write( randomGroupField(i) )
            group_fields[i].append(primary_keys["sigma_core.groupfield"])

    print('OK\n  Generating memberships, chats, chatmembers and field values.. ', end='')
    for i in range(1, GROUP_NUM-1):
        member_num = random.randint(MEMBER_NUM[0], MEMBER_NUM[1])
        members = []
        f.write(generateGroupChat(i))
        for j in range(member_num):                                     # Generate members, chat members, chat messages
            member = randint_norepeat(members, 1, USER_NUM)
            members.append(member)
            f.write( generateMember(i, member, (j==0)) )
            f.write( generateChatMember(member, i))
            if random.randint(0,2)>1:
                f.write( randomChatMessage(member, i))

            group_fields_value_num = random.randint(1, len(group_fields[i]))    # Generate group field values
            already_selected_fields = []
            for k in range(0, group_fields_value_num):
                while True:
                    field = random.choice(group_fields[i])
                    if not field in already_selected_fields:
                        break
                already_selected_fields.append(field)
                f.write( randomGroupFieldValue(member, field) )

    print('OK\n Generating independant chats and chatmembers... ', end='')
    for i in range(GROUP_NUM-1, GROUP_NUM-1+CHAT_NUM):
        member_num = random.randint(MEMBER_NUM[0], MEMBER_NUM[1])
        members = []
        f.write(generateNoGroupChat())
        # for j in range(member_num):
        #     member = randint_norepeat(members, 1, USER_NUM)
        #     members.append(member)
        #     f.write( generateChatMember(member, i))
        #     if random.randint(0,2)>1:
        #         f.write( randomChatMessage(member, i))

    print('OK\n  Generating events... ', end='')
    for i in range(1, EVENT_NUM + 1):
        user = random.randint(1, USER_NUM)
        f.write(randomEvent(user))
        users = [user]
        for k in range(PARTICIPATION_NUM):
            if random.random() < 0.3:
                user = randint_norepeat(users, 1, PARTICIPATION_NUM)
                f.write(randomParticipation(user, i))


    print('OK\n  Generating publications... ', end='')
    for i in range(1, PUBLICATION_NUM + 1):
        user = random.randint(1, USER_NUM)
        group = random.randint(1, GROUP_NUM)
        if random.random() < 0.2:
            event = random.randint(1, EVENT_NUM)
            f.write(randomPublication(user, group, event))
        else:
            f.write(randomPublication(user, group))
        f.write(share(i, group, user))
        groups = [group]
        for k in range(SHARED_NUM):
            if random.random() < 0.1:
                group = randint_norepeat(groups, 1, GROUP_NUM)
                f.write(share(i, group, user))
        for k in range(COMMENT_NUM):
            if random.random() < 0.3:
                user = random.randint(1, USER_NUM)
                f.write(randomComment(user, i))
        for k in range(LIKE_NUM):
            if random.random() < 0.5:
                user = random.randint(1, USER_NUM)
                f.write(randomLike(user, i))
        for k in range(TAG_NUM):
            if random.random() < 0.3:
                user = random.randint(1, USER_NUM)
                f.write(randomTag(user, i))

    print('OK\n  Generating aknowledgment... ', end='')
    for i in range(1, ACKNOW_NUM):                                       # Generate aknowledgments
        f.write( randomAknowledgment() )

    print('OK\n  Generating aknowledgment invitations... ', end='')
    for i in range(1, ACKNOW_INV_NUM):                                       # Generate aknowledgments invitations
        f.write( randomAknowledgmentInvitation() )

    print('OK\n  Generation OAuth client... ', end='')
    f.write(generateOAuthClient())

    print('OK\n')
    f.write(']')


if __name__ == '__main__':
    generateFixtures(sys.argv[1])
