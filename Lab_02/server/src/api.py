from aiohttp import web
from server.api.base import SecureApi
from server.crypto.key import (
    generate_keys,
    generate_shared_key,
    generate_session_key,
    b64dec,
    b64enc,
)

import asyncio


class NotepadApi(SecureApi):
    def __init__(self, fm_cls, sm_cls):
        self.app = web.Application()
        self.__fm_cls = fm_cls
        self.__sm_cls = sm_cls

    def setup_routes(self):
        self.app.router.add_post('/ping', lambda: 'pong')
        self.app.router.add_post('/api/session', self.session)
        self.app.router.add_post('/api/echo', self.echo)

        self.app.router.add_post('/api/login', self.login)
        self.app.router.add_post('/api/register', self.register)

        self.app.router.add_post('/api/download', self.file_download)
        self.app.router.add_post('/api/update', self.file_update)
        self.app.router.add_post('/api/delete', self.file_delete)

    def setup_file_manager(self):
        self.app['fm'] = self.__fm_cls()

    def setup_session_manager(self):
        self.app['sm'] = self.__sm_cls()

    def run(self, host, port):
        self.setup_routes()
        self.setup_file_manager()
        self.setup_session_manager()
        asyncio.run(self.__run(host, port))

    async def __run(self, host, port):
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, host, port)
        await site.start()
        await asyncio.Event().wait()
    
    @SecureApi.api
    async def session(self, ctx):
        spub, spriv = generate_keys()
        cpub = b64dec(ctx.data['pubkey'])
        shared = generate_shared_key(spriv, cpub)

        session_key = generate_session_key(shared)
        session = ctx.sm.new(session_key, ctx)
        
        return {
            'sid': session.sid,
            'exp': str(session.exp),
            'pubkey': b64enc(spub),
        } 

    @SecureApi.api
    @SecureApi.with_session
    async def echo(self, ctx):
        print(ctx.data)
        return ctx.data

    @SecureApi.api
    @SecureApi.with_session
    async def login(self, ctx):
        login = ctx.data['login']
        password = ctx.data['password']
        await ctx.fm.verify_user(login, password)
        ctx.login = login
        print(ctx.login)
        return {}

    @SecureApi.api
    @SecureApi.with_session
    async def register(self, ctx):
        login = ctx.data['login']
        password = ctx.data['password']
        await ctx.fm.new_user(login, password)
        return {}

    @SecureApi.api
    @SecureApi.with_session
    @SecureApi.with_auth
    async def file_download(self, ctx):
        data = ctx.data
        content = await ctx.fm.read(
            login=ctx.login,
            filename=data['filename'],
        )
        return {'content': content}

    @SecureApi.api
    @SecureApi.with_session
    @SecureApi.with_auth
    async def file_update(self, ctx):
        data = ctx.data
        await ctx.fm.save(
            login=ctx.login,
            filename=data['filename'],
            content=data['content'],
        )
        return {}

    @SecureApi.api
    @SecureApi.with_session
    @SecureApi.with_auth
    async def file_delete(self, ctx):
        data = ctx.data
        await ctx.fm.delete(
            login=ctx.login,
            filename=data['filename'],
        )
        return {}
