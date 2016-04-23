#
# Conditional build:
%bcond_without	java		# Java binding
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Library to parse, generate and operate on KML
Summary(pl.UTF-8):	Biblioteka do analizy, generowania i operowania na danych KML
Name:		libkml
Version:	1.2.0
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/google/libkml/releases
#Source0:	https://github.com/google/libkml/archive/release-1.2/%{name}-%{version}.tar.gz
Source0:	http://libkml.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	25d534437f971bf55a945608e39fea79
Patch0:		%{name}-sh.patch
Patch1:		%{name}-system-libs.patch
Patch2:		%{name}-link.patch
Patch3:		%{name}-include.patch
URL:		https://github.com/google/libkml
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9.6
BuildRequires:	boost-devel >= 1.34.0
BuildRequires:	curl-devel >= 7.12.3
BuildRequires:	expat-devel >= 2.0
BuildRequires:	gtest-devel
%{?with_java:BuildRequires:	jdk >= 1.5}
BuildRequires:	libstdc++-devel >= 6:4.0
BuildRequires:	libtool >= 2:1.5
BuildRequires:	python-devel >= 2.3
BuildRequires:	rpm-pythonprov
%{?with_java:BuildRequires:	rpm-javaprov}
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
BuildRequires:	swig >= 1.3.35
BuildRequires:	swig-python >= 1.3.35
BuildRequires:	uriparser-devel >= 0.7.5
BuildRequires:	zlib-devel >= 1.2.3
Requires:	expat >= 2.0
Requires:	uriparser >= 0.7.5
Requires:	zlib >= 1.2.3
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
Requires:	boost-devel >= 1.34.0
Requires:	libstdc++-devel >= 6:4.0
Requires:	uriparser-devel >= 0.7.5
Requires:	zlib-devel >= 1.2.3

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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# error: ISO C++ 1998 does not support 'long long'
%{__sed} -i -e 's/ -Werror//' configure.ac $(find . -name Makefile.am | xargs grep -l -e '-Werror')

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_java:--disable-java} \
	%{?with_java:--with-java-include-dir=%{_jvmdir}/java/include} \
	%{?with_java:--with-java-lib-dir=%{_jvmdir}/java/lib} \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with java}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libkml/libkml*_swig_java.*a
%endif

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libkml/libkml*_swig_python.*

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README
%attr(755,root,root) %{_libdir}/libkmlbase.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libkmlbase.so.0
%attr(755,root,root) %{_libdir}/libkmlconvenience.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libkmlconvenience.so.0
%attr(755,root,root) %{_libdir}/libkmldom.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libkmldom.so.0
%attr(755,root,root) %{_libdir}/libkmlengine.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libkmlengine.so.0
%attr(755,root,root) %{_libdir}/libkmlminizip.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libkmlminizip.so.0
%attr(755,root,root) %{_libdir}/libkmlregionator.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libkmlregionator.so.0
%attr(755,root,root) %{_libdir}/libkmlxsd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libkmlxsd.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libkmlbase.so
%attr(755,root,root) %{_libdir}/libkmlconvenience.so
%attr(755,root,root) %{_libdir}/libkmldom.so
%attr(755,root,root) %{_libdir}/libkmlengine.so
%attr(755,root,root) %{_libdir}/libkmlminizip.so
%attr(755,root,root) %{_libdir}/libkmlregionator.so
%attr(755,root,root) %{_libdir}/libkmlxsd.so
%{_libdir}/libkmlbase.la
%{_libdir}/libkmlconvenience.la
%{_libdir}/libkmldom.la
%{_libdir}/libkmlengine.la
%{_libdir}/libkmlminizip.la
%{_libdir}/libkmlregionator.la
%{_libdir}/libkmlxsd.la
%{_includedir}/kml

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libkmlbase.a
%{_libdir}/libkmlconvenience.a
%{_libdir}/libkmldom.a
%{_libdir}/libkmlengine.a
%{_libdir}/libkmlminizip.a
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
