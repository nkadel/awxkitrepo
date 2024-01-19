# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.11
%global python3_pkgversion 3.11
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

## START: Set by rpmautospec
## (rpmautospec version 0.3.1)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# Let’s try to build this as early as we can, since it’s a dependency for
# some important libraries, such as python-platformdirs.
%bcond_with bootstrap
%if %{without bootstrap}
%bcond_without tests
%else
%bcond_with tests
%endif

Name:           python-hatch-vcs
Version:        0.3.0
Release:        %autorelease
Summary:        Hatch plugin for versioning with your preferred VCS

# SPDX
License:        MIT
URL:            https://github.com/ofek/hatch-vcs
Source0:        %{pypi_source hatch_vcs}

BuildArch:      noarch

# Work with setuptools_scm 7.1 (fix #25)
# https://github.com/ofek/hatch-vcs/pull/26
Patch:          %{url}/pull/26.patch

BuildRequires:  python3-devel
BuildRequires:  python3-exceptiongroup

%if %{with tests}
BuildRequires:  python3dist(pytest)
BuildRequires:  git-core
%endif

%global common_description %{expand:
This provides a plugin for Hatch that uses your preferred version control
system (like Git) to determine project versions.}

%description %{common_description}


%package -n python3-hatch-vcs
Summary:        %{summary}

%description -n python3-hatch-vcs %{common_description}


%prep
%autosetup -n hatch_vcs-%{version} -p1


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files hatch_vcs


%check
%if %{with tests}
%pytest
%else
%pyproject_check_import
%endif


%files -n python3-hatch-vcs -f %{pyproject_files}
%doc HISTORY.md
%doc README.md


%changelog
* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 20 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.3.0-2
- Work with setuptools_scm 7.1

* Sat Dec 10 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.3.0-1
- Update to 0.3.0 (close RHBZ#2152320)
- We can now rely on pyproject-rpm-macros >= 1.2.0
- The LICENSE.txt file is now handled in pyproject_files
- The setuptools_scm 7 patch is now merged upstream

* Sat Oct 22 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.0-10
- Confirm License is SPDX MIT

* Sun Sep 11 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.0-9
- Use hatchling’s new “prepare_metadata_…” hook support for BR’s

* Thu Jul 21 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.0-8
- Updated setuptools_scm 7 patch again

* Thu Jul 07 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.0-7
- Fix extra newline in description

* Thu Jun 30 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.0-6
- Updated setuptools_scm 7 patch

* Thu Jun 30 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.0-5
- Fix test compatibility with setuptools_scm 7

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.2.0-4
- Rebuilt for Python 3.11

* Fri May 06 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.0-3
- Use wheel-building support to generate BR’s

* Sun May 01 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.0-2
- Adjust for pyproject-rpm-macros >= 1.1.0

* Fri Apr 22 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.0-1
- Initial package (close RHBZ#2077832)
