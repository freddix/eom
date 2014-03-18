Summary:	MATE image viewer
Name:		eom
Version:	1.8.0
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz
# Source0-md5:	0e80c19eb58d337ff25a7492967d0e4a
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	exempi-devel
BuildRequires:	gettext-devel
BuildRequires:	mate-desktop-devel >= 1.8.0
BuildRequires:	intltool
BuildRequires:	lcms-devel
BuildRequires:	libexif-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libtool
BuildRequires:	pkg-config
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	hicolor-icon-theme
Provides:	mate-image-viewer = %{version}-%{release}
Obsoletes:	mate-image-viewer <= %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Eye of MATE is a tool for viewing/cataloging images.

%package devel
Summary:	Development files
Group:		Development/Libraries
Provides:	mate-image-viewer-devel = %{version}-%{release}
Obsoletes:	mate-image-viewer-devel <= %{version}-%{release}

%description devel
Eye of the MATE Development files.

%package apidocs
Summary:	Eye of the MATE API documentation
Group:		Documentation
Requires:	gtk-doc-common
Provides:	mate-image-viewer-apidocs = %{version}-%{release}
Obsoletes:	mate-image-viewer-apidocs <= %{version}-%{release}

%description apidocs
Eye of the MATE API documentation.

%prep
%setup -q

# kill mate-common deps
%{__sed} -i -e '/MATE_COMPILE_WARNINGS.*/d'	\
    -i -e '/MATE_MAINTAINER_MODE_DEFINES/d'	\
    -i -e '/MATE_COMMON_INIT/d'			\
    -i -e '/MATE_CXX_WARNINGS.*/d'		\
    -i -e '/MATE_DEBUG_CHECK/d' configure.ac

%build
%{__libtoolize}
%{__intltoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-python		\
	--disable-schemas-compile	\
	--disable-silent-rules		\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/eom.convert
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*/*/*.la
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw}

%find_lang eom --with-mate

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor
%update_gsettings_cache

%postun
%update_desktop_database
%update_icon_cache hicolor
%update_gsettings_cache

%files -f eom.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/eom
%dir %{_libdir}/eom
%dir %{_libdir}/eom/plugins
%attr(755,root,root) %{_libdir}/eom/plugins/*.so
%{_libdir}/eom/plugins/*-plugin
%{_datadir}/eom
%{_datadir}/glib-2.0/schemas/org.mate.eom.gschema.xml
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/apps/eom.*
%{_mandir}//man1/eom.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/eom-2.20
%{_pkgconfigdir}/*.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/eom

