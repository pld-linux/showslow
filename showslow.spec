# http://www.showslow.org/Installation_and_configuration
Summary:	Show Slow is an open source tool that helps monitor various website performance metrics over time
Name:		showslow
Version:	0.16.1
Release:	0.3
License:	New BSD License
Group:		Applications/WWW
Source0:	https://github.com/downloads/sergeychernyshev/showslow/%{name}_%{version}.tar.bz2
# Source0-md5:	9109edaad1eae53af06f40c3f43acdc9
#Source1:	apache.conf
#Source2:	lighttpd.conf
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	webapps
#Requires:	webserver(access)
#Requires:	webserver(alias)
#Requires:	webserver(auth)
#Requires:	webserver(cgi)
#Requires:	webserver(indexfile)
Requires:	webserver(php)
#Requires:	webserver(setenv)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

# in case _sysconfdir is not in webapps dir, run this replace pattern
# before copy-pasting to your spec: :%s#%{_sysconfdir}#%{_webapps}/%{_webapp}#g

%description
Show Slow is an open source tool that helps monitor various website
performance metrics over time. It captures the results of YSlow, Page
Speed and dynaTrace AJAX rankings and graphs them, to help you
understand how various changes to your site affect its performance.

%prep
%setup -qn %{name}_%{version}

cat > apache.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

cat > lighttpd.conf <<'EOF'
alias.url += (
    "/%{name}" => "%{_appdir}",
)
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}
cp -a . $RPM_BUILD_ROOT

cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -a lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

#mv $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}}/apache.conf
#mv $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}}/lighttpd.conf
#cp -a $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf

#cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
#cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
#cp -a $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf

# %webapp_* macros usage extracted from %{_prefix}/lib/rpm/macros.build:
#
# Usage:
#   %%webapp_register HTTPD WEBAPP
#   %%webapp_unregister HTTPD WEBAPP

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.markdown 
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%{_appdir}
