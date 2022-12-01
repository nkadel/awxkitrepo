#
# Makefile - build wrapper for Ansible RPMs
#

#REOBASEE=http://localhost
REPOBASE=file://$(PWD)


# EPEL built
ANSIBLEPKGS+=python39-crypto-srpm
ANSIBLEPKGS+=python39-jq-srpm
ANSIBLEPKGS+=python39-naked-srpm
ANSIBLEPKGS+=python39-shellescape-srpm

ANSIBLEPKGS+=python39-websockets-srpm
ANSIBLEPKGS+=python39-websocket-client-srpm

ANSIBLEPKGS+=python39-awxkit-srpm

REPOS+=awxkitrepo/el/8
REPOS+=awxkitrepo/el/9
REPOS+=awxkitrepo/fedora/37
REPOS+=awxkitrepo/amz/2

REPODIRS := $(patsubst %,%/x86_64/repodata,$(REPOS)) $(patsubst %,%/SRPMS/repodata,$(REPOS))

CFGS+=awxkitrepo-8-x86_64.cfg
CFGS+=awxkitrepo-9-x86_64.cfg
CFGS+=awxkitrepo-f37-x86_64.cfg
# Amazon 2 config
#CFGS+=awxkitrepo-amz2-x86_64.cfg

# /etc/mock version lacks python39 modules
CFGS+=centos-stream+epel-8-x86_64.cfg

# Link from /etc/mock
MOCKCFGS+=centos-stream+epel-9-x86_64.cfg
MOCKCFGS+=fedora-37-x86_64.cfg
#MOCKCFGS+=amazonlinux-2-x86_64.cfg

all:: install

install:: $(CFGS)
install:: $(MOCKCFGS)
install:: $(REPODIRS)
install:: $(ANSIBLEPKGS)

# Actually put all the modules in the local repo
.PHONY: install clean getsrc build srpm src.rpm
install clean getsrc build srpm src.rpm::
	@for name in $(ANSIBLEPKGS); do \
	     (cd $$name && $(MAKE) $(MFLAGS) $@); \
	done  

# Git submodule checkout operation
# For more recent versions of git, use "git checkout --recurse-submodules"
#*-srpm::
#	@[ -d $@/.git ] || \
#	     git submodule update --init $@

# Dependencies of libraries on other libraries for compilation

#python39-commentjson-srpm:: python39-lark-parser-srpm
#python39-entrypoints-srpm:: python39-commentjson-srpm
#
#python39-flake8-srpm:: pyflakes-srpm
#
#python39-resolvelib-srpm:: python39-flake8-srpm
#python39-resolvelib-srpm:: python39-commentjson-srpm
#
#awxkit-core-2.11.x-srpm:: python39-resolvelib-srpm
##awxkit-core-2.12.x-srpm:: python39-resolvelib-srpm
#awxkit-core-2.13.x-srpm:: python39-resolvelib-srpm
#
#awxkit-4.x-srpm:: awxkit-core-2.11.x-srpm
##awxkit-5.x-srpm:: awxkit-core-2.12.x-srpm
#awxkit-6.x-srpm:: awxkit-core-2.13.x-srpm

# Actually build in directories
.PHONY: $(ANSIBLEPKGS)
$(ANSIBLEPKGS)::
	(cd $@ && $(MAKE) $(MLAGS) install)

repodirs: $(REPOS) $(REPODIRS)
repos: $(REPOS) $(REPODIRS)
$(REPOS):
	install -d -m 755 $@

.PHONY: $(REPODIRS)
$(REPODIRS): $(REPOS)
	@install -d -m 755 `dirname $@`
	/usr/bin/createrepo_c -q `dirname $@`

.PHONY: cfg
cfg:: cfgs

.PHONY: cfgs
cfgs:: $(CFGS)
cfgs:: $(MOCKCFGS)


$(MOCKCFGS)::
	@echo Generating $@ from $?
	@echo "include('/etc/mock/$@')" | tee $@

centos-stream+epel-8-x86_64.cfg:: /etc/mock/centos-stream+epel-8-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" | tee $@
	@echo "# Enable python39 modules" | tee -a $@
	@echo "config_opts['module_setup_commands'] = [ ('enable', 'python39'), ('enable', 'python39-devel') ]" | tee -a $@
	@echo "# Disable best" | tee -a $@
	@echo "config_opts['dnf_vars'] = { 'best': 'False' }" | tee -a $@


awxkitrepo-8-x86_64.cfg: /etc/mock/centos-stream+epel-8-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" | tee $@
	@echo "config_opts['root'] = 'awxkitrepo-{{ releasever }}-{{ target_arch }}'" | tee -a $@
	@echo "# Enable python39 modules" | tee -a $@
	@echo "config_opts['module_setup_commands'] = [ ('enable', 'python39'), ('enable', 'python39-devel') ]" | tee -a $@
	@echo "# Disable best" | tee -a $@
	@echo "config_opts['dnf_vars'] = { 'best': 'False' }" | tee -a $@
	@echo "config_opts['dnf.conf'] += \"\"\"" | tee -a $@
	@echo '[awxkitrepo]' | tee -a $@
	@echo 'name=awxkitrepo' | tee -a $@
	@echo 'enabled=1' | tee -a $@
	@echo 'baseurl=$(REPOBASE)/awxkitrepo/el/8/x86_64/' | tee -a $@
	@echo 'skip_if_unavailable=False' | tee -a $@
	@echo 'metadata_expire=1s' | tee -a $@
	@echo 'gpgcheck=0' | tee -a $@
	@echo '"""' | tee -a $@

# packages-microsoft-com-prod added for /bin/pwsh
awxkitrepo-9-x86_64.cfg: centos-stream+epel-9-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" | tee $@
	@echo "config_opts['root'] = 'awxkitrepo-{{ releasever }}-{{ target_arch }}'" | tee -a $@
	@echo "config_opts['dnf.conf'] += \"\"\"" | tee -a $@
	@echo '[awxkitrepo]' | tee -a $@
	@echo 'name=awxkitrepo' | tee -a $@
	@echo 'enabled=1' | tee -a $@
	@echo 'baseurl=$(REPOBASE)/awxkitrepo/el/9/x86_64/' | tee -a $@
	@echo 'skip_if_unavailable=False' | tee -a $@
	@echo 'metadata_expire=1s' | tee -a $@
	@echo 'gpgcheck=0' | tee -a $@
	@echo '"""' | tee -a $@

awxkitrepo-f37-x86_64.cfg: /etc/mock/fedora-37-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" | tee $@
	@echo "config_opts['root'] = 'awxkitrepo-f{{ releasever }}-{{ target_arch }}'" | tee -a $@
	@echo "config_opts['dnf.conf'] += \"\"\"" | tee -a $@
	@echo '[awxkitrepo]' | tee -a $@
	@echo 'name=awxkitrepo' | tee -a $@
	@echo 'enabled=1' | tee -a $@
	@echo 'baseurl=$(REPOBASE)/awxkitrepo/fedora/37/x86_64/' | tee -a $@
	@echo 'skip_if_unavailable=False' | tee -a $@
	@echo 'metadata_expire=1s' | tee -a $@
	@echo 'gpgcheck=0' | tee -a $@
	@echo '"""' | tee -a $@

awxkitrepo-rawhide-x86_64.cfg: /etc/mock/fedora-rawhide-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" | tee $@
	@echo "config_opts['root'] = 'awxkitrepo-rawhide-{{ target_arch }}'" | tee -a $@
	@echo "config_opts['dnf.conf'] += \"\"\"" | tee -a $@
	@echo '[awxkitrepo]' | tee -a $@
	@echo 'name=awxkitrepo' | tee -a $@
	@echo 'enabled=1' | tee -a $@
	@echo 'baseurl=$(REPOBASE)/awxkitrepo/fedora/rawhide/x86_64/' | tee -a $@
	@echo 'skip_if_unavailable=False' | tee -a $@
	@echo 'metadata_expire=1s' | tee -a $@
	@echo 'gpgcheck=0' | tee -a $@
	@echo '"""' | tee -a $@

awxkitrepo-amz2-x86_64.cfg: /etc/mock/amazonlinux-2-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" | tee $@
	@echo "config_opts['root'] = 'awxkitrepo-amz2-{{ target_arch }}'" | tee -a $@
	@echo "config_opts['dnf.conf'] += \"\"\"" | tee -a $@
	@echo '[awxkitrepo]' | tee -a $@
	@echo 'name=awxkitrepo' | tee -a $@
	@echo 'enabled=1' | tee -a $@
	@echo 'baseurl=$(REPOBASE)/awxkitrepo/amz/2/x86_64/' | tee -a $@
	@echo 'skip_if_unavailable=False' | tee -a $@
	@echo 'metadata_expire=1s' | tee -a $@
	@echo 'gpgcheck=0' | tee -a $@
	@echo '"""' | tee -a $@

repo: awxkitrepo.repo
awxkitrepo.repo:: Makefile awxkitrepo.repo.in
	if [ -s /etc/fedora-release ]; then \
		cat $@.in | \
			sed "s|@REPOBASEDIR@/|$(PWD)/|g" | \
			sed "s|/@RELEASEDIR@/|/fedora/|g" | tee $@; \
	elif [ -s /etc/redhat-release ]; then \
		cat $@.in | \
			sed "s|@REPOBASEDIR@/|$(PWD)/|g" | \
			sed "s|/@RELEASEDIR@/|/el/|g" | tee $@; \
	else \
		echo Error: unknown release, check /etc/*-release; \
		exit 1; \
	fi

awxkitrepo.repo::
	@cmp -s $@ /etc/yum.repos.d/$@ || \
	    diff -u $@ /etc/yum.repos.d/$@

clean::
	find . -name \*~ -exec rm -f {} \;
	rm -f *.cfg
	rm -f *.out
	@for name in $(ANSIBLEPKGS); do \
	    $(MAKE) -C $$name clean; \
	done

distclean: clean
	rm -rf $(REPOS)
	rm -rf awxkitrepo
	@for name in $(ANSIBLEPKGS); do \
	    (cd $$name; git clean -x -d -f); \
	done

maintainer-clean: distclean
	rm -rf $(ANSIBLEPKGS)
	@for name in $(ANSIBLEPKGS); do \
	    (cd $$name; git clean -x -d -f); \
	done
