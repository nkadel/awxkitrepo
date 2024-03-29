# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.11
%global python3_pkgversion 3.11
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

%bcond_without python3

# what it's called on pypi
%global pypi_name websocket-client
# what it's imported as
%global libname websocket
# name of egg info directory
%global eggname websocket_client

%global common_description %{expand:
python-websocket-client module is WebSocket client for python. This provides
the low level APIs for WebSocket. All APIs are the synchronous functions.

python-websocket-client supports only hybi-13.}

Name:               python-%{pypi_name}
Version:            1.4.2
Release:            0.2%{?dist}
Summary:            WebSocket client for python
License:            BSD
URL:                https://github.com/websocket-client/websocket-client
Source0:            %pypi_source
BuildArch:          noarch


%description %{common_description}


%if %{with python3}
%package -n python%{python3_pkgversion}-%{pypi_name}
Summary:            %{summary}
BuildRequires:      python%{python3_pkgversion}-devel
BuildRequires:      python%{python3_pkgversion}-setuptools
BuildRequires:      python%{python3_pkgversion}-six
BuildRequires:      python%{python3_pkgversion}-websockets
BuildRequires:      python%{python3_pkgversion}-rpm-macros
Requires:           python%{python3_pkgversion}-six
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

# https://fedoraproject.org/wiki/Packaging:Conflicts#Splitting_Packages
# wsdump moved from py2 to py3 package
Conflicts:          python2-websocket-client <= 0.40.0-4

%if 0%{?el8} || 0%{?el9}
Conflicts:          python3-websocket-client
%endif

%description -n python%{python3_pkgversion}-%{pypi_name} %{common_description}
%endif # with python3


%prep
%setup -q -n %{pypi_name}-%{version}

rm -r %{eggname}.egg-info


%build

%if %{with python3}
%py3_build
%endif # with python3


%install
%if %{with python3}
%py3_install
%endif # with python3

# https://fedoraproject.org/wiki/Packaging:Python#Executables_in_.2Fusr.2Fbin
# wsdump has the same functionality on py2 and py3, so only ship one version
mv %{buildroot}%{_bindir}/wsdump %{buildroot}%{_bindir}/wsdump%{python3_version}
ln -s wsdump%{python3_version} %{buildroot}%{_bindir}/wsdump

# setup.py test does not work in mock
#%%check
#%%if %%{with python3}
#%%{__python3} setup.py test
#%%endif # with python3

%if %{with python3}
%files -n python%{python3_pkgversion}-%{pypi_name}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{libname}
%exclude %{python3_sitelib}/%{libname}/tests
%{python3_sitelib}/%{eggname}-%{version}-py%{python3_version}.egg-info
%{_bindir}/wsdump
%{_bindir}/wsdump%{python3_version}
%endif # with python3

%changelog
* Thu Dec 1 2022 Nico Kadel-Garcia <nkadel@gmail.com> - 1.4.2
- Update to 1.4.2
- Use python 3.9 on RHEL 8

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.56.0-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 0.56.0-4
- Rebuilt for Python 3.8

* Wed Aug 07 2019 Carl George <carl@george.computer> - 0.56.0-3
- Disable python2 subpackage on F31+ rhbz#1738467

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.56.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 10 2019 Carl George <carl@george.computer> - 0.56.0-1
- Latest upstream

* Tue Feb 12 2019 Yatin Karel <ykarel@redhat.com> - 0.54.0-1
- Update to 0.54.0
- Change license to BSD as source has changed it.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.53.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Oct 28 2018 Peter Robinson <pbrobinson@fedoraproject.org> 0.53.0-1
- Update to 0.53.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.47.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 0.47.0-3
- Rebuilt for Python 3.7

* Tue Mar 27 2018 Charalampos Stratakis <cstratak@redhat.com> - 0.47.0-2
- Conditionalize the Python 2 subpackage
- Don't build the Python 2 subpackage on EL > 7

* Mon Mar 26 2018 Jan Beran <jberan@redhat.com> - 0.47.0-1
- Latest upstream (rhbz# 1548228)
- Fixes python3-websocket-client requires both Python 2 and 3 (rhbz# 1531541)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.46.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 02 2018 Carl George <carl@george.computer> - 0.46.0-1
- Latest upstream rhbz#1462523
- Only ship one version of wsdump
- Properly install LICENSE file
- Remove tests from buildroot
- Use Python build, install, and provides macros

* Sun Dec 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.40.0-4
- Python 2 binary package renamed to python2-websocket-client
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 0.40.0-3
- Cleanup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 27 2017 Ralph Bean <rbean@redhat.com> - 0.40.0-1
- new version

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.37.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.37.0-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Apr 14 2016 Ralph Bean <rbean@redhat.com> - 0.37.0-1
- new version

* Mon Apr 04 2016 Ralph Bean <rbean@redhat.com> - 0.35.0-1
- new version

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.34.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Oct 28 2015 Ralph Bean <rbean@redhat.com> - 0.34.0-1
- new version

* Tue Oct 27 2015 Ralph Bean <rbean@redhat.com> - 0.33.0-1
- new version

* Mon Jul 27 2015 Ralph Bean <rbean@redhat.com> - 0.32.0-1
- new version

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu May 22 2014 Ralph Bean <rbean@redhat.com> - 0.14.1-1
- Latest upstream with python3 support.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 10 2013 Ralph Bean <rbean@redhat.com> - 0.10.0-1
- Latest upstream release.
- Removed executable bit from installed lib files for rpmlint.

* Wed Feb 27 2013 Ralph Bean <rbean@redhat.com> - 0.9.0-2
- Replaced websocket_client with %%{eggname} as per review by Palle Ravn
  https://bugzilla.redhat.com/show_bug.cgi?id=909644#c4
- Removed a few unnecessary newlines.

* Wed Feb 27 2013 Ralph Bean <rbean@redhat.com> - 0.9.0-1
- Latest upstream.

* Sat Feb 09 2013 Ralph Bean <rbean@redhat.com> - 0.8.0-1
- Initial package for Fedora
