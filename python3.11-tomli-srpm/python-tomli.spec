# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.11
%global python3_pkgversion 3.11
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

Name:           python-tomli
Version:        2.0.1
#Release:        5%%{?dist}
Release:        0.5%{?dist}
Summary:        A little TOML parser for Python

License:        MIT
URL:            https://pypi.org/project/tomli/
Source0:        https://github.com/hukkin/tomli/archive/%{version}/%{name}-%{version}.tar.gz

# Upstream tomli uses flit, but we want to use setuptools on RHEL 9.
# This a downstream-only setup.py manually created from pyproject.toml metadata.
# It contains a @@VERSION@@ placeholder.
Source1:        tomli-setup.py

BuildArch:      noarch
BuildRequires:  python%{python3_pkgversion}-devel

# The test suite uses the stdlib's unittest framework, but we use %%pytest
# as the test runner.
BuildRequires:  python%{python3_pkgversion}-pytest

%global _description %{expand:
Tomli is a Python library for parsing TOML.
Tomli is fully compatible with TOML v1.0.0.}


%description %_description

%package -n python%{python3_pkgversion}-tomli
Summary:        %{summary}

%description -n python%{python3_pkgversion}-tomli %_description


%prep
%autosetup -p1 -n tomli-%{version}
sed 's/@@VERSION@@/%{version}/' %{SOURCE1} > setup.py
rm pyproject.toml  # force the PEP 517 fallback build backend (setuptools)


%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files tomli


%check
%py3_check_import tomli
%pytest


%files -n python%{python3_pkgversion}-tomli -f %{pyproject_files}
%doc README.md
%doc CHANGELOG.md


%changelog
* Wed Mar 08 2023 Miro Hrončok <mhroncok@redhat.com> - 2.0.1-5
- Initial package for RHEL 9
- Resolves: rhbz#2175213
- Fedora+EPEL contributions by:
      Maxwell G <gotmax@e.email>
      Michel Alexandre Salim <salimma@fedoraproject.org>
      Miro Hrončok <miro@hroncok.cz>
      Petr Viktorin <pviktori@redhat.com>
