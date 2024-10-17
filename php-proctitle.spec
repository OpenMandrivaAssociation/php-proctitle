%define modname proctitle
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A92_%{modname}.ini

Summary:	Allows setting the current process name on Linux and BSD
Name:		php-%{modname}
Version:	0.1.2
Release:	2
Group:		Development/PHP
License:	PHP License
URL:		https://pecl.php.net/package/proctitle
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Source1:	%{modname}.ini
BuildRequires:	php-devel >= 3:5.2.1
BuildRequires:	dos2unix
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This extension allows changing the current process' name on Linux and *BSD
systems. This is useful when using pcntl_fork() to identify running processes
in process list

%prep

%setup -q -n %{modname}-%{version}
[ "../package.xml" != "/" ] && mv ../package.xml .

cp %{SOURCE1} %{inifile}

find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;

# strip away annoying ^M
find -type f | grep -v ".gif" | grep -v ".png" | grep -v ".jpg" | xargs dos2unix

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --enable-%{modname}=shared,%{_prefix} \

%make
mv modules/*.so .

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/
install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc LICENSE README package*.xml
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Fri May 18 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1.2-1mdv2012.0
+ Revision: 799551
- 0.1.2

* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-17
+ Revision: 797043
- fix build
- add upstream changes (Add a function to set the thread name)
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-16
+ Revision: 761279
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-15
+ Revision: 696456
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-14
+ Revision: 695451
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-13
+ Revision: 646672
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-12mdv2011.0
+ Revision: 629852
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-11mdv2011.0
+ Revision: 628172
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-10mdv2011.0
+ Revision: 600519
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-9mdv2011.0
+ Revision: 588856
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-8mdv2010.1
+ Revision: 514636
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-7mdv2010.1
+ Revision: 485418
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-6mdv2010.1
+ Revision: 468234
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-5mdv2010.0
+ Revision: 451345
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 0.1.1-4mdv2010.0
+ Revision: 397464
- Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-3mdv2010.0
+ Revision: 377017
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-2mdv2009.1
+ Revision: 346596
- rebuilt for php-5.2.9

* Tue Feb 24 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-1mdv2009.1
+ Revision: 344393
- import php-proctitle


* Tue Feb 24 2009 Oden Eriksson <oeriksson@mandriva.org> 0.1.1-1mdv2009.1
- initial Mandriva package
