#
# Conditional build:
%bcond_with	static_libs	# static library
#
Summary:	A readwrite library to manage ova files
Summary(pl.UTF-8):	Biblioteka do odczytu i zapisu plików ova
Name:		libovf-glib
# meson.build /version:
Version:	0.1.0
%define	gitref	52d35970d385d0beda4b765a7264d77e79736549
%define	snap	20190308
%define	rel	1
Release:	0.%{snap}.1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://gitlab.gnome.org/felipeborges/libovf-glib/-/tags
Source0:	https://gitlab.gnome.org/felipeborges/libovf-glib/-/archive/%{gitref}/%{name}-%{snap}.tar.bz2
# Source0-md5:	f6e4c0116e67ea59d4e4dcc76c969148
URL:		https://gitlab.gnome.org/felipeborges/libovf-glib
BuildRequires:	glib2-devel >= 1:2.50
BuildRequires:	gobject-introspection-devel
BuildRequires:	libarchive-devel
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	meson >= 0.47.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	vala
Requires:	glib2 >= 1:2.50
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libgovf is a library for reading and writing virtual machine images in
the Open Virtualization Format.

%description -l pl.UTF-8
libgovf to biblioteka do odczytu i zapisu obrazów maszyn wirtualnych
wykorzystujących Open Virtualization Format.

%package devel
Summary:	Header files for libgovf library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libgovf
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.50
Requires:	libarchive-devel
Requires:	libxml2-devel >= 2.0

%description devel
Header files for libgovf library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libgovf.

%package static
Summary:	Static libgovf library
Summary(pl.UTF-8):	Statyczna biblioteka libgovf
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libgovf library.

%description static -l pl.UTF-8
Statyczna biblioteka libgovf.

%package -n vala-libovf-glib
Summary:	Vala API for libgovf library
Summary(pl.UTF-8):	API języka Vala do biblioteki libgovf
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala
BuildArch:	noarch

%description -n vala-libovf-glib
Vala API for libgovf library.

%description -n vala-libovf-glib -l pl.UTF-8
API języka Vala do biblioteki libgovf.

%prep
%setup -q -n %{name}-%{gitref}

%if %{with static_libs}
%{__sed} -i -e '/^govf_lib = / s/shared_library/library/' govf/meson.build
%endif

%build
%meson build

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/libgovf-0.1.so
%{_libdir}/girepository-1.0/Govf-0.1.typelib

%files devel
%defattr(644,root,root,755)
%{_includedir}/govf
%{_datadir}/gir-1.0/Govf-0.1.gir
%{_pkgconfigdir}/govf-0.1.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgovf-0.1.a
%endif

%files -n vala-libovf-glib
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/govf-0.1.deps
%{_datadir}/vala/vapi/govf-0.1.vapi
