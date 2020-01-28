from .models import *
from accounts.models import *
from accounts.views import get_followers, get_followings
from .serializer import CardSerializer, NewsSerializer, LaterSerializer
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views import View
from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Count
from .scripts import imgur_upload, search_images
from django.utils import timezone
from datetime import timedelta
from random import randint, shuffle
import json


class ServiceWorkerView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'static/service-worker.js', content_type="application/x-javascript")


class CardPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    last_page_strings = 'last'
    many = True


class FiltersApi(GenericViewSet):
    queryset = Card.objects.all()
    many = True
    filters = {
        # param name: model, value1, value2, order_by
        'tags': [Tag, 'name', 'id', 'name'],
    }

    def list(self, request, *args, **kwargs):
        try:
            filters = self.filters
            params = request.GET
            page_id = params['page_id']
            user = Account.objects.get(page_address=page_id).user
            if params['type_id'] not in ['all']:
                type_id = int(params['type_id'])
                types = []
                for card_type in Type.objects.filter(owner=user):
                    cards = Card.objects.filter(type=card_type)
                    card_count = cards.count()
                    if card_type.picture in [None, '']:
                        for card in cards:
                            if card.imgur_url:
                                picture = card.imgur_url
                                card_type.picture = picture
                                card_type.save()
                                break
                            picture = None
                    else:
                        picture = card_type.picture
                    types.append({
                        'name': card_type.name,
                        'id': card_type.id,
                        'picture': picture,
                        'color': card_type.color,
                        'card_count': card_count
                    })
                if type_id == 0:
                    type_obj = Type.objects.filter(owner=user)[0]
                else:
                    type_obj = Type.objects.filter(id=type_id)
                    type_obj = type_obj[0] if type_obj.count() > 0 else Type.objects.filter(owner=user)[0]
                    type_obj = type_obj if type_obj.owner == user else Type.objects.filter(owner=user)[0]
                response = {
                    i:  [{filters[i][1]: j[filters[i][1]], filters[i][2]: j[filters[i][2]]}
                         for j in filters[i][0].objects.filter(type=type_obj).order_by(filters[i][3]).values()]
                    for i in filters
                }
                response['types'] = types
            else:
                response = {
                    i: [{filters[i][1]: j[filters[i][1]], filters[i][2]: j[filters[i][2]]}
                        for j in filters[i][0].objects.filter(owner=request.user).distinct('name')
                            .order_by(filters[i][3]).values()]
                    for i in filters
                }
                type_obj = None

                response['types'] = [{'name': card_type.name, 'id': card_type.id}
                         for card_type in Type.objects.filter(owner=request.user)]

            response['rates'] = [{'name': i['name'], 'rate': i['rate']} for i in Rating.objects.all().values()]
            response['type'] = type_obj.id if type_obj else None
        except Exception:
            response = {
                'types': [],
                'tags': [],
                'type': None,
                'rates': [{'name': i['name'], 'rate': i['rate']} for i in Rating.objects.all().values()]
            }
        return JsonResponse(response)


class CardsApi(GenericViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    pagination_class = CardPagination
    many = True
    filters = {
        'rating': 'rating__rate__in',
        'tags': 'tags__id__in',
    }

    def list(self, request, *args, **kwargs):
        params = request.GET
        if 'page_id' in params:
            page_id = params['page_id']
            user = Account.objects.get(page_address=page_id).user
            if 'type_id' not in params:
                return JsonResponse({'status': 'No Cards'})
            elif params['type_id'] == 'null':
                return JsonResponse({'status': 'No Cards'})
            type_id = int(params['type_id'])
            if type_id == 0:
                try:
                    type_obj = Type.objects.filter(owner=user)[0]
                except IndexError:
                    return JsonResponse({'status': 'No Cards'})
            else:
                type_obj = Type.objects.get(id=type_id)

            qs = self.queryset.filter(owner=user).filter(type=type_obj)
            for filter in self.filters:
                if filter in params:
                    values = params.get(filter).split(',')
                    qs = qs.filter(**{
                        self.filters[filter]: values
                    }) if len(values) > 0 and values[0] not in ['null', ''] else qs
            qs = qs.distinct()
            page = self.paginate_queryset(qs)
        elif 'card_id' in params:
            card_id = params['card_id']
            qs = self.queryset.filter(id=card_id)
            page = None
        if page is not None:
            serializer = self.get_serializer(page, many=self.many)
            data = serializer.data
            return self.get_paginated_response(data)
        serializer = self.get_serializer(qs, many=self.many)
        return Response(serializer.data)


def later_filters(request, *args, **kwargs):
    user = request.user
    cards = PostCard.objects.filter(owner=user)
    types = [i[0] for i in cards.order_by('type').distinct('type').values_list('type')]
    all_tags = (json.loads(i[0]) for i in cards.values_list('tags'))
    tags = []
    for tag_list in all_tags:
        for tag in tag_list:
            tags.append(tag)
    tags = list(set(tags))
    return JsonResponse({
        'types': types,
        'tags': tags
    })


class LaterApi(GenericViewSet):
    queryset = PostCard.objects.all()
    serializer_class = LaterSerializer
    pagination_class = CardPagination
    many = True

    def list(self, request, *args, **kwargs):
        user = request.user
        params = request.GET
        qs = PostCard.objects.filter(owner=user)
        if 'type' in params:
            types = params.get('type').split(',')
            if len(types) > 0 and types[0] != '':
                qs = qs.filter(type__in=types)
        if 'tags' in params:
            tags_filter = params.get('tags').split(',')
            if len(tags_filter) > 0 and tags_filter[0] != '':
                cards = []
                for card in qs:
                    card_tags = json.loads(card.tags)
                    if set(tags_filter) & set(card_tags):
                        cards.append(card.id)
                qs = PostCard.objects.filter(id__in=cards)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=self.many)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=self.many)
        return Response(serializer.data)


class NewsApi(GenericViewSet):
    queryset = Card.objects.all()
    serializer_class = NewsSerializer
    pagination_class = CardPagination
    many = True

    def list(self, request, *args, **kwargs):
        user = request.user
        followings = Following.objects.get(user=user).follow.all()
        month = timezone.now() - timedelta(weeks=4)
        qs = Card.objects.filter(timestamp__gte=month).filter(owner__in=followings)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=self.many)
            data = serializer.data
            return self.get_paginated_response(data)
        serializer = self.get_serializer(qs, many=self.many)
        return Response(serializer.data)


@login_required
def create_card(request, *args, **kwargs):
    params = json.loads(request.body)
    owner = request.user
    title = params['title']
    type = params['type']
    tags = params['tags']
    from_post_storage = params['from_post_storage']
    post_storage = params['post_storage']

    picture_url = params['img_url']
    if Card.objects.filter(imgur_url=picture_url).count() > 0 \
            or PostCard.objects.filter(imgur_url=picture_url).count() > 0:
        imgur_url = picture_url
    else:
        imgur_url = imgur_upload(picture_url) if picture_url else None

    if post_storage:
        post_card = PostCard(
            title=title,
            imgur_url=imgur_url,
            type=type['name'] if isinstance(type, dict) else type,
            tags=json.dumps([tag['name'] if isinstance(tag, dict) else tag for tag in tags]) if tags else None,
            owner=owner,
            timestamp=timezone.now()
        )
        post_card.save()
    else:
        rate = int(params['rating'])
        rate_obj = Rating.objects.get(rate=rate)
        type_obj = get_type_object(type, owner)
        tag_ids = []
        if tags:
            for tag in tags:
                tag_obj = get_tag_object(tag, type_obj, owner)
                tag_ids.append(tag_obj.id)

        new = False
        card_id = params['id']
        if from_post_storage:
            PostCard.objects.get(id=card_id).delete()
            new = True
        elif card_id:
            card = Card.objects.get(id=card_id)
            if card.owner == owner:
                card.title = title
                card.imgur_url = imgur_url
                card.type = type_obj
                card.rating = rate_obj
                card.tags.clear()
            else:
                new = True
        else:
            new = True
        if new:
            card = Card(
                title=title,
                picture=None,
                imgur_url=imgur_url,
                type=type_obj,
                rating=rate_obj,
                owner=owner,
                timestamp=timezone.now()
            )
        card.save()
        if params['cover']:
            type_obj.picture = imgur_url
            type_obj.save()
        if len(tag_ids) > 0:
            card.tags.add(*tag_ids)
        delete_odd(owner)
    return JsonResponse({'status': 'Success'})


@login_required
def delete_card(request, *args, **kwargs):
    params = json.loads(request.body)
    owner = request.user
    id = params['id']
    post_storage = params['post_storage']
    if post_storage:
        card = PostCard.objects.get(id=id)
    else:
        card = Card.objects.get(id=id)
    if card.owner == owner:
        card.delete()
        delete_odd(owner)
        return JsonResponse({'status': 'Success'})


@login_required
def group_edit(request, *args, **kwargs):
    params = json.loads(request.body)
    user = request.user
    id = params['id']
    name = params['name']
    type = Type.objects.get(id=id)
    if type.owner == user:
        existing_type = Type.objects.filter(owner=user).filter(name=name)
        if existing_type.count() == 0:
            type.name = name
            type.save()
        else:
            Card.objects.filter(type=type).update(type=existing_type[0])
            Tag.objects.filter(type=type).update(type=existing_type[0])
            delete_odd(user)
        return JsonResponse({'status': 'Success'})
    else:
        return HttpResponseBadRequest


@login_required
def get_images(request, *args, **kwargs):
    params = request.GET
    title = params['title']
    page = int(params['page'])
    existing = [i[0] for i in
                Card.objects.filter(title=title).exclude(imgur_url=None) \
                   .order_by('imgur_url').distinct('imgur_url').values_list('imgur_url')[:5]]
    count = 6 - len(existing)
    result = existing + search_images(title, count, page) if page == 1 else search_images(title, count, page)
    return JsonResponse({'images': result})


allowed_users = User.objects.all() # filter(id__in=[1, 7])
random_cards = [i[0] for i in Card.objects.filter(owner__in=allowed_users)\
    .order_by('title').distinct('title').values_list('id')]
shuffle(random_cards)


def random_card(request, *args, **kwargs):
    global random_cards
    card = Card.objects.get(id=random_cards.pop(randint(0, len(random_cards) - 1)))
    if len(random_cards) == 0:
        random_cards = [i[0] for i in Card.objects.filter(owner__in=allowed_users).values_list('id')]
        shuffle(random_cards)
    owner = card.owner
    owner_acc = Account.objects.get(user=owner)
    owner_info = {
        'username': owner.first_name,
        'avatar': owner_acc.avatar,
        'page_id': owner_acc.page_address,
        'id': owner.id
    }
    return JsonResponse({'info': NewsSerializer(card).data, 'owner': owner_info})


def get_random_users():
    global random_user_list
    random_user_list = []
    all_users = User.objects.all()
    for u in all_users:
        if Card.objects.filter(owner=u).count() > 5:
            random_user_list.append(u.id)
    shuffle(random_user_list)


get_random_users()
# for card in Card.objects.all(): card.save()


def random_collections(request, *args, **kwargs):
    global random_user_list
    users = [User.objects.get(id=random_user_list.pop(randint(0, len(random_user_list) - 1))) for i in range(3)]
    if len(random_user_list) < 3:
        get_random_users()
    collections = []
    for user in users:
        acc = Account.objects.get(user=user)
        avatar = acc.avatar
        page_id = acc.page_address
        username = acc.user.first_name
        card_count = Card.objects.filter(owner=user).count()
        collections.append({
            'avatar': avatar,
            'page_id': page_id,
            'username': username,
            'cardCount': card_count,
            'follow': 0,
            'followers': get_followers(user, None),
            'followings': get_followings(user)
        })
    return JsonResponse({'collections': collections})


def delete_odd(user):

    def delete_odd_model(model, user):
        objects = model.objects.filter(owner=user).annotate(card_count=Count('card'))
        for obj in objects:
            if obj.card_count == 0:
                obj.delete()

    delete_odd_model(Tag, user)
    delete_odd_model(Type, user)


def get_type_object(type, owner):
    if isinstance(type, dict):
        type_obj = Type.objects.get(id=int(type['id']))
        if type_obj.owner != owner:
            exist = Type.objects.filter(owner=owner).filter(name__iexact=type['name'])
            if exist.count() > 0:
                type_obj = exist[0]
            else:
                type_obj = Type(name=type['name'], owner=owner)
                type_obj.save()
    else:
        exist = Type.objects.filter(owner=owner).filter(name__iexact=type)
        if exist.count() > 0:
            type_obj = exist[0]
        else:
            type_obj = Type(name=type, owner=owner)
            type_obj.save()
    return type_obj


# param = params['author']
# type_obj = type_obj
# owner = request.user
def get_tag_object(param, type_obj, owner):
    if isinstance(param, dict):
        param_obj = Tag.objects.get(id=int(param['id']))
        if param_obj.type != type_obj:
            exist = Tag.objects.filter(type=type_obj).filter(name__iexact=param['name'])
            if exist.count() > 0:
                param_obj = exist[0]
            else:
                param_obj = Tag(name=param['name'], type=type_obj, owner=owner)
                param_obj.save()
    elif param:
        exist = Tag.objects.filter(type=type_obj).filter(name__iexact=param)
        if exist.count() > 0:
            param_obj = exist[0]
        else:
            param_obj = Tag(name=param, type=type_obj, owner=owner)
            param_obj.save()
    else:
        param_obj = None
    return param_obj
