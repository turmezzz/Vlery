import vk

from .models import User, Post
from django.core.exceptions import ObjectDoesNotExist


def is_string_empty(s):
    if s is None or len(s) == 0 or len(s.split()) == 0:
        return True
    else:
        return False


def get_content_from_post(post):
    if type(post) == list:
        post = post[0]
    owner_id = str(post['owner_id'])
    text = post['text'].lower()
    post_id = str(post['id'])
    link = 'http://vk.com/id' + owner_id + '?w=wall' + owner_id + '_' + post_id
    if 'copy_history' in post:
        box = get_content_from_post(post['copy_history'])
        if (box is not None) and (not is_string_empty(box['text'])):
            text += ' ' + box['text']
    ret = {'owner_id': owner_id,
           'post_id': post_id,
           'link': link,
           'text': text}
    return ret


def get_posts(user, api):
    vk_id = user.username
    post_count = api.wall.get(owner_id=vk_id, count=1, v=5.74)['count']
    data = []
    offset = 0
    for i in range(post_count // 100):
        box = api.wall.get(owner_id=vk_id, offset=offset, count=100, v=5.74)['items']
        offset += 100
        data += box
    post_count %= 100
    if post_count != 0:
        box = api.wall.get(owner_id=vk_id, offset=offset, count=post_count, v=5.74)['items']
        data += box
    return data


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
        # data = self.api.wall.get(owner_id=vk_id, v=5.74)['items']
        data = get_posts(self.user, self.api)
        for i in data:
            box = get_content_from_post(i)
            if not is_string_empty(box['text']):
                post = Post.objects.create(
                    owner_id=box['owner_id'],
                    post_id=box['post_id'],
                    text=box['text'],
                    link=box['link'])
                post.save()
                self.user.posts += ' ' + str(post.id)
        self.user.save()

    def update_posts(self):
        vk_id = self.user.username
        # data = self.api.wall.get(owner_id=vk_id, v=5.74)['items']
        data = get_posts(self.user, self.api)
        for i in data:
            post_id = i['id']
            try:
                Post.objects.get(owner_id=vk_id, post_id=post_id)
            except ObjectDoesNotExist:
                box = get_content_from_post(i)
                post = Post.objects.create(owner_id=box['owner_id'],
                                           post_id=box['post_id'],
                                           text=box['text'],
                                           link=box['link'])
                post.save()
                self.user.posts += ' ' + str(post.id)
        self.user.save()





