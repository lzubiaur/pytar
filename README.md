pytar
=====

Python script to create backup tarball

Usage
=====
Create the tarball myproject\_YYMMDD.tar.gz excluding files and directories listed in the file patterns.txt

python backup.py --exclude patterns.txt myproject

Create a tarball and call GnuPG to encrypt the backup (symmetric encryption)

python backup.py --gpg myproject

Exclude
=======

To exclude a whole subtree it's recommended to use */dir_to_exclude* instead of  */dir_to_exclude/*

