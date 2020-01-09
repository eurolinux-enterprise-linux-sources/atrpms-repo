Summary: Configuration files for package managers.
Name: atrpms-repo
Version: 6
Release: 5.el6
License: GPLv3
Group: System Environment/Base
URL: http://ATrpms.net/
Source0: %{name}-%{version}.tgz
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

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cd %{buildroot}
tar xvfz %{SOURCE0}

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
* Wed Mar  9 2011 Troy Dawson <dawson@fnal.gov>
- Changed the yum repos from $releasever to 6

* Sat Jan  2 2010 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update signing key.

* Sun Jan 25 2009 Axel Thimm <Axel.Thimm@ATrpms.net>
- Rename atrpms-package-config to atrpms-repo.
