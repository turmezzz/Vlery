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


def text_normalization(q):
    accepted_letters = {'a': 0, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'f': 1, 'g': 1, 'h': 1, 'i': 1, 'j': 1, 'k': 1, 'l': 1,
                        'm': 1, 'n': 1, 'o': 0, 'p': 1, 'q': 1, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 1, 'w': 1, 'x': 1,
                        'y': 1, 'z': 1, 'а': 0, 'б': 1, 'в': 1, 'г': 1, 'д': 1, 'е': 0, 'ж': 1, 'з': 1, 'и': 0, 'й': 1,
                        'к': 1, 'л': 1, 'м': 1, 'н': 1, 'о': 0, 'п': 1, 'р': 1, 'с': 1, 'т': 1, 'у': 0, 'ф': 1, 'х': 1,
                        'ц': 1, 'ч': 1, 'ш': 1, 'щ': 1, 'ъ': 1, 'ы': 0, 'ь': 1, 'э': 1, 'ю': 0, 'я': 0, ' ': 0}

    q_words = q.lower().split()
    data = []
    for word in q_words:
        box = ''
        flag = False
        for i in range(len(word) - 1, -1, -1):
            if word[i] in accepted_letters:
                if accepted_letters[word[i]] == 1 or flag:
                    flag = True
                    box += word[i]
            elif len(box) > 0 and box[-1] != ' ':
                box += ' '
        if flag and box != ' ':
            box = box[::-1]
            data.append(box)
    return ' '.join(data)


def queue_normalization(q):
    q = q.lower()
    ret = q
    rus_to_eng_translit = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j',
     'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'y', 'ф': 'f',
     'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sh', 'ы': 'i', 'э': 'e', 'ю': 'u', 'я': 'ya', ' ': ' ', 'ь': '', 'ъ': ''}
    eng_to_rus_translit = {'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д', 'e': 'э', 'z': 'з', 'i': 'и', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п', 'r': 'р', 's': 'с', 't': 'т', 'y': 'у', 'f': 'ф', 'h': 'х', 'c': 'ц', 'u': 'ю', ' ': ' ', 'j': 'й'}
    rus_to_eng_keybord_loyaut = {'а': 'f', 'б': ',', 'в': 'd', 'г': 'u', 'д': 'l', 'е': 't', 'ж': ';', 'з': 'p', 'и': 'b', 'й': 'q', 'к': 'r', 'л': 'k', 'м': 'v', 'н': 'y', 'о': 'j', 'п': 'g', 'р': 'h', 'с': 'c', 'т': 'n', 'у': 'e', 'ф': 'a', 'х': '[', 'ц': 'w', 'ч': 'x', 'ш': 'i', 'щ': 'o', 'ъ': ']', 'ы': 's', 'ь': '[', 'э': '\'', 'ю': '.', 'я': 'z'}
    eng_to_rus_keybord_loyaut = {'f': 'а', 'd': 'в', 'u': 'г', 'l': 'д', 't': 'е', 'p': 'з', 'b': 'и', 'q': 'й', 'r': 'к', 'k': 'л', 'v': 'м', 'y': 'н', 'j': 'о', 'g': 'п', 'h': 'р', 'c': 'с', 'n': 'т', 'e': 'у', 'a': 'ф', 'w': 'ц', 'x': 'ч', 'i': 'ш', 'o': 'щ', 's': 'ы', 'z': 'я'}

    # раскладка с русского на английский
    box = ''
    for i in q:
        if i in rus_to_eng_keybord_loyaut:
            box += rus_to_eng_keybord_loyaut[i]
        elif i == ' ':
            box += ' '
    ret += ' ' + box

    # раскладка с английского на русский
    box = ''
    for i in q:
        if i in eng_to_rus_keybord_loyaut:
            box += eng_to_rus_keybord_loyaut[i]
        elif i == ' ':
            box += ' '
    ret += ' ' + box

    ret = text_normalization(ret)

    # транслит с русского на английский
    line = ''
    box = ''
    try:
        for word in q.split():
            box = ' '
            for i in word:
                box += rus_to_eng_translit[i]
            if box != ' ':
                line += box
    except KeyError:
        pass
    box = text_normalization(line)
    if box:
        ret += ' ' + box

    # транслит с английского на русский
    line = ''
    box = ''
    try:
        for word in q.split():
            box = ' '
            for i in word:
                box += eng_to_rus_translit[i]
            if box != ' ':
                line += box
    except KeyError:
        pass
    box = text_normalization(line)
    if box:
        ret += ' ' + box
    return ret


def search(user, q):
    # первый способ поиска
    owner_id = user.username
    # q = text_normalization(q)
    q = queue_normalization(q)
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





