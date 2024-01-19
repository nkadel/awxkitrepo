# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.11
%global python3_pkgversion 3.11
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

Name:           python-ansible-tower-cli
Version:        3.3.9
Release:        0.1%{?dist}
Summary:        A CLI tool for Ansible Tower and AWX.

# Check if the automatically generated License and its spelling is correct for Fedora
# https://docs.fedoraproject.org/en-US/packaging-guidelines/LicensingGuidelines/
License:        ASL
URL:            https://github.com/ansible/tower-cli
Source:         %{pypi_source ansible-tower-cli}

BuildArch:      noarch
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-click < 7.0
BuildRequires:  python%{python3_pkgversion}-colorama >= 0.3.1
BuildRequires:  python%{python3_pkgversion}-requests >= 2.3.9
BuildRequires:  python%{python3_pkgversion}-six >= 1.7.2
BuildRequires:  python%{python3_pkgversion}-pyyaml >= 3.1.0

# Fill in the actual package description to submit package to Fedora
%global _description %{expand:
This is package 'ansible-tower-cli' generated automatically by pyp2spec.}


%description %_description

%package -n     python%{python3_pkgversion}-ansible-tower-cli
Summary:        %{summary}

%description -n python%{python3_pkgversion}-ansible-tower-cli %_description


%prep
%autosetup -p1 -n ansible-tower-cli-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
# For official Fedora packages, including files with '*' +auto is not allowed
# Replace it with a list of relevant Python modules/globs and list extra files in %%files
%pyproject_save_files '*' +auto


%check
%pyproject_check_import


%files -n python%{python3_pkgversion}-ansible-tower-cli -f %{pyproject_files}


%changelog
* Tue May 30 2023 Nico Kadel-Garcia <ikadel-garcia@statestreet.com> - 3.3.9-1
- Initial package
