# generate current minishift dependencies
pushd minishift
wget -q https://raw.githubusercontent.com/minishift/minishift/master/glide.yaml
yum -y install "python-yaml"
python glide2specinc.py > ~/rpmbuild/SOURCES/glide2specinc.inc
# https://github.com/marcindulak/minishift-rpm-centos7/issues/5
sed -i 's|gopkg.in/cheggaaa/pb.v1|github.com/cheggaaa/pb|' ~/rpmbuild/SOURCES/glide2specinc.inc
# major.minor.release for github.com/jteeuwen/go-bindata
sed -i 's|v3.0|v3.0.7|' ~/rpmbuild/SOURCES/glide2specinc.inc
popd

yum -y install "compiler(go-compiler)"
yum -y install "golang(github.com/docker/go-units)"
#yum -y install "golang(github.com/google/go-github/github)"  # https://bugzilla.redhat.com/show_bug.cgi?id=1430132
yum -y install "https://kojipkgs.fedoraproject.org//packages/golang-github-google-go-github/0/0.1.git553fda4.fc25/noarch/golang-github-google-go-github-devel-0-0.1.git553fda4.fc25.noarch.rpm"  # https://bugzilla.redhat.com/show_bug.cgi?id=1430132

yum -y install bsdiff
spectool -g -R golang-github-inconshreveable-go-update/golang-github-inconshreveable-go-update.spec
rpmbuild -bb golang-github-inconshreveable-go-update/golang-github-inconshreveable-go-update.spec

spectool -g -R golang-github-pkg-browser/golang-github-pkg-browser.spec
rpmbuild -bb golang-github-pkg-browser/golang-github-pkg-browser.spec

yum -y install "golang(golang.org/x/sys/unix)"
spectool -g -R golang-github-mattn-go-isatty/golang-github-mattn-go-isatty.spec
rpmbuild -bb golang-github-mattn-go-isatty/golang-github-mattn-go-isatty.spec

createrepo ~/rpmbuild/RPMS&& yum clean all --enablerepo=minishift --disablerepo='*'
yum -y install "golang(github.com/mattn/go-isatty)"
spectool -g -R golang-github-mattn-go-colorable/golang-github-mattn-go-colorable.spec
rpmbuild -bb golang-github-mattn-go-colorable/golang-github-mattn-go-colorable.spec

createrepo ~/rpmbuild/RPMS&& yum clean all --enablerepo=minishift --disablerepo='*'
yum -y install "golang(github.com/mattn/go-colorable)"
spectool -g -R golang-github-fatih-color/golang-github-fatih-color.spec
rpmbuild -bb golang-github-fatih-color/golang-github-fatih-color.spec

createrepo ~/rpmbuild/RPMS&& yum clean all --enablerepo=minishift --disablerepo='*'
yum -y install "golang(github.com/fatih/color)"
spectool -g -R golang-github-cheggaaa-pb/golang-github-cheggaaa-pb.spec
rpmbuild -bb golang-github-cheggaaa-pb/golang-github-cheggaaa-pb.spec

spectool -g -R golang-github-asaskevich-govalidator/golang-github-asaskevich-govalidator.spec
rpmbuild -bb golang-github-asaskevich-govalidator/golang-github-asaskevich-govalidator.spec

createrepo ~/rpmbuild/RPMS&& yum clean all --enablerepo=minishift --disablerepo='*'
yum -y install "golang(github.com/inconshreveable/go-update)"
yum -y install "golang(github.com/kardianos/osext)"
yum -y install "golang(github.com/olekukonko/tablewriter)"
yum -y install "golang(github.com/pkg/browser)"
yum -y install "golang(github.com/spf13/cobra)"
yum -y install "golang(github.com/xeipuuv/gojsonschema)"
yum -y install "golang(golang.org/x/oauth2)"
yum -y install "golang(golang.org/x/crypto/ssh)"
yum -y install "golang(github.com/cheggaaa/pb)"

pushd minishift
# download the dependencies
wget -q https://github.com/docker/machine/archive/v0.9.0.tar.gz -P ~/rpmbuild/SOURCES/
wget -q https://github.com/mitchellh/mapstructure/archive/db1efb556f84b25a0a13a04aad883943538ad2e0/mapstructure-db1efb5.tar.gz -P ~/rpmbuild/SOURCES/  # TODO
wget -q https://github.com/spf13/viper/archive/382f87b929b84ce13e9c8a375a4b217f224e6c65/viper-382f87b.tar.gz -P ~/rpmbuild/SOURCES/  # TODO
wget -q https://github.com/blang/semver/archive/v3.5.0.tar.gz -P ~/rpmbuild/SOURCES/  # TODO
wget -q https://github.com/pkg/errors/archive/v0.8.0.tar.gz -P ~/rpmbuild/SOURCES/  # TODO
wget -q https://github.com/jteeuwen/go-bindata/archive/v3.0.7.tar.gz -P ~/rpmbuild/SOURCES/  # TODO
wget -q https://github.com/asaskevich/govalidator/archive/v5.tar.gz -P ~/rpmbuild/SOURCES/
wget -q https://github.com/DATA-DOG/godog/archive/v0.6.2.tar.gz -P ~/rpmbuild/SOURCES/  # TODO
wget -q https://github.com/golang/glog/archive/335da9dda11408a34b64344f82e9c03779b71673/glog-335da9d.tar.gz -P ~/rpmbuild/SOURCES/  # TODO

wget -q https://github.com/minishift/minishift/archive/cebec68fcf03ae5b5a9c0b808178b542c17215a7/minishift-cebec68.tar.gz -P ~/rpmbuild/SOURCES/

rpmbuild -bb minishift.spec  # broken build stage
