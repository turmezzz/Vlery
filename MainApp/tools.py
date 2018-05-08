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
    text = post['text']
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


def text_normalization(text):
    accepted_letters = {'a': 0, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'f': 1, 'g': 1, 'h': 1, 'i': 1, 'j': 1, 'k': 1, 'l': 1,
                        'm': 1, 'n': 1, 'o': 0, 'p': 1, 'q': 1, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 1, 'w': 1, 'x': 1,
                        'y': 1, 'z': 1, 'а': 0, 'б': 1, 'в': 1, 'г': 1, 'д': 1, 'е': 0, 'ж': 1, 'з': 1, 'и': 0, 'й': 1,
                        'к': 1, 'л': 1, 'м': 1, 'н': 1, 'о': 0, 'п': 1, 'р': 1, 'с': 1, 'т': 1, 'у': 0, 'ф': 1, 'х': 1,
                        'ц': 1, 'ч': 1, 'ш': 1, 'щ': 1, 'ъ': 1, 'ы': 0, 'ь': 1, 'э': 1, 'ю': 0, 'я': 0}

    text = text.lower()
    words = []
    for word in text.split():
        box = ''
        for i in word:
            if i in accepted_letters and accepted_letters[i] == 1:
                box += i
        words.append(box)
    return ' '.join(words)


def search(user, q):
    # первый способ поиска
    owner_id = user.username
    q = text_normalization(q)
    q_words = q.split()
    data = {}
    for word in q_words:
        posts = Post.objects.filter(owner_id__exact=owner_id, text__contains=word)
        for post in posts:
            if post not in data:
                data[post] = 0
            data[post] += 1

    box = []
    for i in data:
        box.append([data[i], i])
    box.sort(key=lambda x: x[0])
    return [i[1] for i in box]


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

    def get_posts(self):
        vk_id = self.user.username
        post_count = self.api.wall.get(owner_id=vk_id, count=1, v=5.74)['count']
        data = []
        offset = 0
        for i in range(post_count // 100):
            box = self.api.wall.get(owner_id=vk_id, offset=offset, count=100, v=5.74)['items']
            offset += 100
            data += box
        post_count %= 100
        if post_count != 0:
            box = self.api.wall.get(owner_id=vk_id, offset=offset, count=post_count, v=5.74)['items']
            data += box
        return data

    def create_new_account(self):
        data = self.get_posts()
        for i in data:
            box = get_content_from_post(i)
            box['text'] = text_normalization(box['text'])
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
        data = self.get_posts()
        for i in data:
            post_id = i['id']
            try:
                Post.objects.get(owner_id=vk_id, post_id=post_id)
            except ObjectDoesNotExist:
                box = get_content_from_post(i)
                box['text'] = text_normalization(box['text'])
                if not is_string_empty(box['text']):
                    post = Post.objects.create(owner_id=box['owner_id'],
                                               post_id=box['post_id'],
                                               text=box['text'],
                                               link=box['link'])
                    post.save()
                    self.user.posts += ' ' + str(post.id)
        self.user.save()





