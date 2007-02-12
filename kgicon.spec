Summary:	KGI - Kernel Graphics Interface for FB-console
Summary(pl.UTF-8):   KGI - Kernel Graphics Interface dla konsoli FB
Name:		kgicon
Version:	20010313
Release:	1
Group:		Base
License:	GPL
Source0:	ftp://ftp.ggi-project.org/pub/ggi/ggi-snapshots/ggi-devel-%{name}-%{version}.tar.bz2
# Source0-md5:	5d3a1c2a5b0929286af40ca026cb4ffa
Source1:	%{name}-config-vga
Source2:	%{name}-config-virge
Source3:	%{name}-config-riva
Patch0:		%{name}-fix.patch
BuildRequires:	autoconf
BuildRequires:	automake
URL:		http://www.ggi-project.org/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KGICON are kernel-level drivers for GGI (General Graphics Interface)
based on Linux 2.2.x frame-buffer interface.

%description -l pl.UTF-8
KGICON to niskopoziomowe sterowniki dla GGI oparte o interfejs
frame-buffer w jądrach 2.2.x.

%package utils
Summary:	Utilities for KGICON drivers
Summary(pl.UTF-8):   Narzędzia do sterowników KGICON
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	fbset

%description utils
Utilities for KGICON. Includes setmon - utility for setting monitor
parameters.

%description utils -l pl.UTF-8
Programy użytkowe dla KGICON. Zawierają setmon - narzędzie do
ustawiania parametrów monitora.

%package devel
Summary:	Header files for KGICON
Summary(pl.UTF-8):   Pliki nagłówkowe KGICON
Group:		Development
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for KGICON.

%description devel -l pl.UTF-8
Pliki nagłówkowe KGICON.

%package -n kernel-video-kgicon
Summary:	KGI - Kernel Graphics Interface for FB-console
Summary(pl.UTF-8):   KGI - Kernel Graphics Interface
Group:		Base/Kernel

%description -n kernel-video-kgicon
KGICON are kernel-level drivers for GGI (General Graphics Interface)
based on Linux 2.2.x frame-buffer interface.

%description -n kernel-video-kgicon -l pl.UTF-8
KGICON to niskopoziomowe sterowniki dla GGI oparte o interfejs
frame-buffer w jądrach 2.2.x.

%prep
%setup -qn degas
%patch0 -p1

%build
cd kgicon/kgi
%{__autoconf}
%configure

cp -f %{SOURCE1} .config
%{__make}
mv -f kgicon.o ../kgicon-vga.o

rm -f .config && cp -f %{SOURCE2} .config
%{__make} realclean depend all
mv -f kgicon.o ../kgicon-virge.o

#rm -f .config && cp -f %{SOURCE3} .config
#%%{__make} realclean depend all
#mv -f kgicon.o ../kgicon-riva.o

cd ../util/setmon
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/ggi,%{_includedir}} \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc

cd kgicon
rm -f include/kgi/autoconf.h.in
cp -r include/kgi $RPM_BUILD_ROOT%{_includedir}/kgi

cd kgi
cp -r include/* $RPM_BUILD_ROOT%{_includedir}/kgi
install ../kgicon-*.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc

cd ../util/setmon
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
install sample.multisync $RPM_BUILD_ROOT%{_sysconfdir}/ggi/kgicon.mon

%clean
rm -rf $RPM_BUILD_ROOT

%files utils
%defattr(644,root,root,755)
%doc kgicon/util/setmon/{AUTHORS,NEWS,README}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ggi/kgicon.mon
%attr(755,root,root) %{_sbindir}/setmon

%files devel
%defattr(644,root,root,755)
%{_includedir}/kgi

%files -n kernel-video-kgicon
%defattr(644,root,root,755)
%doc kgicon/kgi/chipset/{S3/{README.*,KNOWN-BUGS},IBM/{README,TODO}.vga}
/lib/modules/*/misc/*.o*
