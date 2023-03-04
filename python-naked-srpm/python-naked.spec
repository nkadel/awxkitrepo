# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8}
%global python3_version 3.9
%global python3_pkgversion 39
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

# Created by pyp2rpm-3.3.8
%global pypi_name naked
%global srcname Naked
%global pypi_version 0.1.32

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        0.1%{?dist}
Summary:        A command line application framework

License:        MIT
URL:            http://naked-py.com
Source0:        https://files.pythonhosted.org/packages/source/n/%{pypi_name}/%{srcname}-%{pypi_version}.tar.gz

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

BuildArch:  noarch

%description
Naked <>_ is a new Python command line application framework that is in
development. The current release is a stable, testing release.Updates Changes,
updates, and brief tutorials are available on the developer log < Guide The
quickstart guide is available at < It demonstrates how the available tools can
be incorporated into your development workflow, spanning the entire period from
an empty...

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        A command line application framework

#Requires:       python%{python3_pkgversion}-%{srcname}
Requires:       python%{python3_pkgversion}-pyyaml
Requires:       python%{python3_pkgversion}-requests
Requires:       python%{python3_pkgversion}-setuptools
%description -n python%{python3_pkgversion}-%{pypi_name}
Naked <>_ is a new Python command line application framework that is in
development. The current release is a stable, testing release.Updates Changes,
updates, and brief tutorials are available on the developer log < Guide The
quickstart guide is available at < It demonstrates how the available tools can
be incorporated into your development workflow, spanning the entire period from
an empty...


%prep
%autosetup -n %{srcname}-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build

%install
%{__python3} setup.py install --skip-build --root %{buildroot}

%files -n python%{python3_pkgversion}-%{pypi_name}
%doc docs/README.rst lib/%{srcname}/templates/readme_md_file.py
%{_bindir}/naked
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}-%{pypi_version}-py%{python3_version}.egg-info

%changelog
* Tue Nov 01 2022 Nico Kadel-Garcia <nkadel@gmail.com> - 0.1.31-1
- Initial package.
