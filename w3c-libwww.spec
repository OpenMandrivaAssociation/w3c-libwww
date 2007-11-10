Name:           w3c-libwww
Version:        5.4.0
Release:        %mkrel 9
Summary:        HTTP library of common code
License:        W3C License
Group:          System/Libraries
URL:            http://www.w3.org/Library
Source0:        http://www.w3.org/Library/Distribution/w3c-libwww-%{version}.tgz
Source1:        http://www.w3.org/Library/Distribution/w3c-libwww-%{version}.tgz.md5
Patch0:         w3c-libwww-5.3.2-lib64.patch
Patch1:         w3c-libwww-5.3.2-incdir.patch
Patch2:         w3c-libwww-ppc64.patch
Patch3:         w3c-libwww-autostar.patch
Patch4:         w3c-libwww-5.4.0-htbound.patch
BuildRequires:  zlib-devel
BuildRequires:  openssl-devel
BuildRequires:  multiarch-utils >= 1.0.4-1mdk
%if %mdkversion >= 1010
BuildRequires:  automake1.4
%endif
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
%patch0 -p1 -b .lib64
%patch1 -p1
%patch2 -p1 -b .ppc64
%patch3 -p1 -b .autostar
%patch4 -p1 -b .can-2005-3183

export FORCE_AUTOCONF_2_5=1
libtoolize -c -f
aclocal
automake --add-missing
autoconf
autoheader

echo timestamp > stamp-h.in
touch Library/User/Extrnals.html
chmod 644 `find -name \*.gif`

%build
%{configure2_5x} \
    --enable-shared \
    --with-gnu-ld \
    --with-regex \
    --with-zlib \
    --with-ssl \
    --with-md5
%{make}

%install
rm -rf %{buildroot}
%{makeinstall_std}

%multiarch_binaries %{buildroot}%{_bindir}/libwww-config
%multiarch_includes %{buildroot}%{_includedir}/wwwconf.h

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc *.html  Icons/*/*.gif
%{_libdir}/libpics*.so.*
%{_libdir}/libwww*.so.*
%{_libdir}/libxml*.so.*
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
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_libdir}/lib*.so
%multiarch %{_includedir}/multiarch-*-linux/wwwconf.h
%{_includedir}/*.h
%dir %{_includedir}/w3c-libwww
%{_includedir}/w3c-libwww/*.h
