
Awesome Terminal Commands
=========================

Packages
--------

### Dpkg
```bash
dpkg                        # Low level package manager for Debian.
    -l                      # Lists installed packages.
    -i <package> (sudo)     # Installs package from a package file.
```

### Apt
```bash
apt-get                     # Advanced Package Tool built on top of 'dpkg'. New command called
                            # simply 'apt' is also available. It merges the functionalities of
                            # 'apt-get' and 'apt-cache'.
    update                  # Updates local list of existing packages.
    -u dist-upgrade         # Upgrades by intelligently handling changing dependencies with new
                            # versions of packages. To regularly update put this line in 
                            # 'crontab': 'apt-get update && apt-get -u dist-upgrade'.
    upgrade                 # Same as dist-upgrade, but will not remove installed packages or 
                            # install new ones.
    install   <package>     # Also updates single package.
    remove    <package>     # Removes package but leaves its configurations.
    remove apt-listchanges  # Useful when Debian can't find a package.
    purge     <package>     # Removes package and its configurations. Run 'apt-get autoremove'
                            # after to remove all dependencies that are not needed anymore.
    autoremove              # Removes unneeded packages.
    source    <package>      # Downloads code.
    build-dep <package>     # Installs the build dependencies.
    --yes                   # Answers with 'yes' to most questions (Except the ones that can
                            # have potentially harmful consequences).
    --force-yes             # Answers 'yes' to all questions (Not recommended).
```

```bash
apt-cache                   # Queries the APT's internal database.
    search  <keyword>       # Searches packages like 'apropos', but globally.
    show    <package>       # Shows package info like version, dependencies, etc.
    showpkg <package>       # Similar, but also shows the packages that depend on the searched
                            # package (reverse dependencies).
    policy  <package>       # Shows installed and remote version.
```

```bash
apt-file                    # APT package searching utility.
    search <file>           # Search in which package a file is included.
    update                  # Updates local list of package contents.
```

```bash
aptitude                    # Enables package browsing (skin for apt-get).
    search '~i!~M'          # Lists installed packages that were not installed as a dependency,
                            # with short description of each.
    search <package>        # Package search.
```

### Misc
```bash
winetricks                  # Installs wine applications.
update-alternatives         # Maintains symbolic links determining default commands.
unattended-upgrade          # Automatic installation of security upgrades.
```

### Commands
```bash
apropos <cmd>               # Searches the manual page names and descriptions (use quotes for 
                            # phrases).
    -a                      # Matches all keywords.
whatis  <cmd>               # Displays one-line manual page description.
whereis <cmd>               # Locates the binary, source, and manual page files for a command.
which   <cmd>               # Locates only the binary of a command.
wtf                         # Translates acronyms and filename suffixes.
```

