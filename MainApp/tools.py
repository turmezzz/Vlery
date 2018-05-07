import vk

from .models import User, Post


class Tool:

    user = None
    api = None

    def __init__(self, request):
        self.user = request.user
        access_token = self.user.access_token
        session = vk.Session(access_token=access_token)
        self.api = vk.API(session)

    def get_img_url(self):
        vk_id = self.user.username
        ret = self.api.users.get(user_id=vk_id, v=5.74, fields='photo_50')[0]['photo_50']
        return ret

    def get_name(self):
        vk_id = self.user.username
        data = self.api.users.get(user_id=vk_id, v=5.74)
        ret = data[0]['first_name']
        return ret

    def create_new_account(self):
        vk_id = self.user.username
        data = self.api.wall.get(owner_id=vk_id, v=5.74)['items']

        for i in data:
            owner_id = str(vk_id)
            attachments = i['attachments']
            comments = i['comments']
            post_id = str(i['id'])
            text = i['text']
            link = 'http://vk.com/id' + owner_id + '?w=wall' + owner_id + '_' + post_id
            post = Post.objects.create(
                owner_id=owner_id,
                attachments=attachments,
                comments=comments,
                post_id=post_id,
                text=text,
                link=link)
            post.save()
            self.user.posts += ' ' + str(post.id)
        self.user.save()



