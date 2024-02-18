# Force python3.111 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.11
%global python3_pkgversion 3.11
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

%global pypi_name awxkit
%global srcname awxkit
%global pypi_version 23.8.1

Name: %{pypi_name}
Version: %{pypi_version}
Release:  0.2%{?dist}
Summary: A Python library that backs the provided `awx` command line client.
License: Apache

# whl files cannot use pypi_source
#Source: https://files.pythonhosted.org/packages/67/31/ce5934908197f6f6fe63cf678c027cc19309ed216d097e19c6042cb22507/awxkit-23.6.0-py3-none-any.whl
Source: %{pypi_source}

BuildArch: noarch

%description
A Python library that backs the provided `awx` command line client.

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary: awxkit

# Added for setup requirements
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-rpm-macros

# Extracted from: METADATA
Requires: python%{python3_pkgversion}
Requires: python%{python3_pkgversion}-PyYAML
Requires: python%{python3_pkgversion}-requests
#Requires: python%{python3_pkgversion}-crypto
Requires: python%{python3_pkgversion}-cryptography
Requires: python%{python3_pkgversion}-jq
Requires: python%{python3_pkgversion}-websockets
Requires: python%{python3_pkgversion}-websocket-client >= 0.57.0

Provides: awxkit = %{pypi_version}-%{release}
Provides: awx-cli = %{pypi_version}-%{release}
Provides: akit = %{pypi_version}-%{release}

%description -n python%{python3_pkgversion}-%{pypi_name}

%prep
%setup -n %{pypi_name}-%{pypi_version}

%build
%{py3_build}

%install
%{py3_install}

%files -n python%{python3_pkgversion}-%{pypi_name}
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-*.egg-info
%{_bindir}/awx
%{_bindir}/akit
%doc README.md
%doc awxkit/cli/docs/source/*.rst

%changelog
* Sat Feb 18 2024 Nico Kadel-Garcia - 23.8.1-0.1
- Use py3_build and py3_install

* Wed Nov 29 2023 Nico Kadel-Garcia - 25.5.0-0.1
- Updddddateee to 23.5.0

* Mon May 15 2023 Nico Kadel-Garcia - 22.2.0-0.1
- Update to 22.2.0
