%define	name		pptpd-server
%define	realname	pptpd
%define	version		1.3.4
%define	rel		4
%define	release		%{rel}
%define	pppver		%(rpm -q --qf %{VERSION} ppp)
%define buildlibwrap 1
%define buildbsdppp 0
%define buildslirp 0
%define buildipalloc 0
%define buildbcrelay 1
%define buildpnsmode 0

Summary:	PoPToP Linux VPN server 
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Networking/Other
Source0:	%{realname}-%{version}.tar.gz
Source1:	%{realname}-init
URL:		http://poptop.sourceforge.net/
Provides:	%{realname} = %{version}-%{release} poptop = %{version}-%{release}
Requires:	tcp_wrappers ppp = %{pppver}
# We need ppp to get its version
BuildRequires:	ppp
Requires(post):	rpm-helper
Requires(preun):	rpm-helper

%description
PoPToP is the PPTP server solution for Linux (ports exist for Solaris
2.6, OpenBSD and FreeBSD and other). To date no real solution existed
if you wished to include Linux server in PPTP established VPNs. PoPToP
resolves that problem by allowing Linux servers to function seamlessly
in the PPTP VPN environment. This enables administrators to leverage
the considerable benifits of both Microsoft and Linux. The current
release supports Windows 9x/NT/2000 PPTP clients and PPTP Linux
clients. PoPToP is free GNU software.

# allow --with[out] <feature> at rpm command line build
# e.g. --with ipalloc --without libwrap
# --with overrides --without
%{?_without_libwrap: %{expand: %%define buildlibwrap 0}}
%{?_without_bsdppp: %{expand: %%define buildbsdppp 0}}
%{?_without_slirp: %{expand: %%define buildslirp 0}}
%{?_without_ipalloc: %{expand: %%define buildipalloc 0}}
%{?_without_bcrelay: %{expand: %%define buildbcrelay 0}}
%{?_without_pnsmode: %{expand: %%define buildpnsmode 0}}
%{?_with_libwrap: %{expand: %%define buildlibwrap 1}}
%{?_with_bsdppp: %{expand: %%define buildbsdppp 1}}
%{?_with_slirp: %{expand: %%define buildslirp 1}}
%{?_with_ipalloc: %{expand: %%define buildipalloc 1}}
%{?_with_bcrelay: %{expand: %%define buildbcrelay 1}}
%{?_with_pnsmode: %{expand: %%define buildpnsmode 1}}

%prep
%setup -q -n %{realname}-%{version}

rm -rf `find -name CVS`

%build
buildopts=""
%if %{buildlibwrap}
buildopts="$buildopts --with-libwrap"
%endif
%if %{buildbsdppp}
buildopts="$buildopts --with-bsdppp"
%endif
%if %{buildslirp}
buildopts="$buildopts --with-slirp"
%endif
%if %{buildipalloc}
buildopts="$buildopts --with-pppd-ip-alloc"
%endif
%if %{buildbcrelay}
buildopts="$buildopts --with-bcrelay"
%endif
%if %{buildpnsmode}
buildopts="$buildopts --with-pns-mode"
%endif
%configure2_5x $buildopts
echo '#undef VERSION' >> plugins/patchlevel.h
echo '#define VERSION "%{pppver}"' >> plugins/patchlevel.h

perl -pi -e 's|-o root||' plugins/Makefile
perl -pi -e 's|/lib/pptpd|/%{_lib}/pptpd|' plugins/Makefile
perl -pi -e 's|/usr/lib/pptpd|%{_libdir}/pptpd|' pptpctrl.c

%make CFLAGS="$RPM_OPT_FLAGS -fPIC -fno-builtin -Wall -DSBINDIR='\"%{_sbindir}\"'" 

%install
%makeinstall

install -m0644 samples/%{realname}.conf -D %{buildroot}%{_sysconfdir}/%{realname}.conf
install -m0644 samples/options.%{realname} -D %{buildroot}%{_sysconfdir}/ppp/options.%{realname}
install -m0755 %{SOURCE1} -D %{buildroot}%{_initrddir}/%{realname}
install -m0755 tools/vpnuser -D %{buildroot}%{_bindir}/vpnuser
install -m0755 tools/vpnstats -D %{buildroot}%{_bindir}/vpnstats
install -m0755 tools/vpnstats.pl -D %{buildroot}%{_bindir}/vpnstats.pl
install -m0755 tools/pptp-portslave -D %{buildroot}%{_sbindir}/pptp-portslave

%post
%_post_service	%{realname}

%preun
%_preun_service	%{realname}

%files
%defattr(644,root,root,755)
%doc AUTHORS README* TODO ChangeLog* samples
%{_mandir}/man[58]/pptp*
%config(noreplace) %{_sysconfdir}/%{realname}.conf
%config(noreplace) %{_sysconfdir}/ppp/options.%{realname}
%defattr(755,root,root,755)
%{_initrddir}/%{realname}
%{_sbindir}/*
%{_bindir}/*
%{_libdir}/pptpd


%changelog
* Thu Apr 05 2012 Johnny A. Solbu <solbu@mandriva.org> 1.3.4-4
+ Revision: 789268
- Fix dead URL
- Spec cleanup

* Tue Dec 07 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3.4-3mdv2011.0
+ Revision: 614608
- the mass rebuild of 2010.1 packages

* Thu Jun 17 2010 Pascal Terjan <pterjan@mandriva.org> 1.3.4-2mdv2010.1
+ Revision: 548270
- Fix broken dependency

  + Michael Scherer <misc@mandriva.org>
    - fix wrong command in init script

* Thu Jan 07 2010 Frederik Himpe <fhimpe@mandriva.org> 1.3.4-1mdv2010.1
+ Revision: 487319
- Update to version 1.3.4
- Use %%configure2_5x to fix ./configure warnings

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 1.3.0-3mdv2010.0
+ Revision: 430771
- rebuild

* Wed Jan 02 2008 Olivier Blin <blino@mandriva.org> 1.3.0-2mdv2008.1
+ Revision: 140735
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - fix ppp version and dependency on it


* Wed Aug 30 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.3.0-2mdv2007.0
- ppp_mppe_mppc module has been renamed to ppp_mppe, rename initscript accordingly
- don't bzip2 initscript
- gprintify initscript up front for translation
- fix macro-in-%%changelog

* Thu Mar 02 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.3.0-1mdk
- 1.3.0

* Thu Feb 02 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.2.1-7mdk
- move ppp options file to correct directory

* Mon Jan 16 2006 Olivier Blin <oblin@mandriva.com> 1.2.1-6mdk
- add -fPIC to fix build on x86_64
- fix plugin path on x86_64

* Mon Jan 09 2006 Olivier Blin <oblin@mandriva.com> 1.2.1-5mdk
- fix typo in initscript

* Mon Jan 09 2006 Olivier Blin <oblin@mandriva.com> 1.2.1-4mdk
- convert parallel init to LSB
- split Requires(X,Y)

* Tue Jan 03 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.2.1-3mdk
- add parallel init support
- fix executable-marked-as-config-file
- be sure to include debug stuff only in debug package
- fix requires(post,preun)

* Wed Jun 01 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.2.1-2mdk
- add poptop to provides
- versioned provides
- %%mkrel
- compile with $RPM_OPT_FLAGS

* Wed Jun 23 2004 Florin <florin@mandrakesoft.com> 1.2.1-1mdk
- 1.2.1
- add modprobe lines in the initscript
- remove the '-o root' in make install
- remove the Anon-CVS and the html/* files in docs
- add the tools %%{_bindir} binaries
- use mcros for %%configure

