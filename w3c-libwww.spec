%define snap 20061204

Summary:        HTTP library of common code
Name:           w3c-libwww
Version:        5.4.1
Release:        %mkrel 0.%{snap}.6
License:        W3C License
Group:          System/Libraries
URL:            http://www.w3.org/Library
Source0:        http://www.w3.org/Library/Distribution/w3c-libwww-%{version}-%{snap}.tar.gz
Patch0:		w3c-libwww-configure.patch
Patch1:		w3c-libwww-5.4.1-incdir.patch
Patch2:		w3c-libwww-ppc64.patch
Patch3:		w3c-libwww-md5.patch
Patch4:		w3c-libwww-expat.patch
Patch5:		w3c-libwww-lib64.diff
Patch6:		w3c-libwww-5.4.1-fix-install.patch
Patch7:		w3c-libwww-5.4.1-fix-link.patch
BuildRequires:	autoconf2.5
BuildRequires:	automake
BuildRequires:	expat-devel
BuildRequires:	libtool
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Libwww is a general-purpose Web API written in C for Unix and Windows (Win32).
With a highly extensible and layered API, it can accommodate many different
types of applications including clients, robots, etc. The purpose of libwww
is to provide a highly optimized HTTP sample implementation as well as other
Internet protocols and to serve as a testbed for protocol experiments.

See: http://www.w3.org/Consortium/Legal/copyright-software.html for
further information on its license.

%package devel
Summary:        Libraries and header files for programs that use libwww
Group:          Development/Other
Requires:       %{name} = %{version}-%{release}

%description devel
Static libraries and header files for libwww, which are available as public
libraries.

%package apps
Summary:        Applications built using Libwww web library: e.g. Robot, etc
Group:          Networking/WWW
Requires:       %{name} = %{version}-%{release}

%description apps
Web applications built using Libwww: Robot, Command line tool, 
line mode browser.  The Robot can crawl web sites faster, and
with lower load, than any other web walker that we know of, 
due to its extensive pipelining and use of HTTP/1.1.

The command line tool (w3c) is very useful for manipulation of 
Web sites that implement more than just HTTP GET (e.g. PUT, 
 POST, etc.).

The line mode browser is a minimal line mode web browser; 
often useful to convert to ascii text.  Currently unavailable
until someone updates it to some new interfaces. (hint, hint...)

%prep

%setup -q

#cvs -d :pserver:anonymous@dev.w3.org:/sources/public login
#after which you type "anonymous" as password.
#cvs -d :pserver:anonymous@dev.w3.org:/sources/public -z3 checkout libwww

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0544 -exec chmod 644 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;
		
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

%patch0 -p1
%patch1 -p1
%patch2 -p1 -b .ppc64
%patch3 -p0
%patch4 -p1
%patch5 -p0
%patch6 -p0
%patch7 -p0 -b .link

# we don't want the libwww version
rm -rf modules/expat

%build
autoreconf -fi
echo timestamp > stamp-h.in
%configure2_5x \
    --enable-shared \
    --disable-static \
    --with-gnu-ld \
    --with-regex \
    --with-zlib \
    --with-ssl \
    --enable-reentrant

%make

%install
rm -rf %{buildroot}

%makeinstall_std

%multiarch_binaries %{buildroot}%{_bindir}/libwww-config

%if %mdkversion < 200900
%post -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc *.html  Icons/*/*.gif
%{_libdir}/libpics*.so.*
%{_libdir}/libwww*.so.*
%{_libdir}/libmd5.so.*
%{_datadir}/w3c-libwww

%files apps
%defattr(-,root,root)
%doc COPYRIGH
%{_bindir}/webbot
%{_bindir}/w3c
%{_bindir}/www

%files devel
%defattr(-,root,root)
%doc COPYRIGH
%multiarch %{_bindir}/multiarch-*-linux/libwww-config
%{_bindir}/libwww-config
%{_libdir}/lib*.la
%{_libdir}/lib*.so
%dir %{_includedir}/w3c-libwww
%{_includedir}/w3c-libwww/*.h
