# MinimalLinux - Minimal Linux filesystem

## Dependencies

### For building

- A C runtime, compiler, linker, etc.
  - Mandatory.
  - Either the platform's native 'cc', or GCC 4.2 or newer.
  - GCC Homepage:
    <https://gcc.gnu.org>
  - Download:
    <https://ftp.gnu.org/gnu/gcc>

- A shell
  - Mandatory.
  - Either the platform's native 'sh', or Bash.
  - Homepage:
    <https://www.gnu.org/software/bash>
  - Download:
    <https://ftp.gnu.org/gnu/bash>

- Awk
  - Mandatory.
    Either the platform's native awk, mawk, or nawk, or GNU awk.
  - Homepage:
    <https://www.gnu.org/software/gawk>
  - Download:
    <https://ftp.gnu.org/gnu/gawk>

- Core POSIX utilities, including:

    ```text
    [ cat cut chmod chown cp dd echo ln ls mkdir mknod mv pwd rm tr
    ```

  - Mandatory.
  - Either the platform's native utilities, or GNU coreutils.
  - Homepage:
    <https://www.gnu.org/software/coreutils>
  - Download:
    <https://ftp.gnu.org/gnu/coreutils>

- GNU Grub
  - Mandatory.
  - GNU Grub 2.x
  - Homepage:
    <https://www.gnu.org/software/grub>
  - Download:
    <https://ftp.gnu.org/gnu/grub>

- GNU Make
  - Mandatory.
  - GNU Make 3.79.1 or newer.
  - GNU Make Homepage:
    <https://www.gnu.org/software/make>
  - Download:
    <https://ftp.gnu.org/gnu/make>

- Grep
  - Mandatory.
  - Either the platform's native grep, or GNU grep.
  - Homepage:
    <https://www.gnu.org/software/grep>
  - Download:
    <https://ftp.gnu.org/gnu/grep>

- Kpartx
  - Mandatory.
  - Homepage:
    <http://christophe.varoqui.free.fr>

- QEMU Utils
  - Mandatory.
  - For creating disk image.
  - Homepage:
    <https://www.qemu.org>
  - Download:
    <https://www.qemu.org/download>

- Sed
  - Mandatory.
  - Either the platform's native sed, or GNU sed.
  - Homepage:
    <https://www.gnu.org/software/sed>
  - Download:
    <https://ftp.gnu.org/gnu/sed>

- Sudo
  - Mandatory.
  - Homepage:
    <https://www.sudo.ws>
  - Download:
    <https://www.sudo.ws/dist>

- Util-linux
  - Mandatory.
  - Homepage:
    <https://github.com/util-linux/util-linux>
  - Download:
    <https://github.com/util-linux/util-linux/tags>

- Wget
  - Mandatory.
  - Either the platform's native 'wget', or GNU Wget.
  - GNU Wget Homepage:
    <https://www.gnu.org/software/wget>
  - Download:
    <https://ftp.gnu.org/gnu/wget>

### For testing

- Tree
  - Mandatory.
  - For `make check` command.
  - Homepage:
    <http://oldmanprogrammer.net/source.php?dir=projects/tree>

- QEMU System
  - Mandatory.
  - For `make check` command.
  - Homepage:
    <https://www.qemu.org>
  - Download:
    <https://www.qemu.org/download>

**And other dependencies for building Linux kernel.**

## Build source tarball

```shell
make -f Makefile.devel dist
```

## Build disk image

**You need to install the dependencies first, and make sure you are in source directory.**

```shell
./configure
make -j$(nproc)
```

The disk image will be name to `disk.img`.

## Configure parameters

- `--with-busybox-version=[X.X.X]`
  - Specify the version of Busybox.
  - Default is `1.36.1`.

- `--with-linux-version=[X.X.X]`
  - Specify the version of Linux kernel.
  - Default is `6.7.5`.

- `--with-busybox-mirror={OFFICIAL | <URL>}`
  - Specify the mirror of Busybox. If you want to use the official mirror, set it to `OFFICIAL`. Otherwise, set it to the URL of the mirror.
  - Default is `OFFICIAL`.

- `--with-linux-mirror={OFFICIAL | CDN | TSINGHUA | ALIYUN | USTC | <URL>}`
  - Specify the mirror of Linux kernel. If you want to use the Tsinghua mirror, set it to `TSINGHUA`. Otherwise, set it to the URL of the mirror.
  - Default is `OFFICIAL`.

Like this:

```shell
./configure --with-busybox-version=1.36.1 --with-linux-version=6.7.5 --with-busybox-mirror=OFFICIAL --with-linux-mirror=TSINGHUA
```

## Run disk image

```shell
make check
```

Or you can run the disk image with QEMU.

```shell
qemu-system-x86_64 -hda disk.img
```

## Copyright

The MinimalLinux is under GPL 2.0,
see file [LICENSE](./LICENSE).

## Download

<https://github.com/ChenPi11/MinimalLinux/releases>

## Homepage

<https://github.com/ChenPi11/MinimalLinux>