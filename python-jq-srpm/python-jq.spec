# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.11
%global python3_pkgversion 3.11
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

# Created by pyp2rpm-3.3.8
%global pypi_name jq
%global pypi_version 1.3.0

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        0.2%{?dist}
Summary:        jq is a lightweight and flexible JSON processor

License:        BSD 2-Clause
URL:            http://github.com/mwilliamson/jq.py
Source0:        https://files.pythonhosted.org/packages/source/j/%{pypi_name}/%{pypi_name}-%{pypi_version}.tar.gz

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-rpm-macros

BuildRequires:  gcc
BuildRequires:  gcc-c++

%description
jq.py: a lightweight and flexible JSON processor This project contains Python
bindings for jq < Wheels are built for various Python versions and
architectures on Linux and Mac OS X. On these platforms, you should be able to
install jq with a normal pip install:.. code-block:: sh pip install jqIf a
wheel is not available, the source for jq 1.6 is downloaded over HTTPS and
built. This requires:*...

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        jq is a lightweight and flexible JSON processor

%description -n python%{python3_pkgversion}-%{pypi_name}
jq.py: a lightweight and flexible JSON processor This project contains Python
bindings for jq < Wheels are built for various Python versions and
architectures on Linux and Mac OS X. On these platforms, you should be able to
install jq with a normal pip install:.. code-block:: sh pip install jqIf a
wheel is not available, the source for jq 1.6 is downloaded over HTTPS and
built. This requires:*...


%prep
%autosetup -n %{pypi_name}-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build

%install
%{__python3} setup.py install --skip-build --root %{buildroot}

%files -n python%{python3_pkgversion}-%{pypi_name}
%doc README.rst
%{python3_sitearch}/%{pypi_name}.cpython-*
%{python3_sitearch}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info
#%{python3_sitearch}/%{pypi_name}


%changelog
* Tue Nov 01 2022 Nico Kadel-Garcia <nkadel@gmail.com> - 1.3.0-1
- Initial package.
