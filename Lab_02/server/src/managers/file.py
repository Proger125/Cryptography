from crypto.hash import hash, decode, b64str, b64bin

import aiofiles
import os
import pathlib
import json


DEFAULT_WORK_DIR = '/tmp'


class UserAlreadyExists(Exception):
    pass


class FileAlreadyExists(Exception):
    pass


class FileNotExists(Exception):
    pass


class IncorrectPassword(Exception):
    pass


class FileManager:
    def __init__(self):
        self.work_dir = os.path.join(DEFAULT_WORK_DIR, 'deadbeef')

        if not os.path.exists(self.work_dir):
            os.makedirs(self.work_dir)

    def new_file(self, login, filename):
        path = os.path.join(self.work_dir, login, filename)
        if os.path.exists(path):
            raise FileAlreadyExists()
        pathlib.Path(path).touch()

    async def new_user(self, login, password):
        path = os.path.join(self.work_dir, login)
        if os.path.exists(path):
            raise UserAlreadyExists()
        os.makedirs(path)
        self.new_file(login, '.pass')

        password_hash, salt = hash(password)
        data = json.dumps({'p': b64str(password_hash), 's': b64str(salt)})
        await self.save(login, '.pass', data)

    async def verify_user(self, login, password):
        exp = await self.read(login, '.pass')
        exp = json.loads(exp)

        exp_password_hash, salt = decode(exp['p'], exp['s'])
        act_password_hash, _ = hash(password, salt=salt)

        if exp_password_hash != act_password_hash:
            raise IncorrectPassword()
        return True

    async def read(self, login, filename):
        path = os.path.join(self.work_dir, login, filename)
        if not os.path.exists(path):
            raise FileNotExists()
        async with aiofiles.open(path, 'r') as f:
            data = await f.read()
            return data

    async def save(self, login, filename, content):
        path = os.path.join(self.work_dir, login)
        if not os.path.exists(path):
            raise FileNotExists()
        async with aiofiles.open(os.path.join(path, filename), 'w') as f:
            await f.write(content)

    async def delete(self, login, filename):
        path = os.path.join(self.work_dir, login, filename)
        if os.path.exists(path):
            os.remove(path)
