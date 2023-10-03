# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.11
%global python3_pkgversion 3.11
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

%global pypi_name awxkit
%global srcname awxkit
%global pypi_version 23.2.0

Name: python-%{pypi_name}
Version: %{pypi_version}
Release:  0.2%{?dist}
Summary: awxkit
License: Apache

# whl files cannot use pypi_source
Source:https://files.pythonhosted.org/packages/58/7d/3c1520db1f462f10e0f248e694a8be07ece9f820576a45556c5e3cae8f61/awxkit-23.2.0-py3-none-any.whl

# Scripts normally built by wheel installer
# python version set by RPM python processing
Source1: awx.bin
Source2: akit.bin

BuildArch: noarch

%description

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

%description -n     python%{python3_pkgversion}-%{pypi_name}

%prep
%setup -c %{pypi_name}-%{pypi_version}

%build
%install
install -d %{buildroot}%{_bindir}

install %{SOURCE1} ./awx
install %{SOURCE2} ./akit

sed -i.bak 's|^#!/usr/bin/env python3.*|#!%{__python3}|g' awx
sed -i.bak 's|^#!/usr/bin/env python3.*|#!%{__python3}|g' akit

install awx %{buildroot}%{_bindir}/awx
install akit %{buildroot}%{_bindir}/akit

rm -f awx awx.bak
rm -f akit akit.bak

install -d %{buildroot}%{python3_sitelib}
cp -r * %{buildroot}%{python3_sitelib}/

%files -n python%{python3_pkgversion}-%{pypi_name}
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{pypi_version}.dist-info
%{_bindir}/awx
%{_bindir}/akit
%doc awxkit/cli/docs/README.md
%doc awxkit/cli/docs/source/*.rst

%changelog
* Mon May 15 2023 Nico Kadel-Garcia - 22.2.0-0.1
- Update to 22.2.0
