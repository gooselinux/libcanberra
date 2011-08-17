Name: libcanberra
Version: 0.22
Release: 1%{?dist}
Summary: Portable Sound Event Library
Group: System Environment/Libraries
Source0: http://0pointer.de/lennart/projects/libcanberra/libcanberra-%{version}.tar.gz
License: LGPLv2+
Url: http://git.0pointer.de/?p=libcanberra.git;a=summary
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gtk2-devel
BuildRequires: alsa-lib-devel
BuildRequires: libvorbis-devel
BuildRequires: libtool-ltdl-devel
BuildRequires: gtk-doc
BuildRequires: pulseaudio-libs-devel >= 0.9.15
BuildRequires: gstreamer-devel
BuildRequires: libtdb-devel
BuildRequires: GConf2-devel
BuildRequires: gettext-devel
Requires: sound-theme-freedesktop
Requires: pulseaudio-libs >= 0.9.15

%description
A small and lightweight implementation of the XDG Sound Theme Specification
(http://0pointer.de/public/sound-theme-spec.html).

%package gtk2
Summary: Gtk+ Bindings for libcanberra
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires(pre): GConf2
Requires(preun): GConf2
Requires(post): GConf2

%description gtk2
Gtk+ bindings for libcanberra

%package devel
Summary: Development Files for libcanberra Client Development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
Requires: gtk-doc
Requires: gtk2-devel

%description devel
Development Files for libcanberra Client Development

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post gtk2
/sbin/ldconfig
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/libcanberra.schemas > /dev/null || :

%postun gtk2 -p /sbin/ldconfig

%pre gtk2
if [ "$1" -gt 1 ]; then
	export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
	gconftool-2 --makefile-install-rule \
		%{_sysconfdir}/gconf/schemas/libcanberra.schemas >& /dev/null || :
fi

%preun gtk2
if [ "$1" -eq 0 ]; then
	export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
	gconftool-2 --makefile-uninstall-rule \
      		%{_sysconfdir}/gconf/schemas/libcanberra.schemas >& /dev/null || :
fi

%prep
%setup -q

%build
%configure --disable-static --enable-pulse --enable-alsa --enable-null --enable-gstreamer --disable-oss --with-builtin=dso
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT \( -name *.a -o -name *.la \) -exec rm {} \;
rm $RPM_BUILD_ROOT%{_docdir}/libcanberra/README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README LGPL
%{_libdir}/libcanberra.so.*
%dir %{_libdir}/libcanberra-%{version}
%{_libdir}/libcanberra-%{version}/libcanberra-alsa.so
%{_libdir}/libcanberra-%{version}/libcanberra-pulse.so
%{_libdir}/libcanberra-%{version}/libcanberra-null.so
%{_libdir}/libcanberra-%{version}/libcanberra-multi.so
%{_libdir}/libcanberra-%{version}/libcanberra-gstreamer.so

%files gtk2
%defattr(-,root,root)
%{_libdir}/libcanberra-gtk.so.*
%{_libdir}/gtk-2.0/modules/libcanberra-gtk-module.so
%{_bindir}/canberra-gtk-play
%{_datadir}/gnome/autostart/libcanberra-login-sound.desktop
%{_datadir}/gnome/shutdown/libcanberra-logout-sound.sh
# co-own these directories to avoid requiring GDM (#522998)
%dir %{_datadir}/gdm/
%dir %{_datadir}/gdm/autostart/
%dir %{_datadir}/gdm/autostart/LoginWindow/
%{_datadir}/gdm/autostart/LoginWindow/libcanberra-ready-sound.desktop
%{_sysconfdir}/gconf/schemas/libcanberra.schemas

%files devel
%defattr(-,root,root)
%doc %{_datadir}/gtk-doc/html/libcanberra
%{_includedir}/canberra-gtk.h
%{_includedir}/canberra.h
%{_libdir}/libcanberra-gtk.so
%{_libdir}/libcanberra.so
%{_libdir}/pkgconfig/libcanberra-gtk.pc
%{_libdir}/pkgconfig/libcanberra.pc
# co-own these directories to avoid requiring vala
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/libcanberra-gtk.vapi
%{_datadir}/vala/vapi/libcanberra.vapi

%changelog
* Tue Oct 20 2009 Lennart Poettering <lpoetter@redhat.com> 0.22-1
- New version 0.22

* Fri Oct 16 2009 Lennart Poettering <lpoetter@redhat.com> 0.21-1
- New version 0.21

* Thu Oct 15 2009 Lennart Poettering <lpoetter@redhat.com> 0.20-1
- New version 0.20

* Wed Oct 14 2009 Lennart Poettering <lpoetter@redhat.com> 0.19-1
- New version 0.19

* Fri Sep 25 2009 Matthias Clasen <mclasen@redhat.com> - 0.18-2
- Don't require vala in -devel (#523473)

* Sat Sep 19 2009 Lennart Poettering <lpoetter@redhat.com> 0.18-1
- New version 0.18

* Wed Sep 16 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.17-2
- Don't require gdm in -gtk2 (#522998)

* Fri Sep 12 2009 Lennart Poettering <lpoetter@redhat.com> 0.17-1
- New version 0.17

* Thu Aug 27 2009 Lennart Poettering <lpoetter@redhat.com> 0.16-1
- New version 0.16

* Wed Aug 5 2009 Lennart Poettering <lpoetter@redhat.com> 0.15-2
- Fix mistag

* Wed Aug 5 2009 Lennart Poettering <lpoetter@redhat.com> 0.15-1
- New version 0.15

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 2 2009 Lennart Poettering <lpoetter@redhat.com> 0.14-2
- Upload the right tarball

* Thu Jul 2 2009 Lennart Poettering <lpoetter@redhat.com> 0.14-1
- New version 0.14

* Tue Jun 23 2009 Lennart Poettering <lpoetter@redhat.com> 0.13-1
- New version 0.13

* Tue Jun 16 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.12-2
- Rebuild for new libtdb.

* Mon Apr 13 2009 Lennart Poettering <lpoetter@redhat.com> 0.12-1
- New version 0.12

* Wed Apr 1 2009 Lennart Poettering <lpoetter@redhat.com> 0.11-9
- Another preview for 0.12

* Wed Feb 25 2009 Lennart Poettering <lpoetter@redhat.com> 0.11-8
- Add missing dependency on gettext-devel

* Wed Feb 25 2009 Lennart Poettering <lpoetter@redhat.com> 0.11-7
- Preview for 0.12

* Thu Feb  5 2009 Matthias Clasen  <mclasen@redhat.com> 0.11-6
- Fix up Requires (#484225)

* Wed Jan 21 2009 Lennart Poettering <lpoetter@redhat.com> 0.11-5
- New version

* Sun Dec 14 2008 Lennart Poettering <lpoetter@redhat.com> 0.10-4
- Moved login sound to "Application" startup phase.

* Thu Nov 13 2008 Matthias Clasen <mclasen@redhat.com> 0.10-3
- Rebuild

* Fri Oct 10 2008 Lennart Poettering <lpoetter@redhat.com> 0.10-2
- Drop libcanberra-gtk-module.sh since the gconf stuff is supported just fine in current gnome-session already.

* Mon Oct 6 2008 Lennart Poettering <lpoetter@redhat.com> 0.10-1
- New version

* Thu Sep 9 2008 Lennart Poettering <lpoetter@redhat.com> 0.9-1
- New version

* Thu Aug 28 2008 Lennart Poettering <lpoetter@redhat.com> 0.8-2
- Fix build-time dep on Gstreamer

* Thu Aug 28 2008 Lennart Poettering <lpoetter@redhat.com> 0.8-1
- New version

* Thu Aug 14 2008 Lennart Poettering <lpoetter@redhat.com> 0.7-1
- New version

* Mon Aug 4 2008 Lennart Poettering <lpoetter@redhat.com> 0.6-1
- New version

* Wed Jul 30 2008 Lennart Poettering <lpoetter@redhat.com> 0.5-4
- Really add versioned dependency on libpulse

* Wed Jul 30 2008 Lennart Poettering <lpoetter@redhat.com> 0.5-3
- Ship libcanberra-gtk-module.sh directly in CVS

* Wed Jul 30 2008 Lennart Poettering <lpoetter@redhat.com> 0.5-2
- Fix build

* Wed Jul 30 2008 Lennart Poettering <lpoetter@redhat.com> 0.5-1
- New version

* Mon Jul 28 2008 Lennart Poettering <lpoetter@redhat.com> 0.4-3
- Add versioned dependency on libpulse

* Sun Jul 27 2008 Lennart Poettering <lpoetter@redhat.com> 0.4-2
- Fix module name in libcanberra-gtk-module.sh

* Fri Jul 25 2008 Lennart Poettering <lpoetter@redhat.com> 0.4-1
- New version
- Install libcanberra-gtk-module.sh

* Mon Jun 16 2008 Lennart Poettering <lpoetter@redhat.com> 0.3-2
- Add dependency on sound-theme-freedesktop

* Fri Jun 13 2008 Lennart Poettering <lpoetter@redhat.com> 0.3-1
- Initial package, based on Colin Guthrie's Mandriva package

