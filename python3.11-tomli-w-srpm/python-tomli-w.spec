# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.11
%global python3_pkgversion 3.11
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

%bcond_with check

Name:           python-tomli-w
Version:        0.4.0
#Release:        3%%{?dist}
Release:        0.3%{?dist}
Summary:        A Python library for writing TOML

License:        MIT
URL:            https://github.com/hukkin/tomli-w
Source0:        %{url}/archive/%{version}/tomli-w-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel

%global _description %{expand:
Tomli-W is a Python library for writing TOML. It is a write-only counterpart
to Tomli, which is a read-only TOML parser. Tomli-W is fully compatible
with TOML v1.0.0.}

%description %_description

%package -n python3-tomli-w
Summary:        %{summary}

%description -n python3-tomli-w %_description


%prep
%autosetup -p1 -n tomli-w-%{version}
# Measuring coverage is discouraged in Python packaging guidelines:
sed -i '/pytest-cov/d' tests/requirements.txt
# This testing dependency is optional and we don't have it in (EP)EL,
# it has many missing transitive dependencies that we don't want to maintain
%if 0%{?rhel}
sed -i '/pytest-randomly/d' tests/requirements.txt
%endif


%generate_buildrequires
%pyproject_buildrequires %{?with_check:-t}


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files tomli_w


%check
%pyproject_check_import tomli_w
%if %{with check}
%tox
%endif


%files -n python3-tomli-w -f %{pyproject_files}
%doc README.md
%doc CHANGELOG.md
%license LICENSE


%changelog
* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 20 2022 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.4.0-2
- Add boostrap and check toggles to ease bootstrapping new EPEL releases

* Wed Oct 27 2021 Tomáš Hrnčiar <thrnciar@redhat.com> - 0.4.0-1
- Initial package
