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

### Create feature/developer_one branch


#### **Task 1: As a contributor 1, perform following steps:**
**Contributor: developer_one**

Assume a developer 'one' created the feature branch to work on a feature assigned to him.
Good practice to name a feature branch to prefix it with ticket number. If a story number is ST003,
then you can add a feature branch named like 'feature/st003_login_otp'.

In this we named as developer_one to track changes done by multiple developer in a repo. Just for learning :)

```bash
git checkout -b feature/developer_one
git branch
```

Add a folder, and few files in the repo.

```bash
mkdir developer_one
cd developer_one
touch first.py
```
Add few lines of code to first.py. Run below command to check status and commit the changes from local to origin.

```bash
git status
```

```bash
git add developer_one/
```
This will add developer_one and all files fromworking directory to the staging area. It prepare files for commit.

```bash
git commit -m "Added developer_one commit"
```
The git commit command takes everything from the staging area and creates a permanent snapshot (commit) in your Git repository's history. It's like taking a photo of your project at that exact moment.

For first time push into new beranch use below command:
```bash
git push --set-upstream origin feature/developer_one
```

For regular update, after first push use below command:

```bash
git push --set-upstream origin feature/developer_one
```

The git push command uploads your local commits from your local repository to a remote repository (like GitHub, GitLab, etc.). It's how you share your work with others and back up your commits to the cloud.

Good, now we successfully added developer_one codes to feature/developer_one branch in origin.

**Task 2: Merge feature/developer_one to develop branch**
=======
Run below command
```bash
git checkout develop
```

Now, you will notice the directory, files and changes made in developer_one feature branch is not available in your IDE.

Run below command to merge code from feature branch to origin develop
```bash
git merge develop
```

**Task 3: Add new file developer_one feature branch**


Add new file second.py
Enter few lines of codes in second.py

```bash
git status
git add developer_one/second.py
git commit -m "added second.py"
git push
```

Now checkout develop branch, and create a new feature branch developer_test

```bash
git status
git checkout develop
git checkout -b feature/developer_test
```
make necessary changes

```bash
git stash push -m "aded new file"
git checkout develop
git pull origin develop
git rebase develop
git stash pop
```

**Task 4: As a contributor 'two' clone the branch and create feature branch developer_two**

```bash
git checkout -b feature/developer_two
git pull origin develop
```