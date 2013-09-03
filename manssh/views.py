import json
from django.conf import settings
from django.http import HttpResponse
from django.template import Context, RequestContext, Template, loader

keys = []

def index(request):
    strRet = ''
    fHandle = None

    fHandle = open(settings.SSH_AUTHOR_FILE, 'r')
    strRet = fHandle.read()

    lines = strRet.splitlines()
    idx = 0
    while(len(keys) > 0):
        keys.pop()
    for line in lines:
        if(line.strip() == ''):
            continue
        key = MySSHKey.parseKey(line)
        key.idx = idx
        idx += 1
        keys.append(key)

    t = loader.get_template('list.html')
    c = RequestContext(request, {
        'ssh_keys': keys,
    })

    rendered_template = t.render(c)
    return HttpResponse(rendered_template)

def getKeyByIndex(request):
    idx = 0
    key = MySSHKey('ssh-rsa', '', '')
    if('keyIdx' in request.GET.keys()):
        idx = int(request.GET['keyIdx'])
        key = keys[idx]

    return HttpResponse(json.dumps({'id':key.getId(), 'type': key.getType(), 'key': key.getKey()}), mimetype='application/json')

def getKeys(request):
    key_arr = []
    key_idx = 0;
    for key in keys:
        key_arr.append({ 'idx': key_idx, 'media_url': settings.MEDIA_URL, 'id': key.getId(), 'type': key.getType(), 'key': key.getKey(), 'skey': key.getShortKey()})
        key_idx += 1
    return HttpResponse(json.dumps(key_arr), mimetype='application/json')

def deleteKey(request):
    try:
        idx = int(request.GET['keyIdx'])
        key = keys[idx]
        keys.remove(key)
        store_keys()
        return HttpResponse("")
    except Exception as ex:
        return HttpResponse("Error: %s" % ex)

def saveKey(request):
    try:
        mkeyStr = request.GET['curKey']
        midStr = request.GET['curId']
        mtypeStr = request.GET['curType']
        actionTypeStr = request.GET['actionType']

        action = 0  # new

        if(len(actionTypeStr) > 0):
            action = 1  # edit

        # split key in case of add new key
        if(action == 0 and ' ' in mkeyStr):
            arr = mkeyStr.split(' ')
            if(len(arr) == 1):
                mtypeStr = 'ssh-rsa'
                midStr = ''
            elif(len(arr) == 2):
                mtypeStr = arr[0]
                mkeyStr = arr[1]
                midStr = ''
            elif(len(arr) == 3):
                mtypeStr = arr[0]
                mkeyStr = arr[1]
                midStr = arr[2]
            else:
                raise Exception("The new SSH key contains many spaces. Please check again.")

        dupplicated_idx = -1
        for i in range(0, len(keys)):
            key = keys[i]
            if(key.getKey() == mkeyStr):
                dupplicated_idx = i
                break

        # check dupplicated
        if(action == 0 and dupplicated_idx != -1):
            # new key was existed
            raise Exception("The SSH key was existed. Please check again.")
        if(action == 1 and dupplicated_idx!= -1 and dupplicated_idx != int(actionTypeStr)):
            # edit key was dupplicated with other
            raise Exception("The SSH key was dupplicated with other key. Please check again.")

        if(action == 0):
            # new
            key = MySSHKey(mtypeStr, mkeyStr, midStr)
            keys.append(key)
        elif(action == 1):
            # edit
            key = keys[int(actionTypeStr)]
            key.setId(midStr)
            key.setType(mtypeStr)
            key.setKey(mkeyStr)

        # update into file
        store_keys()

        return HttpResponse('')
    except Exception as ex:
        return HttpResponse("Error: %s" % ex)

def store_keys():
    fHandle = open(settings.SSH_AUTHOR_FILE, 'w')
    for key in keys:
        keyStr = "%s %s" % (key.getType(), key.getKey())
        if(len(key.getId().strip()) > 0):
            keyStr += " %s" % key.getId()
        fHandle.write(keyStr + "\n")
    fHandle.close()

class MySSHKey(object):


    def __init__(self, typeStr='ssh-rsa', keyStr='', idStr=''):
        self.__type = typeStr
        self.__key = keyStr
        self.__id = idStr

    def getType(self):
        return self.__type

    def setType(self, val):
        if(val is not None):
            self.__type = val
        return self.__type

    def getKey(self):
        return self.__key

    def setKey(self, val):
        if(val is not None):
            self.__key = val
        return self.__key

    def getShortKey(self, size=60):
        return self.__key[:size] + "..."

    def getId(self):
        return self.__id

    def setId(self, val):
        if(val is not None):
            self.__id = val
        return self.__id

    @staticmethod
    def parseKey(s):
        arr = s.split(' ')
        __type = arr[0]
        __key = arr[1]
        __id = ''
        if(len(arr) == 3):
            __id = arr[2]
        return MySSHKey(__type, __key, __id)

    def __unicode__(self):
        return '%s %s %s' % (self.__type, self.__id, self.__key)

    def __str__(self):
        return '%s %s %s' % (self.__type, self.__id, self.__key)