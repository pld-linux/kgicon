Summary:	KGI - Kernel Graphics Interface for FB-console
Summary(pl):	KGI - Kernel Graphics Interface
Name:		kgicon
Version:	20010225
Release:	1
Group:		Base
License:	GPL
Source0:	ftp://ftp.ggi-project.org/pub/ggi/ggi-snapshots/ggi-devel-%{name}-%{version}.tar.bz2
Source1:	%{name}-config-vga
Source2:	%{name}-config-virge
Source3:	%{name}-config-riva
BuildRequires:	bison
BuildRequires:	autoconf
BuildRequires:	automake
URL:		http://www.ggi-project.org/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KGICON are kernel-level drivers for GGI (General Graphics Interface)
based on Linux 2.2.x frame-buffer interface

%description -l pl
KGICON to niskopoziomowe sterowniki dla GGI oparte o interfejs
frame-buffer w j±drach 2.2.x

%package utils
Summary:	Utilities for KGICON drivers
Summary(pl):	obs³uga aalib dla LibGII
Group:		Libraries
Requires:	%{name} = %{version}
Obsoletes:	fbset

%description utils
Utilities for KGICON. Includes: setmon - utility for setting monitor
parameters fbset - utility for setting framebuffer modes

%description utils -l pl
Programy u¿ytkowe dla KGICON. Zawieraj±: setmon - narzêdzie do
ustawiania parametrów monitora, fbset - narzêdzie to ustawiania trybów
framebuffera.

%package devel
Summary:	development files
Summary(pl):	pliki dla developerów
Group:		Development
Requires:	%{name} = %{version}

%description devel
Header files for KGICON

%description devel -l pl
Pliki nag³ówkowe dla KGICON

%define _sysconfdir /etc

%prep
%setup -qn degas/%{name}

%build
cd kgi
%configure

cp -f %{SOURCE1} .config
%{__make}
mv -f kgicon.o ../kgicon-vga.o

rm -f .config && cp -f %{SOURCE2} .config
%{__make} realclean depend all
mv -f kgicon.o ../kgicon-virge.o

#rm -f .config && cp -f %{SOURCE3} .config
#%{__make} realclean depend all
#mv -f kgicon.o ../kgicon-riva.o

cd ../util/fbset
%{__make}

cd ../setmon
automake -a -c -i
aclocal
autoconf
%configure
%{__make}

cd ../..

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_sbindir}
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/ggi
install -d $RPM_BUILD_ROOT/%{_mandir}/{man5,man8}
install -d $RPM_BUILD_ROOT/%{_includedir}
install -d $RPM_BUILD_ROOT/lib/modules/`uname -r`/misc

cp -r include/kgi $RPM_BUILD_ROOT%{_includedir}/kgi

cd kgi
cp -r include/* $RPM_BUILD_ROOT%{_includedir}/kgi/
install ../kgicon-*.o $RPM_BUILD_ROOT/lib/modules/`uname -r`/misc

cd ../util/fbset
install fbset $RPM_BUILD_ROOT/%{_sbindir}
install fbset.8 $RPM_BUILD_ROOT%{_mandir}/man8
install fb.modes.5 $RPM_BUILD_ROOT%{_mandir}/man5
install etc/fb.modes.ATI $RPM_BUILD_ROOT%{_sysconfdir}/fb.modes

cd ../setmon
%{__make} install DESTDIR=$RPM_BUILD_ROOT
install sample.multisync $RPM_BUILD_ROOT%{_sysconfdir}/ggi/kgicon.mon

cd ../..
gzip -9nf kgi/README.* util/setmon/README util/setmon/NEWS

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc kgi/README.*
/lib/modules/*/misc/*

%files utils
%defattr(644,root,root,755)
%doc util/setmon/README.gz
%doc util/setmon/NEWS.gz
%doc util/fbset%{_sysconfdir}/*
%config %{_sysconfdir}/fb.modes
%config %{_sysconfdir}/ggi/kgicon.mon
%attr(755,root,root) %{_sbindir}/fbset
%attr(755,root,root) %{_sbindir}/setmon

%files devel
%defattr(644,root,root,755)
%{_includedir}/kgi
