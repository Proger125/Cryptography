from datetime import datetime, timedelta


class SessionNotFound(Exception):
    pass


class SessionExpired(Exception):
    pass


class Session:
    def __init__(self, exp, key, ctx, sid):
        self.exp = exp
        self.key = key
        self.sid = sid
        self.ctx = ctx

    def is_valid(self, ts):
        return ts < self.exp


class SessionManager:
    last_sid = 1

    def __init__(self):
        self.sessions = {}

    def new(self, key, ctx):
        while True:
            sid = str(SessionManager.last_sid + 1)
            SessionManager.last_sid += 1

            if not self.sessions.get(sid, None):
                session = Session(
                    exp=datetime.now() + timedelta(days=1),
                    key=key,
                    sid=sid,
                    ctx=ctx,
                )
                self.sessions[sid] = session
                return session

    def get(self, sid):
        session: Session = self.sessions.get(sid, None)
        if not session:
            raise SessionNotFound()
        if not session.is_valid(datetime.now()):
            self.sessions.pop(session)
            raise SessionExpired()
        return session
