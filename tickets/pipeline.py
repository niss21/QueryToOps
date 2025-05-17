def save_profile(backend, user, response, *args, **kwargs):
    name = response.get('name') or response.get('given_name') or ''
    if name and user.name != name:
        user.name = name
        user.save()