Name:           snappy
Version:        1.1.8
Release:        3%{?dist}
Summary:        Fast compression and decompression library

Group:          System Environment/Libraries
License:        BSD
URL:            https://github.com/google/snappy
Source0:        https://github.com/google/snappy/archive/%{version}.tar.gz

# add missing dependency on gtest to snappy_unittest
Patch0:         %{name}-gtest.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  gtest-devel

%description
Snappy is a compression/decompression library. It does not aim for maximum 
compression, or compatibility with any other compression library; instead, it 
aims for very high speeds and reasonable compression. For instance, compared to 
the fastest mode of zlib, Snappy is an order of magnitude faster for most 
inputs, but the resulting compressed files are anywhere from 20% to 100% 
bigger. 


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       cmake-filesystem
Requires:       pkgconfig
Obsoletes:      %{name}-devel < %{version}-2

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1

%build
%cmake .
%make_build

# create pkgconfig file
cat << EOF >snappy.pc
prefix=%{_prefix}
exec_prefix=%{_exec_prefix}
includedir=%{_includedir}
libdir=%{_libdir}

Name: %{name}
Description: A fast compression/decompression library
Version: %{version}
Cflags: -I\${includedir}
Libs: -L\${libdir} -lsnappy
EOF


%install
rm -rf %{buildroot}
chmod 644 *.txt AUTHORS COPYING NEWS README.md
%make_install
install -m644 -D snappy.pc %{buildroot}%{_libdir}/pkgconfig/snappy.pc
# Address multilib failures while moving files from _libdir to
# _datadir
%ifarch x86_64 s390x ppc64 ppc64le aarch64
mkdir -p %{buildroot}%{_datadir}/cmake/Modules/lib64/
mv %{buildroot}%{_libdir}/cmake/Snappy/*cmake %{buildroot}%{_datadir}/cmake/Modules/lib64/
%else
mkdir -p %{buildroot}%{_datadir}/cmake/Modules/lib/
mv %{buildroot}%{_libdir}/cmake/Snappy/*cmake %{buildroot}%{_datadir}/cmake/Modules/lib/
%endif
rm -rf %{buildroot}%{_datadir}/doc/snappy/
rm -rf %{buildroot}%{_datadir}/doc/snappy-devel/

%check
ctest -V %{?_smp_mflags}


%ldconfig_scriptlets


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README.md
%{_libdir}/libsnappy.so.*

%files devel
%defattr(-,root,root,-)
%doc format_description.txt framing_format.txt
%{_includedir}/snappy*.h
%{_libdir}/libsnappy.so
%{_libdir}/pkgconfig/snappy.pc
%ifarch x86_64 s390x ppc64 ppc64le aarch64
%{_datadir}/cmake/Modules/lib64/*.cmake
%else
%{_datadir}/cmake/Modules/lib/*.cmake
%endif


%changelog
* Fri Aug 21 2020 Bhupesh Sharma <bhsharma@redhat.com> - 1.1.8-3
- Obsolete snappy-devel versions lower than 1.1.8-2 as lower versions have multilib issues.

* Fri Jul 24 2020 Bhupesh Sharma <bhsharma@redhat.com> - 1.1.8-2
- Fix multilib (i686 and x86) issues with snappy-devel package

* Wed Jul 22 2020 Bhupesh Sharma <bhsharma@redhat.com> - 1.1.8-1
- Rebase to latest github version Snappy-1.1.8
- Also change the URL to reflect to the updated github location.

* Mon Feb 19 2018 Martin Gieseking <martin.gieseking@uos.de> - 1.1.7-5
- Added BR: gcc-c++ according to new packaging guidelines.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.1.7-3
- Switch to %%ldconfig_scriptlets

* Wed Dec 20 2017 Martin Gieseking <martin.gieseking@uos.de> - 1.1.7-2
- Fixed https://bugzilla.redhat.com/show_bug.cgi?id=1527850

* Fri Aug 25 2017 Martin Gieseking <martin.gieseking@uos.de> - 1.1.7-1
- Updated to new release.
- Build with CMake since autotool support is deprecated.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 28 2017 Martin Gieseking <martin.gieseking@uos.de> - 1.1.4-2
- Rebuilt with https://github.com/google/snappy/archive/1.1.4.tar.gz since
  %%{source0} contains different and buggy code.
  https://groups.google.com/forum/#!topic/snappy-compression/uhELq553TrI

* Sat Jan 28 2017 Martin Gieseking <martin.gieseking@uos.de> - 1.1.4-1
- Updated to new release.
- Added pkgconfig file now coming with the sources.

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 14 2015 Martin Gieseking <martin.gieseking@uos.de> 1.1.3-1
- Updated to new release.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.1.1-5
- Rebuilt for GCC 5 C++11 ABI change

* Wed Feb 25 2015 Martin Gieseking <martin.gieseking@uos.de> 1.1.1-4
- Rebuilt for new GCC 5.0 ABI.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 24 2014 Martin Gieseking <martin.gieseking@uos.de> 1.1.1-1
- Updated to new release.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 06 2013 Martin Gieseking <martin.gieseking@uos.de> 1.1.0-1
- updated to new release

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 24 2012 Martin Gieseking <martin.gieseking@uos.de> 1.0.5-1
- updated to release 1.0.5
- made dependency of devel package on base package arch dependant

* Tue Jan 17 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.0.4-3
- Add in buildroot stuff for EL5 build

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 16 2011 Martin Gieseking <martin.gieseking@uos.de> 1.0.4-1
- updated to release 1.0.4

* Sat Jun 04 2011 Martin Gieseking <martin.gieseking@uos.de> 1.0.3-1
- updated to release 1.0.3
- added format description to devel package

* Fri Apr 29 2011 Martin Gieseking <martin.gieseking@uos.de> 1.0.2-1
- updated to release 1.0.2
- changed License to BSD
- dropped the patch as it has been applied upstream

* Thu Mar 24 2011 Martin Gieseking <martin.gieseking@uos.de> 1.0.0-3
- added file COPYING from the upstream repo

* Thu Mar 24 2011 Martin Gieseking <martin.gieseking@uos.de> 1.0.0-2
- replaced $CXXFLAGS with %%{optflags} in %%build section
- removed empty %%doc entry from %%files devel

* Thu Mar 24 2011 Martin Gieseking <martin.gieseking@uos.de> 1.0.0-1
- initial package

