# git-tutorial
Refer: https://git-scm.com/docs
Refer: https://raybo.org/slides_practicalactions/#/
Refer: https://github.com/LinkedInLearning/github-practical-actions-4412872

## Install Git cli
1. Download git cli from google search
2. $ git --version (check status)

## git global config

git config --global user.name
git config --global user.name "username"

git config --global user.email
git config --global user.email "email.com"


## Git First Commit

git add .
git commit -m "First Commit"

use "git branch -M main" (to rename master branch to main)


git status
git remote
git remote -v
git restore

git restore --stage "one.txt"

git deff --staged

## File Structure
dynamic_api_creator/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── tools.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── utils.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── utils.py
│   ├── dashboard/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── forms.py
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   └── templates/
│       ├── auth/
│       │   ├── login.html
│       │   └── register.html
│       ├── dashboard/
│       │   ├── index.html
│       │   ├── create_api.html
│       │   └── edit_api.html
│       ├── layout.html
│       └── index.html
├── config.py
├── run.py
└── requirements.txt