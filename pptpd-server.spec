%define	name		pptpd-server
%define	realname	pptpd
%define	version		1.3.0
%define	rel		2
%define	release		%mkrel %{rel}
%define	pppver		2.4.4
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
Source0:	%{realname}-%{version}.tar.bz2
Source1:	%{realname}-init
#Patch0: %{realname}-%{version}-headers.patch.bz2
URL:		http://www.poptop.org/
Provides:	%{realname} = %{version}-%{release} poptop = %{version}-%{release}
Requires:	tcp_wrappers ppp = %{pppver}
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

#%patch -p1

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
%configure $buildopts
echo '#undef VERSION' >> plugins/patchlevel.h
echo '#define VERSION "%{pppver}"' >> plugins/patchlevel.h

perl -pi -e 's|-o root||' plugins/Makefile
perl -pi -e 's|/lib/pptpd|/%{_lib}/pptpd|' plugins/Makefile
perl -pi -e 's|/usr/lib/pptpd|%{_libdir}/pptpd|' pptpctrl.c

%make CFLAGS="$RPM_OPT_FLAGS -fPIC -fno-builtin -Wall -DSBINDIR='\"%{_sbindir}\"'" 

%install
rm -rf %{buildroot}
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

%clean 
rm -rf %{buildroot}

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
