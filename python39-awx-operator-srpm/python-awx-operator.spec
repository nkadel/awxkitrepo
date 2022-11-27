# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8}
%global python3_version 3.9
%global python3_pkgversion 39
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

%global pypi_name awx-operator
%global srcname awx-operator
%global pypi_version 1.0.0

Name: python-%{pypi_name}
Version: %{pypi_version}
Release:  0.2%{?dist}
Summary: awx-operator
License: Apache

# whl files cannot use pypi_source
Source0: https://github.com/ansible/awx-operator/archive/refs/tags/%{version}.zip

# Scripts normally built by wheel installer
# python version set by RPM python processing
#Source1: awx.bin
#Source2: akit.bin

BuildArch: noarch

%description

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary: awx-operator

# Added for setup requirements
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

# Extracted from: METADATA
Requires: python%{python3_pkgversion}
Requires: python%{python3_pkgversion}-PyYAML
Requires: python%{python3_pkgversion}-requests
#Requires: python%{python3_pkgversion}-crypto
Requires: python%{python3_pkgversion}-cryptography
Requires: python%{python3_pkgversion}-jq
Requires: python%{python3_pkgversion}-websockets
Requires: python%{python3_pkgversion}-websocket-client >= 0.57.0

Provides: awx-operator = %{version}-%{release}

%description -n     python%{python3_pkgversion}-%{pypi_name}

%prep
%setup -n %{pypi_name}-%{pypi_version}

%build
%install
#install -d %{buildroot}%{_bindir}
#install %{SOURCE1} %{buildroot}%{_bindir}/awx
#install %{SOURCE2} %{buildroot}%{_bindir}/akit

install -d %{buildroot}%{python3_sitelib}/%{pypi_name}
cp -r * %{buildroot}%{python3_sitelib}/%{pypi_name}

%files -n python%{python3_pkgversion}-%{pypi_name}
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}.dist-info

%changelog
