# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8}
%global python3_version 3.9
%global python3_pkgversion 39
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

# Created by pyp2rpm-3.3.8
%global pypi_name websocket
%global pypi_version 0.2.1

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        0.1%{?dist}
Summary:        Websocket implementation for gevent

License:        None
URL:            http://pypi.python.org/pypi/websocket
Source0:        https://files.pythonhosted.org/packages/source/w/%{pypi_name}/%{pypi_name}-%{pypi_version}.tar.gz
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%description
UNKNOWN

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        Websocket implementation for gevent

Requires:       python%{python3_pkgversion}-gevent
Requires:       python%{python3_pkgversion}-greenlet
%description -n python%{python3_pkgversion}-%{pypi_name}
UNKNOWN


%prep
%autosetup -n %{pypi_name}-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%{__python3} setup.py build

%install
# Must do the default python version install last because
# the scripts in /usr/bin are overwritten with every setup.py install.
%{__python3} setup.py install --skip-build --root %{buildroot}

%files -n python%{python3_pkgversion}-%{pypi_name}
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%changelog
* Tue Nov 01 2022 Nico Kadel-Garcia <nkadel@gmail.com> - 0.2.1-1
- Initial package.
