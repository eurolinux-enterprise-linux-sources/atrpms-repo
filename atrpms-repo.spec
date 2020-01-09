Summary: Configuration files for package managers.
Name: atrpms-repo
Version: %{distversion}
Release: 4%{?dist}
License: GPLv3
Group: System Environment/Base
URL: http://ATrpms.net/
Source0: RPM-GPG-KEY-atrpms
Source1: atrpms.repo.in
Source2: atrpms-testing.repo.in
Source3: atrpms-bleeding.repo.in
Source4: atrpms.channel.in
Source5: atrpms-testing.channel.in
Source6: atrpms-bleeding.channel.in
Source7: atrpms.list.in
Source8: atrpms-testing.list.in
Source9: atrpms-bleeding.list.in
Source10: f.sed
Source11: el.sed
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Obsoletes: fedora-package-config, redhat-package-config
Provides: fedora-package-config, redhat-package-config
Obsoletes: smart-config, apt-config, yum-config
Provides: smart-config, apt-config, yum-config
Obsoletes: atrpms-package-config
Provides: atrpms-package-config

%description
This package contains configuration files for yum, smart and apt.

%prep
%setup -q -T -c

%build
cp -a %{SOURCE10} %{SOURCE11} .
cat %distinitials.sed > temp.sed
cat >> temp.sed <<EOF
s,@DISTARCH@,%{distinitials}%{distversion}-%{_target_cpu},g
s,@DISTINITIALS@,%{distinitials},g
s,@DIST@,$dist,g
s,@DISTVERSION@,%{distversion},g
s,@ARCH@,%{_target_cpu},g
EOF

for s in %{SOURCE1} %{SOURCE2} %{SOURCE3} \
         %{SOURCE4} %{SOURCE5} %{SOURCE6} \
         %{SOURCE7} %{SOURCE8} %{SOURCE9}; do
  f=`echo $s | sed -e's,.*/\([^/]*\)\.in$,\1,'`
  sed -f temp.sed < $s > $f
  touch -r $s $f
done

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/pki/rpm-gpg
install -p %{SOURCE0} %{buildroot}%{_sysconfdir}/pki/rpm-gpg

mkdir -p %{buildroot}%{_sysconfdir}/yum.repos.d
install -p *.repo %{buildroot}%{_sysconfdir}/yum.repos.d
mkdir -p %{buildroot}%{_sysconfdir}/smart/channels
install -p *.channel %{buildroot}%{_sysconfdir}/smart/channels
mkdir -p %{buildroot}%{_sysconfdir}/apt/sources.d
install -p *.list %{buildroot}%{_sysconfdir}/apt/sources.d

%post
for x in %{_sysconfdir}/apt/* %{_sysconfdir}/apt/*/* \
         %{_sysconfdir}/yum* %{_sysconfdir}/yum*/*; do
  test \! -e $x -o -d $x && continue
  grep apt.physik.fu-berlin.de $x > /dev/null 2>&1 && \
    perl -pi -e's,apt.physik.fu-berlin.de,apt.atrpms.net,g' $x

  grep apt.atrpms.net.*fedora $x > /dev/null 2>&1 && \
    perl -pi -e's,apt.atrpms.net(.*)fedora/([^/]*)/en/([^/ ]*),dl.atrpms.net\1fc\2-\3,g' $x
  grep apt.atrpms.net.*redhat $x > /dev/null 2>&1 && \
    perl -pi -e's,apt.atrpms.net(.*)redhat/([^/]*)/en/([^/ ]*),dl.atrpms.net\1rh\2-\3,g' $x
  grep apt.atrpms.net.*rhel $x > /dev/null 2>&1 && \
    perl -pi -e's,apt.atrpms.net(.*)rhel/([^/]*)/en/([^/ ]*),dl.atrpms.net\1el\2-\3,g' $x

  grep dl.atrpms.net.*/at- $x  > /dev/null 2>&1 && \
    perl -pi -e's,(dl.atrpms.net.*)/at-,\1/atrpms/,g' $x
done
exit 0

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_sysconfdir}/pki
%{_sysconfdir}/yum.repos.d
%{_sysconfdir}/smart
%{_sysconfdir}/apt

%changelog
* Sat Jan  2 2010 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update signing key.

* Sun Jan 25 2009 Axel Thimm <Axel.Thimm@ATrpms.net>
- Rename atrpms-package-config to atrpms-repo.
