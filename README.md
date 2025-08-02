# Basic Configuration
Refer: https://git-scm.com/docs

## Install Git cli
1. Download git cli from google search
2. $ git --version (check status)

## git global config
```bash
git config --global user.name
git config --global user.name "username"

git config --global user.email
git config --global user.email "email.com"
```

## Know the difference Clone vs Fork

'git clone' and 'fork' are often confused, but they serve different purposes in collaborative development.

Let me break this down:
### git clone
```bash
git clone https://github.com/mahadevanvaradhan/git-tutorial.git
cd git-tutorial
```

The above command create a local copy in your machine.

Clone is used when you want to create your own repository or when you want to contribute to existing repository as a team member.

### Fork
'Fork' is the button (feature) available in github, gitlab, bitbuket. When you click on the buttun it creates your own copy of someone's repository in your account.

For is used when you want to customize someone projects to meet your requirements.

# 2. Practical

### Create develop branch

```bash
git checkout -b develop
git branch
```


Run below command
```bash
git checkout develop
```

Now, you will notice the directory, files and changes made in developer_one feature branch is not available in your IDE.

Run below command to merge code from feature branch to develop
```bash
git merge develop
```