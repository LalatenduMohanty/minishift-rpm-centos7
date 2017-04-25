# If any of the following macros should be set otherwise,
# you can wrap any of them with the following conditions:
# - %%if 0%%{centos} == 7
# - %%if 0%%{?rhel} == 7
# - %%if 0%%{?fedora} == 23
# Or just test for particular distribution:
# - %%if 0%%{centos}
# - %%if 0%%{?rhel}
# - %%if 0%%{?fedora}
#
# Be aware, on centos, both %%rhel and %%centos are set. If you want to test
# rhel specific macros, you can use %%if 0%%{?rhel} && 0%%{?centos} == 0 condition.
# (Don't forget to replace double percentage symbol with single one in order to apply a condition)

# Generate devel rpm
%global with_devel 0
# Build project from bundled dependencies
%global with_bundled 1
# Build with debug info rpm
%global with_debug 0
# Run tests in check section
%global with_check 0
# Generate unit-test rpm
%global with_unit_test 0

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%endif

%global provider        github
%global provider_tld    com
%global project         minishift
%global repo            minishift
# https://github.com/minishift/minishift
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          36b772f752493387e6ecba66b6e4af3837e8438e
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           minishift
Version:        1.0.0-rc.2
Release:        0.1%{?dist}
Summary:        Run OpenShift locally
License:        ASL 2.0
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 aarch64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%if ! 0%{?with_bundled}
# gen_help_text.go
BuildRequires: golang(github.com/spf13/cobra/doc)

# Remaining dependencies not included in main packages
BuildRequires: golang(github.com/docker/go-units)
BuildRequires: golang(github.com/spf13/cobra)
BuildRequires: golang(gopkg.in/yaml.v2)
BuildRequires: golang(github.com/docker/machine/libmachine/drivers/rpc)
BuildRequires: golang(github.com/docker/machine/libmachine/shell)
BuildRequires: golang(github.com/google/go-github/github)
BuildRequires: golang(github.com/docker/machine/libmachine/auth)
BuildRequires: golang(github.com/docker/machine/libmachine/provision/serviceaction)
BuildRequires: golang(github.com/docker/machine/libmachine)
BuildRequires: golang(github.com/docker/machine/libmachine/mcnerror)
BuildRequires: golang(github.com/pborman/uuid)
BuildRequires: golang(github.com/blang/semver)
BuildRequires: golang(github.com/docker/machine/libmachine/host)
BuildRequires: golang(github.com/docker/machine/libmachine/drivers)
BuildRequires: golang(github.com/olekukonko/tablewriter)
BuildRequires: golang(golang.org/x/crypto/ssh)
BuildRequires: golang(github.com/spf13/viper)
BuildRequires: golang(github.com/docker/machine/libmachine/drivers/plugin)
BuildRequires: golang(github.com/docker/machine/libmachine/mcnutils)
BuildRequires: golang(github.com/docker/machine/libmachine/log)
BuildRequires: golang(github.com/kardianos/osext)
BuildRequires: golang(github.com/docker/machine/libmachine/drivers/plugin/localbinary)
BuildRequires: golang(github.com/docker/machine/libmachine/swarm)
BuildRequires: golang(golang.org/x/oauth2)
BuildRequires: golang(github.com/docker/machine/libmachine/engine)
BuildRequires: golang(github.com/docker/machine/drivers/vmwarefusion)
BuildRequires: golang(github.com/pkg/browser)
BuildRequires: golang(github.com/docker/machine/drivers/virtualbox)
BuildRequires: golang(github.com/asaskevich/govalidator)
BuildRequires: golang(github.com/docker/machine/libmachine/state)
BuildRequires: golang(golang.org/x/crypto/ssh/terminal)
BuildRequires: golang(github.com/inconshreveable/go-update)
BuildRequires: golang(github.com/docker/machine/libmachine/provision)
BuildRequires: golang(github.com/docker/machine/libmachine/provision/pkgaction)
BuildRequires: golang(github.com/docker/machine/drivers/hyperv)
BuildRequires: golang(github.com/pkg/errors)
BuildRequires: golang(github.com/docker/machine/libmachine/mcnflag)
BuildRequires: golang(github.com/golang/glog)
BuildRequires: golang(github.com/spf13/pflag)
BuildRequires: golang(github.com/docker/machine/libmachine/ssh)
%endif

%description
%{summary}

%if 0%{?with_devel}
%package devel
Summary:       %{summary}
BuildArch:     noarch

%if 0%{?with_check} && ! 0%{?with_bundled}
BuildRequires: golang(github.com/asaskevich/govalidator)
BuildRequires: golang(github.com/blang/semver)
BuildRequires: golang(github.com/docker/go-units)
BuildRequires: golang(github.com/docker/machine/drivers/hyperv)
BuildRequires: golang(github.com/docker/machine/drivers/virtualbox)
BuildRequires: golang(github.com/docker/machine/drivers/vmwarefusion)
BuildRequires: golang(github.com/docker/machine/libmachine)
BuildRequires: golang(github.com/docker/machine/libmachine/auth)
BuildRequires: golang(github.com/docker/machine/libmachine/drivers)
BuildRequires: golang(github.com/docker/machine/libmachine/drivers/plugin)
BuildRequires: golang(github.com/docker/machine/libmachine/drivers/plugin/localbinary)
BuildRequires: golang(github.com/docker/machine/libmachine/drivers/rpc)
BuildRequires: golang(github.com/docker/machine/libmachine/engine)
BuildRequires: golang(github.com/docker/machine/libmachine/host)
BuildRequires: golang(github.com/docker/machine/libmachine/log)
BuildRequires: golang(github.com/docker/machine/libmachine/mcnerror)
BuildRequires: golang(github.com/docker/machine/libmachine/mcnflag)
BuildRequires: golang(github.com/docker/machine/libmachine/mcnutils)
BuildRequires: golang(github.com/docker/machine/libmachine/provision)
BuildRequires: golang(github.com/docker/machine/libmachine/provision/pkgaction)
BuildRequires: golang(github.com/docker/machine/libmachine/provision/serviceaction)
BuildRequires: golang(github.com/docker/machine/libmachine/shell)
BuildRequires: golang(github.com/docker/machine/libmachine/ssh)
BuildRequires: golang(github.com/docker/machine/libmachine/state)
BuildRequires: golang(github.com/docker/machine/libmachine/swarm)
BuildRequires: golang(github.com/golang/glog)
BuildRequires: golang(github.com/google/go-github/github)
BuildRequires: golang(github.com/inconshreveable/go-update)
BuildRequires: golang(github.com/kardianos/osext)
BuildRequires: golang(github.com/olekukonko/tablewriter)
BuildRequires: golang(github.com/pborman/uuid)
BuildRequires: golang(github.com/pkg/browser)
BuildRequires: golang(github.com/pkg/errors)
BuildRequires: golang(github.com/spf13/cobra)
BuildRequires: golang(github.com/spf13/pflag)
BuildRequires: golang(github.com/spf13/viper)
BuildRequires: golang(golang.org/x/crypto/ssh)
BuildRequires: golang(golang.org/x/crypto/ssh/terminal)
BuildRequires: golang(golang.org/x/oauth2)
BuildRequires: golang(gopkg.in/yaml.v2)
%endif

Requires:      golang(github.com/asaskevich/govalidator)
Requires:      golang(github.com/blang/semver)
Requires:      golang(github.com/docker/go-units)
Requires:      golang(github.com/docker/machine/drivers/hyperv)
Requires:      golang(github.com/docker/machine/drivers/virtualbox)
Requires:      golang(github.com/docker/machine/drivers/vmwarefusion)
Requires:      golang(github.com/docker/machine/libmachine)
Requires:      golang(github.com/docker/machine/libmachine/auth)
Requires:      golang(github.com/docker/machine/libmachine/drivers)
Requires:      golang(github.com/docker/machine/libmachine/drivers/plugin)
Requires:      golang(github.com/docker/machine/libmachine/drivers/plugin/localbinary)
Requires:      golang(github.com/docker/machine/libmachine/drivers/rpc)
Requires:      golang(github.com/docker/machine/libmachine/engine)
Requires:      golang(github.com/docker/machine/libmachine/host)
Requires:      golang(github.com/docker/machine/libmachine/log)
Requires:      golang(github.com/docker/machine/libmachine/mcnerror)
Requires:      golang(github.com/docker/machine/libmachine/mcnflag)
Requires:      golang(github.com/docker/machine/libmachine/mcnutils)
Requires:      golang(github.com/docker/machine/libmachine/provision)
Requires:      golang(github.com/docker/machine/libmachine/provision/pkgaction)
Requires:      golang(github.com/docker/machine/libmachine/provision/serviceaction)
Requires:      golang(github.com/docker/machine/libmachine/shell)
Requires:      golang(github.com/docker/machine/libmachine/ssh)
Requires:      golang(github.com/docker/machine/libmachine/state)
Requires:      golang(github.com/docker/machine/libmachine/swarm)
Requires:      golang(github.com/golang/glog)
Requires:      golang(github.com/google/go-github/github)
Requires:      golang(github.com/inconshreveable/go-update)
Requires:      golang(github.com/kardianos/osext)
Requires:      golang(github.com/olekukonko/tablewriter)
Requires:      golang(github.com/pborman/uuid)
Requires:      golang(github.com/pkg/browser)
Requires:      golang(github.com/pkg/errors)
Requires:      golang(github.com/spf13/cobra)
Requires:      golang(github.com/spf13/pflag)
Requires:      golang(github.com/spf13/viper)
Requires:      golang(golang.org/x/crypto/ssh)
Requires:      golang(golang.org/x/crypto/ssh/terminal)
Requires:      golang(golang.org/x/oauth2)
Requires:      golang(gopkg.in/yaml.v2)

Provides: bundled(golang(github.com/cpuguy83/go-md2man/md2man)) = %{version}-a65d4d2de4d5f7c74868dfa9b202a3c8be315aaa
Provides: bundled(golang(github.com/DATA-DOG/godog/colors)) = %{version}-c3f5ce27930fff8efffaaf0acab7f24d5deecdbc
Provides: bundled(golang(github.com/DATA-DOG/godog/gherkin)) = %{version}-c3f5ce27930fff8efffaaf0acab7f24d5deecdbc
Provides: bundled(golang(github.com/docker/docker/pkg/term)) = %{version}-a8a31eff10544860d2188dddabdee4d727545796
Provides: bundled(golang(github.com/docker/machine/commands/mcndirs)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/drivers/errdriver)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/drivers/fakedriver)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/drivers/hyperv)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/drivers/none)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/drivers/virtualbox)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/drivers/vmwarefusion)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/libmachine)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/libmachine/auth)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/libmachine/cert)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/libmachine/check)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/libmachine/drivers)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/libmachine/drivers/plugin)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/libmachine/drivers/plugin/localbinary)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/libmachine/drivers/rpc)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/libmachine/engine)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/libmachine/host)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/libmachine/log)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/libmachine/mcndockerclient)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/libmachine/mcnerror)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/libmachine/mcnflag)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/libmachine/mcnutils)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/libmachine/persist)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/libmachine/provision)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/libmachine/provision/pkgaction)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/libmachine/provision/provisiontest)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/libmachine/provision/serviceaction)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/libmachine/shell)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/libmachine/ssh)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/libmachine/state)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/libmachine/swarm)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/libmachine/version)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/libmachine/versioncmp)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/docker/machine/version)) = %{version}-15fd4c70403bab784d91031af02d9e169ce66412
Provides: bundled(golang(github.com/golang/protobuf/proto)) = %{version}-3c84672111d91bb5ac31719e112f9f7126a0e26e
Provides: bundled(golang(github.com/google/go-github/github)) = %{version}-30a21ee1a3839fb4a408efe331f226b73faac379
Provides: bundled(golang(github.com/google/go-querystring/query)) = %{version}-30f7a39f4a218feb5325f3aebc60c32a572a8274
Provides: bundled(golang(github.com/hashicorp/hcl/hcl/ast)) = %{version}-372e8ddaa16fd67e371e9323807d056b799360af
Provides: bundled(golang(github.com/hashicorp/hcl/hcl/parser)) = %{version}-372e8ddaa16fd67e371e9323807d056b799360af
Provides: bundled(golang(github.com/hashicorp/hcl/hcl/scanner)) = %{version}-372e8ddaa16fd67e371e9323807d056b799360af
Provides: bundled(golang(github.com/hashicorp/hcl/hcl/strconv)) = %{version}-372e8ddaa16fd67e371e9323807d056b799360af
Provides: bundled(golang(github.com/hashicorp/hcl/hcl/token)) = %{version}-372e8ddaa16fd67e371e9323807d056b799360af
Provides: bundled(golang(github.com/hashicorp/hcl/json/parser)) = %{version}-372e8ddaa16fd67e371e9323807d056b799360af
Provides: bundled(golang(github.com/hashicorp/hcl/json/scanner)) = %{version}-372e8ddaa16fd67e371e9323807d056b799360af
Provides: bundled(golang(github.com/hashicorp/hcl/json/token)) = %{version}-372e8ddaa16fd67e371e9323807d056b799360af
Provides: bundled(golang(github.com/inconshreveable/go-update/internal/binarydist)) = %{version}-8152e7eb6ccf8679a64582a66b78519688d156ad
Provides: bundled(golang(github.com/inconshreveable/go-update/internal/osext)) = %{version}-8152e7eb6ccf8679a64582a66b78519688d156ad
Provides: bundled(golang(github.com/spf13/afero/mem)) = %{version}-72b31426848c6ef12a7a8e216708cb0d1530f074
Provides: bundled(golang(github.com/spf13/cobra/doc)) = %{version}-b5d8e8f46a2f829f755b6e33b454e25c61c935e1
Provides: bundled(golang(golang.org/x/crypto/curve25519)) = %{version}-beef0f4390813b96e8e68fd78570396d0f4751fc
Provides: bundled(golang(golang.org/x/crypto/ssh)) = %{version}-beef0f4390813b96e8e68fd78570396d0f4751fc
Provides: bundled(golang(golang.org/x/crypto/ssh/terminal)) = %{version}-beef0f4390813b96e8e68fd78570396d0f4751fc
Provides: bundled(golang(golang.org/x/net/context)) = %{version}-4f2fc6c1e69d41baf187332ee08fbd2b296f21ed
Provides: bundled(golang(golang.org/x/net/context/ctxhttp)) = %{version}-4f2fc6c1e69d41baf187332ee08fbd2b296f21ed
Provides: bundled(golang(golang.org/x/oauth2/internal)) = %{version}-442624c9ec9243441e83b374a9e22ac549b5c51d
Provides: bundled(golang(golang.org/x/sys/windows/registry)) = %{version}-d9157a9621b69ad1d8d77a1933590c416593f24f
Provides: bundled(golang(golang.org/x/text/transform)) = %{version}-ceefd2213ed29504fff30155163c8f59827734f3
Provides: bundled(golang(golang.org/x/text/unicode/norm)) = %{version}-ceefd2213ed29504fff30155163c8f59827734f3
Provides: bundled(golang(google.golang.org/appengine/internal)) = %{version}-6a436539be38c296a8075a871cc536686b458371
Provides: bundled(golang(google.golang.org/appengine/internal/app_identity)) = %{version}-6a436539be38c296a8075a871cc536686b458371
Provides: bundled(golang(google.golang.org/appengine/internal/base)) = %{version}-6a436539be38c296a8075a871cc536686b458371
Provides: bundled(golang(google.golang.org/appengine/internal/datastore)) = %{version}-6a436539be38c296a8075a871cc536686b458371
Provides: bundled(golang(google.golang.org/appengine/internal/log)) = %{version}-6a436539be38c296a8075a871cc536686b458371
Provides: bundled(golang(google.golang.org/appengine/internal/modules)) = %{version}-6a436539be38c296a8075a871cc536686b458371
Provides: bundled(golang(google.golang.org/appengine/internal/remote_api)) = %{version}-6a436539be38c296a8075a871cc536686b458371
Provides: bundled(golang(google.golang.org/appengine/internal/urlfetch)) = %{version}-6a436539be38c296a8075a871cc536686b458371
Provides: bundled(golang(google.golang.org/appengine/urlfetch)) = %{version}-6a436539be38c296a8075a871cc536686b458371

%description devel
%{summary}

%if 0%{?with_devel}
Summary:       %{summary}
BuildArch:     noarch

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test-devel
Summary:         Unit tests for %{name} package
%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}

%if 0%{?with_check} && ! 0%{?with_bundled}
BuildRequires: golang(github.com/DATA-DOG/godog)
BuildRequires: golang(github.com/DATA-DOG/godog/gherkin)
BuildRequires: golang(github.com/docker/machine/drivers/fakedriver)
BuildRequires: golang(github.com/docker/machine/libmachine/provision/provisiontest)
%endif

Requires:      golang(github.com/DATA-DOG/godog)
Requires:      golang(github.com/DATA-DOG/godog/gherkin)
Requires:      golang(github.com/docker/machine/drivers/fakedriver)
Requires:      golang(github.com/docker/machine/libmachine/provision/provisiontest)

%description unit-test-devel
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%setup -q -n %{repo}-%{commit}

%build
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s ../../../ src/%{import_path}

%if ! 0%{?with_bundled}
export GOPATH=$(pwd):%{gopath}
%else
# No dependency directories so far
export GOPATH=$(pwd):%{gopath}
%endif

export LDFLAGS=%{ldflags}
%gobuild %{buildflags} -o bin/komposeld %{buildflags} -o bin/kompose %{import_path}/ %{import_path}/

#%gobuild -o bin/ %{import_path}/
#%gobuild -o bin/cmd/minishift %{import_path}/cmd/minishift

%install
install -d -p %{buildroot}%{_bindir}
install -p -m 0755 bin/minishift %{buildroot}%{_bindir}
#install -p -m 0755 bin/cmd/minishift %{buildroot}%{_bindir}

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . \( -iname "*.go" -or -iname "*.s" \) \! -iname "*_test.go") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test-devel.file-list
for file in $(find . -iname "*_test.go") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test-devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
# No dependency directories so far

export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%endif

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}/cmd/minishift/cmd
%gotest %{import_path}/cmd/minishift/cmd/addon
%gotest %{import_path}/cmd/minishift/cmd/config
%gotest %{import_path}/cmd/minishift/cmd/openshift
%gotest %{import_path}/pkg/minikube/cluster
%gotest %{import_path}/pkg/minikube/constants
%gotest %{import_path}/pkg/minikube/kubeconfig
%gotest %{import_path}/pkg/minikube/machine
%gotest %{import_path}/pkg/minikube/sshutil
%gotest %{import_path}/pkg/minishift/addon
%gotest %{import_path}/pkg/minishift/addon/command
%gotest %{import_path}/pkg/minishift/addon/manager
%gotest %{import_path}/pkg/minishift/addon/parser
%gotest %{import_path}/pkg/minishift/cache
%gotest %{import_path}/pkg/minishift/config
%gotest %{import_path}/pkg/minishift/hostfolder
%gotest %{import_path}/pkg/minishift/oc
%gotest %{import_path}/pkg/minishift/openshift/version
%gotest %{import_path}/pkg/minishift/provisioner
%gotest %{import_path}/pkg/minishift/registration
%gotest %{import_path}/pkg/minishift/util
%gotest %{import_path}/pkg/testing/cli
%gotest %{import_path}/pkg/util
%gotest %{import_path}/pkg/util/cmd
%gotest %{import_path}/pkg/util/filehelper
%gotest %{import_path}/pkg/util/github
%gotest %{import_path}/test/integration
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE
#%{_bindir}/
#%{_bindir}/cmd/minishift

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENSE
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files unit-test-devel -f unit-test-devel.file-list
%license LICENSE
%endif

%changelog* Tue Apr 25 2017 Lalatendu Mohanty <lmohanty@redhat.com> - 0-0.1.git36b772f
- First package for Fedora

