# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.11
%global python3_pkgversion 3.11
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

# Created by pyp2rpm-3.3.8
%global pypi_name crypto
%global pypi_version 1.4.1

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        0.2%{?dist}
Summary:        Simple symmetric GPG file encryption and decryption

License:        MIT license
URL:            https://github.com/chrissimpkins/crypto
Source0:        https://files.pythonhosted.org/packages/source/c/%{pypi_name}/%{pypi_name}-%{pypi_version}.tar.gz
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-rpm-macros

%description
Documentation: -crypto provides a simple interface to symmetric Gnu Privacy
Guard (gpg) encryption and decryption for one or more files on Unix and Linux
platforms. It runs on top of gpg and requires a gpg install on your system.
Encryption is performed with the AES256 cipher algorithm. Benchmarks relative
to default gpg settings are available for text and binary file mime types <
provides a...

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        Simple symmetric GPG file encryption and decryption

#Requires:       python%{python3_pkgversion}-Naked
Requires:       python%{python3_pkgversion}-naked
Requires:       python%{python3_pkgversion}-setuptools
Requires:       python%{python3_pkgversion}-shellescape
%description -n python%{python3_pkgversion}-%{pypi_name}
Documentation: -crypto provides a simple interface to symmetric Gnu Privacy
Guard (gpg) encryption and decryption for one or more files on Unix and Linux
platforms. It runs on top of gpg and requires a gpg install on your system.
Encryption is performed with the AES256 cipher algorithm. Benchmarks relative
to default gpg settings are available for text and binary file mime types <
provides a...


%prep
%autosetup -n %{pypi_name}-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}/%{_bindir}/crypto %{buildroot}/%{_bindir}/crypto%{python3_pkgversion}
mv %{buildroot}/%{_bindir}/decrypto %{buildroot}/%{_bindir}/decrypto%{python3_pkgversion}


%files -n python%{python3_pkgversion}-%{pypi_name}
%doc docs/README.rst
%{_bindir}/crypto%{python3_pkgversion}
%{_bindir}/decrypto%{python3_pkgversion}
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%changelog
* Tue Nov 01 2022 Nico Kadel-Garcia <nkadel@gmail.com> - 1.4.1-1
- Initial package.
