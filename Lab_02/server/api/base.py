from aiohttp import web
from server.crypto.idea import encode, decode
import traceback


class NotAuthenticated(Exception):
    pass


class SessionContext:
    pass
  

class SecureApi:
    @staticmethod
    def api(func):
        async def wrapper(self, r: web.Request):
            data = await r.json()
            print(data)
            try:
                ctx = SessionContext()
                ctx.sm = r.app.get('sm', None)
                ctx.fm = r.app.get('fm', None)
                ctx.data = data

                ret = {
                    'status': 'ok',
                    'result': await func(self, ctx)
                }
            except:
                ret = {
                    'status': 'error',
                    'result': traceback.format_exc()    
                }
            return web.json_response(ret)
        return wrapper

    @staticmethod
    def with_session(func):
        async def wrapper(self, ctx):
            sid = ctx.data['sid']
            session = ctx.sm.get(sid)

            session.ctx.data = ctx.data
            session.ctx.data = decode(session.ctx.data, session.key)
            res = await func(self, session.ctx)
            res = encode(res, session.key, session.sid)

            return res
        return wrapper

    @staticmethod
    def with_auth(func):
        async def wrapper(self, ctx):
            if not getattr(ctx, 'login', None):
                raise NotAuthenticated()
            return await func(self, ctx)
        return wrapper
