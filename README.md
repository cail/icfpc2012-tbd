icfpc2012-tbd
=============

icfpc2012-tbd



=== Tools ===

python 2.7? (preferably 32-bit version)
setuptools
easy_install numpy
msysgit (for windows)
eclipse
pydev (specify preferences->pydev->python interpreter)

--
Eclipse projects correspond to directories in repo.
But eclipse workspace itself is not in repo (that's why .metadata have to be in gitignore)


=== Git ===

Generate keys (http://help.github.com/msysgit-key-setup/)
Upload public key on github account settings page

Line endings:
  for linux    git config --global core.autocrlf input
  for windows  git config --global core.autocrlf true

git config --global user.name "Your Name"
git config --global user.email "address you used to register on github"

git clone git@github.com:cail/icfpc2011-tbd.git


== Git working cycle, cail's version ==

git pull
[hack]
git add
gitk (to ensure you added to index all changes you indended to add)
git commit (or git gui for better and precise commit management)
git pull
[resolve conflicts if any]
git push


== Never Never Never revert your published history!
Never do 'git commit --amend' if you've already push-ed the previous commit!
Never do 'git rebase' on published commits
