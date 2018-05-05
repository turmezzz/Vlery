import vk


class Tool:

    api = None
    user = None

    def __int__(self, request):
        self.user = request.user
        access_token = self.user.username
        session = vk.Session(access_token=access_token)
        self.api = vk.API(session)

    def get_img_url(self):
        vk_id = self.user.vk_id
        ret = self.api.user.get(user_id=vk_id, v=5.74, fields='photo_50')[0]['photo_50']
        return ret

    def get_name(self):
        vk_id = self.user.vk_id
        data = self.api.user.get(user_id=vk_id, v=5.74)
        ret = data[0]['first_name']
        return ret


