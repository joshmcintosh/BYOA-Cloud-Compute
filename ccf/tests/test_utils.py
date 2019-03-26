from django.contrib.auth.models import User


def create_user(username, password):
    test_user = User.objects.create_user(username, password)
    test_user.save()
    return test_user
