# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.11
%global python3_pkgversion 3.11
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

# Created by pyp2rpm-3.3.8
%global pypi_name websockets
%global srcname websockets
%global pypi_version 10.4

# Avoid errors about missing debugsourcfiles.list
%define debug_package %{nil}

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        0.2%{?dist}
Summary:        An implementation of the WebSocket Protocol (RFC 6455 & 7692)

License:        BSD
URL:            https://github.com/aaugustin/websockets
Source0:        %{pypi_source}

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-rpm-macros
#BuildRequires:  python%{python3_pkgversion}-sphinx
BuildRequires:  python3-sphinx

%description
websockets is a library for building WebSocket_ servers and clients in Python
with a focus on correctness, simplicity, robustness, and performance.

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        An implementation of the WebSocket Protocol (RFC 6455 & 7692)

%description -n python%{python3_pkgversion}-%{pypi_name}
websockets is a library for building WebSocket_ servers and clients in Python
with a focus on correctness, simplicity, robustness, and performance.

%package -n python-%{pypi_name}-doc
Summary:        websockets documentation
%description -n python-%{pypi_name}-doc
Documentation for websockets

%prep
%autosetup -n %{pypi_name}-%{pypi_version}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
## generate html docs
#PYTHONPATH=${PWD} sphinx-build-3 docs html
## remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%{__python3} setup.py install --skip-build --root %{buildroot}

%check
# Disable tests for now
#%%{__python3} setup.py test

%files -n python%{python3_pkgversion}-%{pypi_name}
%doc README.rst
# Overwritten by doc directory flattening
#%%dov compliance/README.rst
%{python3_sitearch}/%{pypi_name}
#%%{python3_sitearch}/%{pypi_name}/extensions
#%%{python3_sitearch}/%{pypi_name}/legacy
%{python3_sitearch}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%files -n python-%{pypi_name}-doc
#%doc html
%license LICENSE

%changelog
* Wed Nov 02 2022 Nico Kadel-Garcia <nkadel@gmail.com> - 10.1-1
- Initial package.
