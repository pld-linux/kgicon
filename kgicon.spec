Summary:	KGI - Kernel Graphics Interface for FB-console	
Summary(pl):	KGI - Kernel Graphics Interface
Name:		kgicon
Version:	990710
Release:	1
Group:		Base
Group(pl):	Podstawowe
Copyright:	GPL
#Source0:	ftp://ftp.ggi-project.org/pub/ggi/ggi-snapshots/ggi-devel-%{version}.tar.gz
Source0:	%{name}-devel-%{version}.tar.gz
Source1:	kgicon-config-vga
Source2:	kgicon-config-virge
Source3:	kgicon-config-riva
Patch:		kgicon-virge-accel.patch
Patch1:		kgicon-riva-comments.patch
BuildPrereq:	bison		
URL:		http://www.ggi-project.org/
BuildRoot:   	/tmp/%{name}-%{version}-root

%description
KGICON are kernel-level drivers for GGI (General Graphics Interface) based
on Linux 2.2.x frame-buffer interface

%description -l pl
KGICON to niskopoziomowe sterowniki dla GGI oparte o interfejs frame-buffer 
w j±drach 2.2.x

%package utils
Summary:	Utilities for KGICON drivers
Summary(pl):	obs³uga aalib dla LibGII
Group:		Library
Group(pl):	Biblioteki
Requires:	%{name} = %{version}
Obsoletes:	fbset

%description utils 
Utilities for KGICON.
Includes:
  setmon - utility for setting monitor parameters 
  fbset - utility for setting framebuffer modes

%package devel
Summary:	SVGALib target for LibGII
Summary(pl):	obs³uga SVGALib dla LibGII
Group:		Development
Group(pl):	Programowanie	
Requires:	%{name} = %{version}

%description devel
Header files for KGICON

%define _sysconfdir /etc

%prep
%setup -qn degas/%{name}
%patch -p1
%patch1 -p1

%build
cd kgi
LDFLAGS="-s" ; export LDFLAGS
%configure

cp ${RPM_SOURCE_DIR}/kgicon-config-vga .config
make
mv kgicon.o kgicon-vga.o

cp ${RPM_SOURCE_DIR}/kgicon-config-virge .config
make
mv kgicon.o kgicon-virge.o

cp ${RPM_SOURCE_DIR}/kgicon-config-riva .config
make
mv kgicon.o kgicon-riva.o

cd ../util/fbset
make

cd ../setmon
%configure
make

cd ../..


%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_sbindir}
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/ggi
install -d $RPM_BUILD_ROOT/%{_mandir}/{man5,man8}
install -d $RPM_BUILD_ROOT/%{_includedir}
install -d $RPM_BUILD_ROOT/lib/modules/`uname -r`/misc

cp -r include/kgi $RPM_BUILD_ROOT/usr/include/kgi

cd kgi
cp -r include/* $RPM_BUILD_ROOT%{_includedir}/kgi/
install kgicon-*.o $RPM_BUILD_ROOT/lib/modules/`uname -r`/misc


cd ../util/fbset
install fbset $RPM_BUILD_ROOT/%{_sbindir}
install fbset.8 $RPM_BUILD_ROOT%{_mandir}/man8
install fb.modes.5 $RPM_BUILD_ROOT%{_mandir}/man5
install etc/fb.modes.ATI $RPM_BUILD_ROOT%{_sysconfdir}/fb.modes


cd ../setmon
make install prefix=$RPM_BUILD_ROOT/usr
install sample.multisync $RPM_BUILD_ROOT%{_sysconfdir}/ggi/kgicon.mon

cd ../..
gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	kgi/README.* util/setmon/README util/setmon/NEWS

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
%doc util/fbset/etc/*
%config %{_sysconfdir}/fb.modes
%config %{_sysconfdir}/ggi/kgicon.mon
%attr(755,root,root) %{_sbindir}/fbset
%attr(755,root,root) %{_sbindir}/setmon
 
%files devel
%defattr(644,root,root,755)
%{_includedir}/kgi
