#
# Conditional build:
%bcond_without	java		# Java binding
%bcond_without	static_libs	# static libraries
#
Summary:	Library to parse, generate and operate on KML
Summary(pl.UTF-8):	Biblioteka do analizy, generowania i operowania na danych KML
Name:		libkml
Version:	1.3.0
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/libkml/libkml/releases
Source0:	https://github.com/libkml/libkml/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e663141e9ebd480538b25d226e1b2979
Patch0:		%{name}-python.patch
Patch1:		%{name}-minizip-git.patch
Patch2:		%{name}-minizip-nocrypt.patch
Patch3:		%{name}-pc.patch
URL:		https://github.com/libkml/libkml
BuildRequires:	boost-devel >= 1.44.0
BuildRequires:	cmake >= 2.8
BuildRequires:	curl-devel >= 7.12.3
BuildRequires:	expat-devel >= 2.0
BuildRequires:	gtest-devel >= 1.7.0
%{?with_java:BuildRequires:	jdk >= 1.5}
BuildRequires:	libstdc++-devel >= 6:4.5
BuildRequires:	libtool >= 2:1.5
BuildRequires:	minizip-devel >= 1.2.8
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	rpm-pythonprov
%{?with_java:BuildRequires:	rpm-javaprov}
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
BuildRequires:	swig >= 2.0
BuildRequires:	swig-python >= 2.0
BuildRequires:	uriparser-devel >= 0.7.5
BuildRequires:	zlib-devel >= 1.2.8
Requires:	expat >= 2.0
Requires:	minizip >= 1.2.8
Requires:	uriparser >= 0.7.5
Requires:	zlib >= 1.2.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libkml is Google's library for use with applications that want to
parse, generate and operate on KML. It is an implementation of the OGC
KML 2.2 standard.

It is written in C++ and bindings are available via SWIG to Java and
Python.

%description -l pl.UTF-8
libkml to biblioteka Google przeznaczona dla aplikacji mających
analizować, generować i operować na danych w formacie KML. Jest
implementacją standardu KML 2.2.

Biblioteka została napisana w C++, dostępne są oparte na SWIG-u
wiązania do Javy i Pythona.

%package devel
Summary:	Header files for KML libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek KML
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	expat-devel >= 2.0
Requires:	boost-devel >= 1.44.0
Requires:	libstdc++-devel >= 6:4.5
Requires:	minizip-devel >= 1.2.8
Requires:	uriparser-devel >= 0.7.5
Requires:	zlib-devel >= 1.2.8

%description devel
Header files for KML libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek KML.

%package static
Summary:	Static KML libraries
Summary(pl.UTF-8):	Statyczne biblioteki KML
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static KML libraries.

%description static -l pl.UTF-8
Statyczne biblioteki KML.

%package -n java-libkml
Summary:	Java bindings to KML libraries
Summary(pl.UTF-8):	Wiązania Javy do bibliotek KML
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}
Requires:	jpackage-utils

%description -n java-libkml
SWIG-based Java bindings to KML libraries.

%description -n java-libkml -l pl.UTF-8
Oparte na SWIG-u wiązania Javy do bibliotek KML.

%package -n python-libkml
Summary:	Python bindings to KML libraries
Summary(pl.UTF-8):	Wiązania Pythona do bibliotek KML
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-libs

%description -n python-libkml
SWIG-based Python bindings to KML libraries.

%description -n python-libkml -l pl.UTF-8
Oparte na SWIG-u wiązania Pythona do bibliotek KML.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1

%build
%if %{with static_libs}
install -d build-static
cd build-static
%cmake .. \
	-DBUILD_SHARED_LIBS=OFF \
	-DWITH_SWIG=OFF

%{__make}
cd ..
%endif

install -d build
cd build
%cmake .. \
	-DJNI_INSTALL_DIR=%{_libdir}/libkml \
	-DPYTHON_EXECUTABLE=%{__python} \
	-DWITH_JAVA=%{__true_false java} \
	-DWITH_PYTHON=ON \
	-DWITH_SWIG=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C build-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README.md
%attr(755,root,root) %{_libdir}/libkmlbase.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libkmlbase.so.1
%attr(755,root,root) %{_libdir}/libkmlconvenience.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libkmlconvenience.so.1
%attr(755,root,root) %{_libdir}/libkmldom.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libkmldom.so.1
%attr(755,root,root) %{_libdir}/libkmlengine.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libkmlengine.so.1
%attr(755,root,root) %{_libdir}/libkmlregionator.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libkmlregionator.so.1
%attr(755,root,root) %{_libdir}/libkmlxsd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libkmlxsd.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libkmlbase.so
%attr(755,root,root) %{_libdir}/libkmlconvenience.so
%attr(755,root,root) %{_libdir}/libkmldom.so
%attr(755,root,root) %{_libdir}/libkmlengine.so
%attr(755,root,root) %{_libdir}/libkmlregionator.so
%attr(755,root,root) %{_libdir}/libkmlxsd.so
%{_includedir}/kml
%{_pkgconfigdir}/libkml.pc
%{_libdir}/cmake/libkml

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libkmlbase.a
%{_libdir}/libkmlconvenience.a
%{_libdir}/libkmldom.a
%{_libdir}/libkmlengine.a
%{_libdir}/libkmlregionator.a
%{_libdir}/libkmlxsd.a
%endif

%if %{with java}
%files -n java-libkml
%defattr(644,root,root,755)
%dir %{_libdir}/libkml
%attr(755,root,root) %{_libdir}/libkml/libkmlbase_swig_java.so
%attr(755,root,root) %{_libdir}/libkml/libkmldom_swig_java.so
%attr(755,root,root) %{_libdir}/libkml/libkmlengine_swig_java.so
%{_javadir}/LibKML.jar
%endif

%files -n python-libkml
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_kmlbase.so
%attr(755,root,root) %{py_sitedir}/_kmldom.so
%attr(755,root,root) %{py_sitedir}/_kmlengine.so
%{py_sitedir}/kmlbase.py[co]
%{py_sitedir}/kmldom.py[co]
%{py_sitedir}/kmlengine.py[co]
