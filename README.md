# icfpc2012-tbd #

## Tools ##

- python 2.7? (preferably 32-bit version)
- setuptools
- easy_install numpy
- msysgit (for windows)
- eclipse (eclipse classic is fine)
- pydev

Eclipse projects correspond to directories in repo.
But eclipse workspace itself is not in repo (that's why .metadata have to be in gitignore)

## Git ##

Generate keys (http://help.github.com/msysgit-key-setup/)

Upload public key on github account settings page

Line endings:

- Linux:   `git config --global core.autocrlf input`
- Windows:  `git config --global core.autocrlf true`

Username and email:

    git config --global user.name "Your Name"
    git config --global user.email "address you used to register on github"

Clone the repo:

    git clone git@github.com:cail/icfpc2012-tbd.git

## Git working cycle, cail's version ##

    git pull
    [hack]
    git add
    gitk (to ensure you added to index all changes you indended to add)
    git commit (or git gui for better and precise commit management)
    git pull
    [resolve conflicts if any]
    git push


Never Never Never revert your published history!
Never do `git commit --amend` if you've already push-ed the previous commit!
Never do `git rebase` on published commits

## Eclipse ##

In eclipse specify this repo directory (icfpc2012-tbd ) as workspace directory.
All preferences are stored in metadata and are therefore local.

preferences->pydev->python interpreter->auto config

file->import->existing project into workspace (test_proj)

run it (open file 'main.py' and Ctrl-F11)
