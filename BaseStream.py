# Copyright (C) 2009 AG Projects. See LICENSE for details.     
#

__all__ = ['BaseStream', 'log_debug', 'log_error', 'log_info', 'STATE_IDLE', 'STATE_DNS_LOOKUP', 'STATE_DNS_FAILED', 'STATE_CONNECTING',
           'STATE_CONNECTED', 'STATE_FAILED', 'STATE_FINISHED', 'STREAM_IDLE', 'STREAM_WAITING_DNS_LOOKUP', 'STREAM_RINGING', 'STREAM_ADDING',
           'STREAM_CONNECTING', 'STREAM_PROPOSING', 'STREAM_CONNECTED', 'STREAM_DISCONNECTING', 'STREAM_CANCELLING', 'STREAM_FAILED', 'STREAM_INCOMING']

from application.notification import NotificationCenter

from BlinkBase import NotificationObserverBase
from BlinkLogger import BlinkLogger


STATE_IDLE = "IDLE"
STATE_DNS_LOOKUP = "DNS_LOOKUP"
STATE_DNS_FAILED = "DNS_FAILED"
STATE_CONNECTING = "CONNECTING"
STATE_CONNECTED = "CONNECTED"
STATE_FAILED = "FAILED"
STATE_FINISHED = "FINISHED"

STREAM_IDLE = "IDLE"
STREAM_WAITING_DNS_LOOKUP = "WAITING_DNS_LOOKUP"
STREAM_RINGING = "RINGING"
STREAM_ADDING = "ADDING"
STREAM_CONNECTING = "CONNECTING"
STREAM_PROPOSING = "PROPOSING"
STREAM_CONNECTED = "CONNECTED"
STREAM_DISCONNECTING = "DISCONNECTING"
STREAM_CANCELLING = "CANCELLING"
STREAM_FAILED = "FAILED"
STREAM_INCOMING = "INCOMING"



def log_info(session, text):
    BlinkLogger().log_info(u"[session to %s] %s" % (session.remoteParty, text))


def log_debug(session, text):
    BlinkLogger().log_debug(u"[session to %s] %s" % (session.remoteParty, text))


def log_error(session, text):
    BlinkLogger().log_error(u"[session to %s] %s" % (session.remoteParty, text))


class BaseStream(NotificationObserverBase):
    sessionController = None
    stream = None
    status = None

    def __new__(cls, *args, **kwargs):
        return cls.alloc().initWithOwner_stream_(*args)

    def initWithOwner_stream_(self, owner, stream):
        self = super(BaseStream, self).init()
        if self:
            self.sessionController = owner
            self.stream = stream
        return self

    def changeStatus(self, newstate, fail_reason=None):
        data = {"state": newstate, "detail": fail_reason}
        NotificationCenter().post_notification("BlinkStreamHandlerChangedState", sender=self, data=data)

    @property
    def isConnecting(self):
        return self.status in (STREAM_WAITING_DNS_LOOKUP, STREAM_RINGING, STREAM_PROPOSING, STREAM_ADDING, STREAM_CONNECTING, STREAM_INCOMING)

    @property
    def session(self):
        return self.sessionController.session

    @property
    def remoteParty(self):
        return self.sessionController.remoteParty if self.sessionController else '?'

    @property
    def sessionManager(self):
        return self.sessionController.owner

    def removeFromSession(self):
        self.sessionController.removeStreamHandler(self)

    def sessionRinging(self):
        pass

    def sessionStateChanged(self, newstate, detail):
        pass


