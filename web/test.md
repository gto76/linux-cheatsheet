
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
    source    <package>     # Downloads code.
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

### Install Mantra
```bash
./configure --help
./configure
make
sudo make install
```


General
-------

```bash
su  - <user>   # Switches to user.
    -          # Switches to root.
```

```bash
man <cmd>      # Help on commands.
    <section>  # Section numbers: 1. Programs, 2. System calls, 3. Library calls,
               # 4. Special files, 5. File formats, 7. Miscellaneous, 8. System 
               # administration commands
```

```bash
echo <text>    # Prints passed text.
    -n         # Does not add newline at the end.
    -e         # Enables interpretation of backslashed letters.
```

```bash
xargs <cmd>    # Passes output from one command to arguments of another:  
               # `echo -a | xargs ls`
    -t         # Echoes the command before executing it. 
    -p         # Echoes command and asks for confirmation before execution.
    -0         # Input items are separated by null character instead of space.
```

```bash
tee <file>     # Sends output of a program to specified file and to standard 
               # output: `<cmd_1> | tee out_1.txt | <cmd_2>`.
    /dev/tty   # Sends output to terminal and to standard output
```

```bash
expr <expr>    # Evaluates passed expression.
    1 + 1      # Prints `2`.
```

```bash
bc [<file>]    # Evaluates input. It's basically a calculator, but also provides some 
               # control commands.
               # `echo 1 + 1 | bc` prints `2`.
               # `echo "scale=5;3/4" | bc` prints `.75000`.
```

```bash
sh                  # Runs command interpreter (shell). Can run a script even if not executable.
    -c '<commands>' # Starts new non-interactive shell and reads commands from 
                    # arguments instead of `stdin`. To append lines to system configuration 
                    # file run: `sudo sh -c 'echo "<text>" >> <file>'`
```

```bash
bash                # Runs bash command interpreter (shell).
    -c              # Reads commands from arguments instead of `stdin`.
    -n <script>     # Checks script for errors.
    -x              # Prints commands before execution. Useful for debugging.
```

```bash
gcc <files>         # Gnu C compiler. Run `g++` for C++ code.
    -w              # Supresses warnings (Only prints errors).
    -Wall           # All warnings.
    -g              # Compile for debugging.
    -std=<std>      # Sets the standard. Suported standards for C are:  
                    # `c90`, `gnu90`, `c99`, `gnu99`, `c11` and `gnu11`.  
                    # Suported standarts for C++ are:  
                    # `c++98`, `gnu++98`, `c++11` and `gnu++11`.  
                    # `gnu90` and `gnu++98` are the default options.
    -O<level>       # Optimization level. `0`: Reduce compilation time (default),
                    # `1-3`: - Level of optimization, `s` - Optimize for size, `g` - Optimize
                    # debugging experience.
```

```bash
run-parts <dir>     # Runs all scripts or programs in a directory.
```

```bash
date                   # Tells date and time.
    -s <string>        # Sets date.
    +%T -s "10:13:13"  # Sets time.
```

```bash
timedatectl            # Controls the system time and date.
    set-timezone CET   # Sets timezone.
```

```bash
cal                    # Calendar
```

```bash
xclip                  # Copies to clipboard.
mkfifo <pipe>          # Creates named pipe during that shell session.
```

```bash
mkisofs                # Creates a DVD/CD image.
genisoimage            # Creates a DVD/CD image (Debian).
cdrecord               # Writes to a CD/DVD.
```

```bash
acpi                   # Checks battery.
```

```bash
fdisk -l (sudo)        # Shows partitions. 
```

```bash
shutdown               # Closes down the system at a given time.
    now                # Takes you to the single user mode.
    -h now             # Begins the shutdown procedure, same as `halt` and `poweroff`.
    -h 11:50           # At 11:50.
    -r now             # Same as `reboot`.
```

```bash
make                   # Utility that maintains groups of programs.
    -q                 # Doesn't run any commands, just returns `0` exit code if everything is
                       # up to date or non-zero otherwise.
    -B                 # Unconditionally makes all targets.
```


Files
-----
```bash
ls [<dir>, ...] 
    -d            # List directory names instead of contents
    -S            # Sort by size 
    -t            # Sort by time
    -1            # One file per line
    ./*           # Ls one level deep
    -i            # Get inode number of file (file id). Use `sudo find / -inum <number>` to find all 
                  # links that point to same file.
```

```bash
cp <file> <file> [..., <dir>] 
    -i            # Interactive (Prompts before overwrite)
    -v            # Verbose (Explains what is being done)
    -R            # Copy directories recursively
    -p            # Preserve mode, ownership and timestamps. `--preserve=all` also preserves
                  # context, links and xattr
```

```bash
rm <file> [...] 
    -i            # Interactive (Prompts before every removal)
    -v            # Verbose (Explains what is being done)
    -f            # Force remove (Does not prompt, useful if `rm` is aliased with `-i`)
    -R            # Removes directories and their content recursively 
```

```bash
mkdir <dir>
    -p            # Make parents if needed
```

```bash
ln <file> <link>  # Makes links to the files
    -s            # Makes symbolic link. If you want to use relative paths you must be in 
                  # links directory !!!!!!!!!!!!!!!!!!!!!!
```

```bash
df  -h            # Displays humanly readable free disk space
du  -s <dir>      # Directory size
```

```bash
mc                # Midnight commander
    Alt o         # Open parent dir in another panel
    Ctrl o        # Switch to bash
```

### Search
```bash
find <dir> 
    -name <file>              # Search by name
    -regex <regex>            # Use regex for name search
    -not                      # Insert before other options to negate
    -maxdepth <levels>        # Descend only to levels deep
    -samefile <file>          # Find all hard links of a file
    -xdev                     # Don't descend directories on other filesystems
    -inum <inum>              # Find files with the inode number
    -type <f|d|b|...>         # Find files of type
    -delete                   # Delete found files
    -exec <cmd> {} \;         # Find files and execute command for every found file. `{}` is
                              # replaced with filename
    -exec <cmd> {} +          # Find files and execute command with filenames in place of `{}`
    -atime +/-n               # Find files that were last accessed less or more than n days.
    -print0 | xargs -0 <cmd>  # Sends found files to a command as parameters. Uses `NUL` 
                              # character as separator, necessary for filenames with spaces 
```

```bash
locate <regex>                # Similar as `find` but using index. Run `sudo updatedb` to
                              # update index.
    -i                        # Ignore case
    --regex                   # Interprets all patterns as extended regex
    -0 | xargs -0 <cmd>       # Sends found files to a command as parameters.
```

### Misc
```bash
md5sum <file>         # Prints md5 sum hash of a file
read                  # Read single line from standard input 
  -n 1                # Print after reading one character
  -s                  # Do not echo input coming from terminal
shred <files>         # Securely remove files
file <file>           # Determine file's type
tree                  # Ls in a tree-like (hierarchical) format
install               # Copy files and set attributes
gpg                   # Decrypt file with password
    -c                # Encrypt
mktemp                # Create a temporary file or directory in `/tmp` and returns it's name.
rename <sed> <files>  # Renames multiple files using `sed` syntax (s/<from>/<to>)
rsync                 # A fast, versatile, remote (and local) file-copying tool
    -H                # Preserves hard links
    -b                # Renames preexisting destination files (back up)
    -a                # Preserve everything except hard links
    -z                # compresses
    cmp               # Compares two files, similar to diff but also for binaries
                      # -Hbaz -e ssh — `<src_dir> <user>@<host>:<dest_dir>` backs up the 'src-dir'.
stat <file>           # Displays file's status
    -c%X              # Time of last modification of the file 
readlink -f           # Follow link recursively and print files path
xdg-open <file>       # Open file with default application for the file type
dialog                # Display dialog box from shell script
watch <cmd>           # Execute command periodically
```
