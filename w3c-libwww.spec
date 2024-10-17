%define snap 20061204

Summary:        HTTP library of common code
Name:           w3c-libwww
Version:        5.4.1
Release:        %mkrel 0.%{snap}.8
License:        W3C License
Group:          System/Libraries
URL:            https://www.w3.org/Library
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
%{_bindir}/libwww-config
%{multiarch_bindir}/libwww-config
%{_libdir}/lib*.so
%dir %{_includedir}/w3c-libwww
%{_includedir}/w3c-libwww/*.h


%changelog
* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 5.4.1-0.20061204.7mdv2011.0
+ Revision: 661754
- multiarch fixes

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 5.4.1-0.20061204.6mdv2011.0
+ Revision: 608149
- rebuild

* Thu Apr 08 2010 Funda Wang <fwang@mandriva.org> 5.4.1-0.20061204.5mdv2010.1
+ Revision: 533061
- bump rel
- finally fix linkage with newer flags

* Thu Apr 08 2010 Eugeni Dodonov <eugeni@mandriva.com> 5.4.1-0.20061204.4mdv2010.1
+ Revision: 533058
- Rebuild for new openssl

  + Funda Wang <fwang@mandriva.org>
    - rebuild

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 5.4.1-0.20061204.2mdv2010.1
+ Revision: 511657
- rebuilt against openssl-0.9.8m

* Sat Oct 03 2009 Funda Wang <fwang@mandriva.org> 5.4.1-0.20061204.1mdv2010.0
+ Revision: 453220
- fix installation

* Mon Apr 13 2009 Funda Wang <fwang@mandriva.org> 5.4.1-0.20061204.1mdv2009.1
+ Revision: 366570
- rediff incdir patch

* Fri Jul 11 2008 Oden Eriksson <oeriksson@mandriva.com> 5.4.1-0.20061204.1mdv2009.0
+ Revision: 233675
- 5.4.1-20061204 (partly synced with w3c-libwww-5.4.1-0.10.20060206cvs.fc9.src.rpm)
- use both _disable_ld_as_needed and _disable_ld_no_undefined due to ugly autopoo

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sat Nov 10 2007 David Walluck <walluck@mandriva.org> 5.4.0-9mdv2008.1
+ Revision: 107393
- add correct sources
- call %%{configure2_5x}
- use upstream sources


* Sat Mar 17 2007 Oden Eriksson <oeriksson@mandriva.com> 5.4.0-8mdv2007.1
+ Revision: 145611
- Import w3c-libwww

* Sat Mar 17 2007 Oden Eriksson <oeriksson@mandriva.com> 5.4.0-8mdv2007.1
- use the %%mrel macro
- bunzip patches

* Wed Nov 16 2005 Thierry Vignaud <tvignaud@mandriva.com> 5.4.0-7mdk
- security update for CAN-2005-3183 (P4)

* Mon Nov 14 2005 Oden Eriksson <oeriksson@mandriva.com> 5.4.0-6mdk
- rebuilt against openssl-0.9.8a

* Mon Jan 31 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.4.0-5mdk
- fix build with new rpm

* Sat Dec 25 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 5.4.0-4mdk
- sync with fedora to get things rebuilding
- fix summary-ended-with-dot
- cosmetics

* Tue Sep 21 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.4.0-3mdk
- use automake 1.4

