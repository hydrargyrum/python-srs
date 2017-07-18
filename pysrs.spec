%define name pysrs
%define version 0.30.5
%define release 1

Summary: Python SRS (Sender Rewriting Scheme) library
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.gz
License: Python license
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
BuildArchitectures: noarch
Vendor: Stuart Gathman (Perl version by Shevek) <stuart@bmsi.com>
Packager: Stuart D. Gathman <stuart@bmsi.com>
Url: http://bmsi.com/python/pysrs.html

%description
Python SRS (Sender Rewriting Scheme) library.
As SPF is implemented, mail forwarders must rewrite envfrom for domains
they are not authorized to send from.

See http://spf.pobox.com/srs.html for details.
The Perl reference implementation is at http://www.anarres.org/projects/srs/


%prep
%setup

%build
python2.3 setup.py build

%install
python2.3 setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
mkdir -p $RPM_BUILD_ROOT/etc/mail
cp pysrs.cfg $RPM_BUILD_ROOT/etc/mail

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
%config /etc/mail/pysrs.cfg

%changelog
* Mon Mar 22 2004 Stuart Gathman <stuart@bmsi.com> 0.30.5-1
- Make sendmail map use config in /etc/mail/pysrs.cfg