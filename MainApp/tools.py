import vk

from .models import User, Post


def get_content_from_post(post):
    if type(post) == list:
        post = post[0]
    owner_id = str(post['owner_id'])
    text = post['text'].lower()
    post_id = str(post['id'])
    link = 'http://vk.com/id' + owner_id + '?w=wall' + owner_id + '_' + post_id
    if 'copy_history' in post:
        box = get_content_from_post(post['copy_history'])
        if box is not None:
            text += box['text']
    ret = {'owner_id': owner_id,
           'post_id': post_id,
           'link': link,
           'text': text}
    return ret


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
            box = get_content_from_post(i)
            post = Post.objects.create(
                owner_id=box['owner_id'],
                # attachments=box['attachments'],
                # comments=comments,
                post_id=box['post_id'],
                text=box['text'],
                link=box['link'])
                # link='')
            post.save()
            self.user.posts += ' ' + str(post.id)
        self.user.save()



