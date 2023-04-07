from utils import unwrap_json, wrap_json, decrypt, encrypt


class APIError(Exception):
    pass


class ApiRequests:
    def __init__(self, session, url):
        self.session = session
        self.url = url
        self.session_key = None
        self.session_id = None

    def set_session_key(self, session_key):
        self.session_key = session_key

    def set_session_id(self, session_id):
        self.session_id = session_id

    async def api_request(self, method, data):
        async with self.session.post(f"{self.url}/{method}", json=data) as resp:
            print(f'{self.url}/{method} response => {resp}')
            rj = await resp.json()
            if rj['status'] == 'ok':
                return rj['result']
            else:
                raise APIError(rj['result'])

    async def api_request_sw(self, method, data):
        return unwrap_json(await self.api_request(method, wrap_json(data, self.session_key, self.session_id)),
                           self.session_key, self.session_id)

    async def test_session(self, key):
        echo_data = {'content': encrypt('some secret content', key)}
        recv_data = await self.api_request_sw('echo', echo_data)

        print(f'content_encrypted : {echo_data} => {recv_data}')
        recv_data['content'] = decrypt(recv_data['content'], key)
        print(f'content_decrypted : {echo_data} => {recv_data}')

    async def login(self):
        login = input("Enter login: ")
        password = input("Enter password: ")
        login_data = {"login": login, "password": password}
        recv_data = await self.api_request_sw("login", login_data)
        print(recv_data)

    async def register(self):
        login = input("Enter login: ")
        password = input("Enter password: ")
        login_data = {"login": login, "password": password}
        recv_data = await self.api_request_sw("register", login_data)
        print(recv_data)

    async def get_file(self, key):
        filename = input("Enter filename: ")
        data = {"filename": filename}
        recv_data = await self.api_request_sw("download", data)
        content = recv_data["content"]
        if key is not None:
            content = decrypt(content, key)
        print(content)

    async def put_file(self, key):
        filename = input("Enter filename: ")
        content = input("Enter contents: ")
        if key is not None:
            content = encrypt(content, key)
        data = {"filename": filename, "content": content}
        recv_data = await self.api_request_sw("update", data)
        print(recv_data)

    async def delete_file(self):
        filename = input("Enter filename: ")
        data = {"filename": filename}
        recv_data = await self.api_request_sw("delete", data)
        print(recv_data)
