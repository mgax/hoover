from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.conf import settings
import requests

LIQUID_URL = settings.HOOVER_OAUTH_LIQUID_URL
LIQUID_CLIENT_ID = settings.HOOVER_OAUTH_LIQUID_CLIENT_ID
LIQUID_CLIENT_SECRET = settings.HOOVER_OAUTH_LIQUID_CLIENT_SECRET

def oauth2_login(request):
    authorize_url = LIQUID_URL + '/o/authorize/'
    return redirect(
        '{}?response_type=code&client_id={}'
        .format(authorize_url, LIQUID_CLIENT_ID)
    )

def oauth2_exchange(request):
    token_url = LIQUID_URL + '/o/token/'
    redirect_uri = request.build_absolute_uri('/accounts/oauth2-exchange/')
    code = request.GET.get('code')
    token_resp = requests.post(
        token_url,
        data={
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
            'code': code,
        },
        auth=(LIQUID_CLIENT_ID, LIQUID_CLIENT_SECRET),
    )
    assert token_resp.status_code == 200
    token_data = token_resp.json()
    access_token = token_data['access_token']
    token_type = token_data['token_type']
    assert token_type == 'Bearer'
    refresh_token = token_data['refresh_token']
    profile_url = LIQUID_URL + '/accounts/profile'
    profile_resp = requests.get(
        profile_url,
        headers={'Authorization': 'Bearer {}'.format(access_token)},
    )
    assert profile_resp.status_code == 200
    profile = profile_resp.json()
    user, created = User.objects.get_or_create(username=profile['login'])
    login(request, user)

    return redirect(settings.LOGIN_REDIRECT_URL)

def oauth2_logout(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
