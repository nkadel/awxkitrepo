# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8}
%global python3_version 3.9
%global python3_pkgversion 39
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

%global pypi_name awxkit
%global srcname awxkit
%global pypi_version 21.8.0

Name: python-%{pypi_name}
Version: %{pypi_version}
Release:  0.2%{?dist}
Summary: awxkit
License: Apache

# whl files cannot use pypi_source
Source0: https://files.pythonhosted.org/packages/b1/e0/347277ec924c7bc3f6a2d6188c78a2a653838bfc4d4de9059cddc0d8c012/awxkit-%{version}-py3-none-any.whl

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

# Extracted from: METADATA
Requires: python%{python3_pkgversion}
Requires: python%{python3_pkgversion}-PyYAML
Requires: python%{python3_pkgversion}-requests
#Requires: python%{python3_pkgversion}-crypto
Requires: python%{python3_pkgversion}-cryptography
Requires: python%{python3_pkgversion}-jq
Requires: python%{python3_pkgversion}-websockets
Requires: python%{python3_pkgversion}-websocket-client >= 0.57.0

%description -n     python%{python3_pkgversion}-%{pypi_name}

%prep
%setup -c %{pypi_name}-%{pypi_version}

%build
cp %{SOURCE1} awx
cp %{SOURCE2} akit

%install
install -d %{buildroot}%{_bindir}
install awx %{buildroot}%{_bindir}/awx
install akit %{buildroot}%{_bindir}/akit
rm -f awx
rm -f akit

install -d %{buildroot}%{python3_sitelib}
cp -r * %{buildroot}%{python3_sitelib}/

%files -n python%{python3_pkgversion}-%{pypi_name}
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}.dist-info
%{_bindir}/awx
%{_bindir}/akit

%changelog
