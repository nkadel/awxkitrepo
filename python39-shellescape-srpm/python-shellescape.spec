# Created by pyp2rpm-3.3.8
%global pypi_name shellescape
%global srcname shellescape
%global pypi_version 3.8.1

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        0%{?dist}
Summary:        Shell escape a string to safely use it as a token in a shell command (backport of cPython shlex

License:        MIT license
URL:            https://github.com/chrissimpkins/shellescape
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%description
 shellescape DescriptionThe shellescape Python module defines the
shellescape.quote() function that returns a shell-escaped version of a Python
string. This is a backport of the shlex.quote() function from Python 3.8 that
makes it accessible to users of Python 3 versions < 3.3 and all Python 2.x
versions. quote(s)*From the Python documentation*:Return a shell-escaped
version of the string s....

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        Shell escape a string to safely use it as a token in a shell command (backport of cPython shlex

%description -n python%{python3_pkgversion}-%{pypi_name}
 shellescape DescriptionThe shellescape Python module defines the
shellescape.quote() function that returns a shell-escaped version of a Python
string. This is a backport of the shlex.quote() function from Python 3.8 that
makes it accessible to users of Python 3 versions < 3.3 and all Python 2.x
versions. quote(s)*From the Python documentation*:Return a shell-escaped
version of the string s....


%prep
%autosetup -n %{pypi_name}-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --skip-build --root %{buildroot}

%files -n python%{python3_pkgversion}-%{pypi_name}
%doc README.md docs/README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%changelog
* Wed Nov 02 2022 Nico Kadel-Garcia <nkadel@gmail.com> - 3.8.1-1
- Initial package.
