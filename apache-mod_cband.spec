#Module-Specific definitions
%define mod_name mod_cband
%define mod_conf A43_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Apache 2 Bandwidth Quota Module
Name:		apache-%{mod_name}
Version:	0.9.7.5
Release:	%mkrel 11
Group:		System/Servers
License:	GPL
URL:		http://cband.linux.pl/
Source0:	http://cband.linux.pl/download/mod-cband-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= 2.2.0
Requires(pre):  apache >= 2.2.0
Requires:       apache-conf >= 2.2.0
Requires:       apache >= 2.2.0
BuildRequires:  apache-devel >= 2.2.0
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_cband is an Apache 2 module provided to solve the problem of
limiting users' and virtualhosts' bandwidth usage. When the
configured virtualhost's transfer limit is exceeded, mod_cband
will redirect all further requests to a location specified in the
configuration file. 

%prep

%setup -q -n mod-cband-%{version}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
cp src/* .

%{_sbindir}/apxs -Wc,-Wall -Wc,-DDST_CLASS=3 -c %{mod_name}.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}/var/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}/var/www/html/addon-modules/%{name}-%{version}

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc conf/* AUTHORS Changes INSTALL LICENSE libpatricia.copyright
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
/var/www/html/addon-modules/*


