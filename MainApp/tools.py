import vk


class Tool:

    def __init__(self, request):
        self.user = request.user
        access_token = self.user.username
        session = vk.Session(access_token=access_token)
        self.api = vk.API(session)

    def get_img_url(self):
        vk_id = self.user.username
        # ret = self.api.users.get(user_id=vk_id, v=5.74, fields='photo_50')[0]['photo_50']
        # return ret
        return self.user.username

    def get_name(self):
        vk_id = self.user.username
        # data = self.api.users.get(user_id=vk_id, v=5.74)
        # ret = data[0]['first_name']
        # return ret

        return self.user.access_token


