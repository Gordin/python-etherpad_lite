# This file is part of a program licensed under the terms of the GNU Lesser
# General Public License version 3 (or at your option any later version)
# as published by the Free Software Foundation.
#
# If you have not received a copy of the GNU Lesser General Public License
# along with this file, see <http://www.gnu.org/licenses/>.


from functools import partial
import json
import sys
if sys.hexversion >= 0x3000000:
    from urllib.request import urlopen
    from urllib.parse import urlencode
else:
    from urllib2 import urlopen
    from urllib import urlencode


class EtherpadException(Exception):
    pass


class EtherpadLiteClient(object):

    def __init__(self, base_params={}, base_url='http://localhost:9001/api',
                       api_version=1, timeout=20):
        self.api_version = api_version
        self.base_params = base_params
        self.base_url = base_url
        self.timeout = timeout

    def __call__(self, path, **params):
        data = urlencode(dict(self.base_params, **params)).encode('ascii')
        url = '%s/%i/%s' % (self.base_url, self.api_version, path)
        r = json.loads(urlopen(url, data, self.timeout).read().decode('utf-8'))
        if not r or not isinstance(r, dict):
            raise EtherpadException('API returned: %s' % r)
        if r.get('code') != 0:
            raise EtherpadException(r.get('message', r))
        return r.get('data')

    def __getattr__(self, name):
        return partial(self, name)

#Groups
    def createGroup(self):
        return self.__call__('createGroup')

    def createGroupIfNotExistsFor(self, groupMapper):
        return self.__call__('createGroupIfNotExistsFor',
                groupMapper=groupMapper)

    def deleteGroup(self, groupID):
        return self.__call__('deleteGroup', groupID=groupID)

    def listPads(self, groupID):
        return self.__call__('listPads', groupID=groupID)

    def createGroupPad(self, groupID, padName, text=False):
        if not text:
            return self.__call__('createGroupPad', groupID=groupID,
                    padName=padName)
        else:
            return self.__call__('createGroupPad', groupID=groupID,
                    padName=padName, text=text)

    def listSessionsOfGroup(self, groupID):
        return self.__call__('listSessionsOfGroup', groupID=groupID)
#Authors

    def createAuthor(self, name=''):
        if name != '':
            return self.__call__('createAuthor', name=name)
        else:
            return self.__call__('createAuthor')

    def createAuthorIfNotExistsFor(self, authorMapper,  name=''):
        if name != '':
            return self.__call__('createAuthorIfNotExistsFor',
                    authorMapper=authorMapper, name=name)
        else:
            return self.__call__('createAuthorIfNotExistsFor',
                    authorMapper=authorMapper)

    def listPadsOfAuthor(self, authorID):
            return self.__call__('listPadsOfAuthor', authorID=authorID)

    def listSessionsOfAuthor(self, authorID):
        return self.__call__('listSessionsOfAuthor', authorID=authorID)

#Sessions
    def createSession(self, groupID, authorID, validUntil):
        return self.__call__('createSession', groupID=groupID,
                authorID=authorID, validUntil=validUntil)

    def deleteSession(self, sessionID):
        return self.__call__('deleteSession', sessionID=sessionID)

    def getSessionInfo(self, sessionID):
        return self.__call__('getSessionInfo', sessionID=sessionID)

#Pad Content
    def getText(self, padID, rev=False):
        if rev:
            return self.__call__('getText', padID=padID, rev=rev)
        else:
            return self.__call__('getText', padID=padID)

    def setText(self, padID, text):
        return self.__call__('setText', padID=padID, text=text)

    def getHTML(self, padID, rev=False):
        if rev:
            return self.__call__('getHTML', padID=padID, rev=rev)
        else:
            return self.__call__('getHTML', padID=padID)

#Pad
    def createPad(self, padID, text=False):
        if not text:
            data = self.__call__('createPad', padID=padID)
        else:
            data = self.__call__('createPad', padID=padID, text=text)
        return data

    def getRevisionsCount(self, padID):
        return self.__call__('getRevisionsCount', padID=padID)

    def padUsersCount(self, padID):
        return self.__call__('padUsersCount', padID=padID)

    def deletePad(self, padID):
        return self.__call__('deletePad', padID=padID)

    def getReadOnlyID(self, padID):
        return self.__call__('getReadOnlyID', padID=padID)

    def setPublicStatus(self, padID, publicStatus):
        if publicStatus is 'true' or publicStatus is 'false':
            return self.__call__('setPublicStatus', padID=padID,
                    publicStatus=publicStatus)
        else:
            raise EtherpadException('publicStatus needs to be true or false')

    def getPublicStatus(self, padID):
        return self.__call__('getPublicStatus', padID=padID)

    def setPassword(self, padID, password):
        return self.__call__('setPassword', padID=padID, password=password)

    def isPasswordProtected(self, padID):
        return self.__call__('isPasswordProtected', padID=padID)

    def listAuthorsOfPad(self, padID):
        return self.__call__('listAuthorsOfPad', padID=padID)

    def getLastEdited(self, padID):
        return self.__call__('getLastEdited', padID=padID)


class Group:
    def __init__(self, client, groupMapper=False):
        self.client = client
        pass

    '''
    creates a new group.

    Example returns:
        {code: 0, message:"ok", data: {groupID: g.s8oes9dhwrvt0zif}}
    '''
    def createGroup(self):
        return self.__call__('createGroup')

    '''
    this functions helps you to map your application group ids to etherpad lite
    group ids.

    Example returns:
        {code: 0, message:"ok", data: {groupID: g.s8oes9dhwrvt0zif}}
    '''
    def createGroupIfNotExistsFor(self, groupMapper):
        return self.__call__('createGroupIfNotExistsFor', groupMapper)

    '''
    deletes a group.

    Example returns:
        {code: 0, message:"ok", data: null}
        {code: 1, message:"groupID does not exist", data: null}
    '''
    def deleteGroup(self, groupID):
        return self.__call__('deleteGroup', groupID)

    '''
    returns all pads of this group.

    Example returns:
        {code: 0, message:"ok", data: {padIDs :
            ["g.s8oes9dhwrvt0zif$test", "g.s8oes9dhwrvt0zif$test2"]}
        {code: 1, message:"groupID does not exist", data: null}
    '''
    def listPads(self, groupID):
        return self.__call__('listPads', groupID)

    '''
    creates a new pad in this group.

    Example returns:
        {code: 0, message:"ok", data: null}
        {code: 1, message:"pad does already exist", data: null}
        {code: 1, message:"groupID does not exist", data: null}
    '''
    def createGroupPad(self, groupID, padName, text=False):
        if text:
            return self.__call__('createGroupPad', padName, text)
        else:
            return self.__call__('createGroupPad', padName)

    '''
    returns all sessions of a group.

    Example returns:
        {"code":0,"message":"ok","data":{"s.oxf2ras6lvhv2132":{
            "groupID":"g.s8oes9dhwrvt0zif",
            "authorID":"a.akf8finncvomlqva",
            "validUntil":2312905480}}}
        {code: 1, message:"groupID does not exist", data: null}

    '''
    def listSessionsOfGroup(self, groupID):
        return self.__call__('listSessionsOfGroup', self.groupID)


class Author:
    '''
    creates a new author.

    Example returns:
        {code: 0, message:"ok", data: {authorID: "a.s8oes9dhwrvt0zif"}}
    '''
    def createAuthor(self, name=''):
        if name != '':
            return self.createAuthor(name)
        else:
            return self.createAuthor()

    '''
    this functions helps you to map your application author ids to etherpad
    lite author ids.

    Example returns:
        {code: 0, message:"ok", data: {authorID: "a.s8oes9dhwrvt0zif"}}
    '''
    def createAuthorIfNotExistsFor(self, authorMapper, name=''):
        if name != '':
            return self.createAuthorIfNotExistsFor(authorMapper, name)
        else:
            return self.createAuthorIfNotExistsFor(authorMapper)

    '''
    returns an array of all pads this author contributed to.

    Example returns:
        {code: 0, message:"ok", data: {padIDs:
            ["g.s8oes9dhwrvt0zif$test", "g.s8oejklhwrvt0zif$foo"]}}
        {code: 1, message:"authorID does not exist", data: null}
    '''
    def listPadsOfAuthor(self, authorID):
        return self.listPadsOfAuthor(authorID)

    '''
    '''
    def listSessionsOfAuthor(self, authorID):
        return self.__call__('listSessionsOfAuthor', authorID=authorID)
    pass


class Session:
    def __init__(self, client, groupID, authorID, validUntil):
        self.client = client
        self.groupID = groupID
        self.authorID = authorID
        self.validUntil = validUntil

    '''
    creates a new session. validUntil is an unix timestamp in seconds.

    Example returns:
        {code: 0, message:"ok", data: {sessionID: "s.s8oes9dhwrvt0zif"}}
        {code: 1, message:"groupID doesn't exist", data: null}
        {code: 1, message:"authorID doesn't exist", data: null}
        {code: 1, message:"validUntil is in the past", data: null}
    '''
    def createSession(self, groupID, authorID, validUntil):
        return self.__call__('createSession', groupID=groupID,
                authorID=authorID, validUntil=validUntil)

    '''
    deletes a session.

    Example returns:
        {code: 1, message:"ok", data: null}
        {code: 1, message:"sessionID does not exist", data: null}
    '''
    def deleteSession(self):
        return self.__call__('deleteSession', self.sessionID)

    '''
    returns informations about a session

    Example returns:
        {code: 0, message:"ok", data:
            {authorID: "a.s8oes9dhwrvt0zif",
            groupID: g.s8oes9dhwrvt0zif,
            validUntil: 1312201246}}
        {code: 1, message:"sessionID does not exist", data: null}
    '''
    def getSessionInfo(self, sessionID):
        return self.__call__('getSessionInfo', self.sessionID)


class Pad:
    def __init__(self, client, padID):
        self.client = client
        self.padID = padID

#Pad Content
    def getText(self, rev=False):
        if rev:
            return self.client.getText(self.padID, rev)
        else:
            return self.client.getText(self.padID)

    def setText(self, text):
        return self.client.getText(self.padID, text)

    def getHTML(self, rev=False):
        if rev:
            return self.client.getHTML(self.padID, rev)
        else:
            return self.client.getHTML(self.padID)

#Pad
    '''
    '''
    def createPad(self, padID, text=''):
        return self.client.createPad(padID, text)

    '''
    '''
    def getRevisionsCount(self):
        return self.client.getRevisionsCount(self.padID)

    '''
    '''
    def padUsersCount(self):
        return self.client.padUsersCount(self.padID)

    '''
    '''
    def deletePad(self):
        return self.client.deletePad(self.padID)

    '''
    '''
    def getReadOnlyID(self):
        return self.client.getReadOnlyID(self.padID)

    '''
    '''
    def setPublicStatus(self, publicStatus):
        return self.client.setPublicStatus(self.padID, publicStatus)

    '''
    '''
    def getPublicStatus(self):
        return self.client.getPublicStatus(self.padID)

    '''
    '''
    def setPassword(self, password):
        return self.client.setPassword(self.padID, password)

    '''
    '''
    def isPasswordProtected(self):
        return self.client.isPasswordProtected(self.padID)

    '''
    '''
    def listAuthorsOfPad(self):
        return self.client.listAuthorsOfPad(self.padID)

    '''
    '''
    def getLastEdited(self):
        return self.client.getLastEdited(self.padID)
