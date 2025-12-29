import os
from django.conf import settings

APNAGIT_DIR = os.path.join(settings.BASE_DIR, ".apnaGit")

def init_apnagit():
    repos_path = os.path.join(APNAGIT_DIR, "repos")

    if not os.path.exists(APNAGIT_DIR):
        os.mkdir(APNAGIT_DIR)

    if not os.path.exists(repos_path):
        os.mkdir(repos_path)
