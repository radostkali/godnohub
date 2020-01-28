from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from collection.scripts import imgur_upload
from collection.models import Card
from .models import *
import json


# Pages user follows
def get_followings(user):
    followings_users = Following.objects.get(user=user).follow.all()
    followings = []
    for u in followings_users:
        acc = Account.objects.get(user=u)
        followings.append({
            'username': u.first_name,
            'avatar': acc.avatar,
            'page_id': acc.page_address,
            'id': u.id,
            'followed': True,
            'follower_count': Following.objects.filter(follow=u).count(),
            'timestamp': Card.objects.filter(owner=u).latest('timestamp').timestamp
        })
        followings.sort(key=lambda item: item['timestamp'], reverse=True)
    return followings


# User followers
def get_followers(user, requester):
    requester_followings = Following.objects.get(user=requester).follow.all() if requester else []
    user_followers = Following.objects.filter(follow=user)
    if user_followers.count() > 0:
        followers = []
        for u in user_followers:
            acc = Account.objects.get(user=u.user)
            followers.append({
                'username': u.user.first_name,
                'avatar': acc.avatar,
                'page_id': acc.page_address,
                'id': u.id,
                'followed': u.user in requester_followings,
                'follower_count': Following.objects.filter(follow=u.user).count()
            })
    else:
        followers = None
    return followers


@csrf_exempt
def create_account(request, *args, **kwargs):
    params = json.loads(request.body)
    email = params['email']
    password = params['password']
    name = params['name']
    if email == '' or password == '' or len(email) > 40 or len(password) > 33 or len(name) > 13:
        return JsonResponse({'status': 'Wrong data'})
    if User.objects.filter(username=email).count() > 0:
        return JsonResponse({'status': 'User already exists'})
    new_user = User.objects.create_user(
        username=email,
        password=password,
        first_name=name
    )
    new_user.save()
    new_account = Account(
        user=new_user,
        last_news_check=timezone.now()
    )
    new_account.save()
    new_following = Following(
        user=new_user
    )
    new_following.save()
    login(request, new_user)
    return JsonResponse({'status': 'Success'})


@csrf_exempt
def login_account(request, *args, **kwargs):
    params = json.loads(request.body)
    username = params['username']
    password = params['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'status': 'Success'})
    else:
        return HttpResponseBadRequest


@login_required
#@csrf_exempt
def logout_account(request, *args, **kwargs):
    logout(request)
    return JsonResponse({'status': 'Success'})


@login_required
def get_info(request, *args, **kwargs):
    user = request.user
    if 'get_followings' in request.GET:
        return JsonResponse({'followings': get_followings(request.user)})
    acc = Account.objects.get(user=user)
    page_id = acc.page_address
    avatar = acc.avatar
    username = user.first_name
    return JsonResponse({'page_id': page_id, 'username': username, 'avatar': avatar})


@login_required
def load_avatar(request, *args, **kwargs):
    user = request.user
    if request.method == 'POST':
        data = json.loads(request.body)
        image_url = data['image_url']
        imgur_url = imgur_upload(image_url)
        if imgur_url:
            acc = Account.objects.get(user=user)
            acc.avatar = imgur_url
            acc.save()
            return JsonResponse({'avatar_url': imgur_url})
        else:
            return JsonResponse({'avatar_url': 'error'})
    elif request.method == 'PUT':
        data = request.body
        imgur_url = imgur_upload(file=data)
        if imgur_url:
            acc = Account.objects.get(user=user)
            acc.avatar = imgur_url
            acc.save()
            return JsonResponse({'avatar_url': imgur_url})
        else:
            return JsonResponse({'avatar_url': 'error'})


@login_required
def change_nickname(request, *args, **kwargs):
    try:
        nickname = json.loads(request.body)['nickname']
        user = request.user
        user.first_name = nickname
        user.save()
        return JsonResponse({'status': 'Success'})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'Error'})


@login_required
def change_page_id(request, *args, **kwargs):
    try:
        page_id = json.loads(request.body)['page_id']
        if page_id not in ['news', 'later', 'settings']:
            user = request.user
            acc = Account.objects.get(user=user)
            acc.page_address = page_id
            acc.save()
            return JsonResponse({'status': 'Success'})
        else:
            return JsonResponse({'status': 'Error'})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'Error'})


def owner_info(request, *args, **kwargs):
    params = request.GET
    page_id = params['page_id']
    acc = Account.objects.get(page_address=page_id)
    avatar = acc.avatar
    username = acc.user.first_name
    card_count = Card.objects.filter(owner=acc.user).count()
    user_to_follow = acc.user

    if request.user.is_authenticated:
        user = request.user
        # followings of requester
        user_followings = Following.objects.get(user=user).follow.all()
        if user_to_follow in user_followings:
            followed = 1
        else:
            followed = 0
    else:
        followed = 0
        user = None
    return JsonResponse({
        'avatar': avatar,
        'username': username,
        'card_count': card_count,
        'follow': followed,
        'followers': get_followers(user_to_follow, user),
        'followings': get_followings(user_to_follow)
    })


@login_required
def follow(request, *args, **kwargs):
    params = json.loads(request.body)
    user = request.user
    command = params['command']
    page_id = params['page_id']
    user_to_follow = Account.objects.get(page_address=page_id).user
    user_followings = Following.objects.get(user=user)
    if user_to_follow in user_followings.follow.all():
        if command == 'unfollow':
            user_followings.follow.remove(user_to_follow)
            return JsonResponse({'follow': 0})
    else:
        if command == 'follow':
            user_followings.follow.add(user_to_follow)
            return JsonResponse({'follow': 1})
    return HttpResponseBadRequest


@login_required
def news_info(request, *args, **kwargs):
    params = request.GET
    acc = Account.objects.get(user=request.user)
    last_check = acc.last_news_check
    if 'news_count' in params:
        all_news_count = 0
        followings = get_followings(request.user)
        for i in range(len(followings)):
            all_news_count += Card.objects.filter(owner=User.objects.get(id=followings[i]['id'])) \
                .filter(timestamp__gte=last_check).count()
        return JsonResponse({'news_count': all_news_count})
    else:
        followings = get_followings(request.user)
        for i in range(len(followings)):
            news_count = Card.objects.filter(owner=User.objects.get(id=followings[i]['id'])) \
                .filter(timestamp__gte=last_check).count()
            followings[i]['news_count'] = news_count
        acc.last_news_check = timezone.now()
        acc.save()
        return JsonResponse({'last_check': last_check.strftime('%Y-%m-%dT%H:%M:%S'), 'followings': followings})

