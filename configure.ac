dnl Copyright (C) 2024 ChenPi11.
dnl This file is part of the MinimalLinux.
dnl
dnl MinimalLinux is free software: you can redistribute it and/or modify
dnl it under the terms of the GNU General Public License as published
dnl by the Free Software Foundation; either version 2 of the License,
dnl or (at your option) any later version.
dnl
dnl MinimalLinux is distributed in the hope that it will be useful,
dnl but WITHOUT ANY WARRANTY; without even the implied warranty of
dnl MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
dnl GNU General Public License for more details.
dnl
dnl You should have received a copy of the GNU General Public License
dnl along with this program.  If not, see <https://www.gnu.org/licenses/>.

AC_PREREQ([2.64])
AC_INIT([MinimalLinux], [0.1])
AC_PROG_MAKE_SET

dnl           checks for basic programs

AC_PROG_CC

AC_PATH_PROG([STRIP], [strip], [:]) dnl sets STRIP

dnl           check for host type

dnl           checks for programs

CL_PROG_CP
CL_PROG_LN
AC_PROG_LN_S
AC_PATH_PROG([CHMOD], [chmod])
AC_PATH_PROG([CHOWN], [chown])
AC_PATH_PROG([FDISK], [fdisk])
AC_PATH_PROG([GRUB_INSTALL], [grub-install])
AC_PATH_PROG([KPARTX], [kpartx])
AC_PATH_PROG([LOSETUP], [losetup])
AC_PATH_PROG([MKDIR], [mkdir])
AC_PATH_PROG([MKFS_EXT4], [mkfs.ext4])
AC_PATH_PROG([MKNOD], [mknod])
AC_PATH_PROG([MOUNT], [mount])
AC_PATH_PROG([PYTHON], [python])
if test -z "$PYTHON"; then
    AC_PATH_PROG([PYTHON], [python3])
fi
AC_SUBST([PYTHON])
AC_PATH_PROG([QEMU_IMG], [qemu-img])
AC_PATH_PROG([RM], [rm])
AC_PATH_PROG([SUDO], [sudo])
AC_PATH_PROG([TAR], [tar])
AC_PATH_PROG([UMOUNT], [umount])
AC_PATH_PROG([WGET], [wget])
AC_PATH_PROG([XZ], [xz])

# Options
AC_ARG_WITH([busybox-version],
    [AS_HELP_STRING([--with-busybox-version=X.X.X],
        [define the version of BusyBox])],
    [BUSYBOX_VERSION=$withval],
    [BUSYBOX_VERSION=1.36.1]
)
AC_SUBST([BUSYBOX_VERSION])

AC_ARG_WITH([linux-version],
    [AS_HELP_STRING([--with-linux-version=X.X.X],
        [define the version of Linux kernel])],
    [LINUX_VERSION=$withval],
    [LINUX_VERSION=6.7.5]
)
LINUX_VERSION_MAJOR=$(echo $LINUX_VERSION | cut -d. -f1)
AC_SUBST([LINUX_VERSION])
AC_SUBST([LINUX_VERSION_MAJOR])

dnl Use '[[', ']]' instead of '[', ']' to avoid Autoconf interpreting.
BUSYBOX_MIRROR=$(echo "$BUSYBOX_MIRROR" | tr "[[:lower:]]" "[[:upper:]]")
BUSYBOX_MIRROR_CUSTOME=
if test "$BUSYBOX_MIRROR" != "OFFICIAL"; then
    BUSYBOX_MIRROR_CUSTOME=$BUSYBOX_MIRROR
    BUSYBOX_MIRROR=CUSTOME
fi
AC_SUBST([BUSYBOX_MIRROR])
AC_SUBST([BUSYBOX_MIRROR_CUSTOME])

AC_ARG_WITH([linux-mirror],
    [AS_HELP_STRING([--with-linux-mirror=OFFICIAL | CDN | TSINGHUA | ALIYUN | USTC | <URL>],
        [define the mirror of Linux kernel])],
    [LINUX_MIRROR=$withval],
    [LINUX_MIRROR=OFFICIAL]
)
LINUX_MIRROR=$(echo "$LINUX_MIRROR" | tr "[[:lower:]]" "[[:upper:]]")
LINUX_MIRROR_CUSTOME=
if test "$LINUX_MIRROR" != "OFFICIAL" -a "$LINUX_MIRROR" != "CDN" -a "$LINUX_MIRROR" != "TSINGHUA" -a "$LINUX_MIRROR" != "ALIYUN" -a "$LINUX_MIRROR" != "USTC"; then
    LINUX_MIRROR_CUSTOME=$LINUX_MIRROR
    LINUX_MIRROR=CUSTOME
fi
AC_SUBST([LINUX_MIRROR])
AC_SUBST([LINUX_MIRROR_CUSTOME])

AC_ARG_WITH([busybox-mirror],
    [AS_HELP_STRING([--with-busybox-mirror=OFFICIAL | <URL>],
        [define the mirror of BusyBox])],
    [BUSYBOX_MIRROR=$withval],
    [BUSYBOX_MIRROR=OFFICIAL]
)

dnl           checks for build configuration

AC_CONFIG_FILES([Makefile])
AC_CONFIG_FILES([mirrors.mk])
AC_OUTPUT
