Name:   ngfd-watch
Version:  0.0.2
Release:  1%{?dist}
Summary:  Watchdog for ngfd
BuildArch:  noarch
License:  GPLv3+
URL:    https://github.com/b100dian/ngfd-watch
Source0:    %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires: systemd

%description
Tries to determine if ngfd service is in a deadlock and kills it if is.

%files
%{_userunitdir}/%{name}.service
%{_bindir}/%{name}.sh

%install
%{__install} -D -m 755 %{name}.sh %{buildroot}%{_bindir}/%{name}.sh
%{__install} -D -m 644 %{name}.service %{buildroot}%{_userunitdir}/%{name}.service

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%changelog
* Tue Jan 10 2023 Vlad G. <vlad@grecescu.net> - 0.0.2-1
- Initial detection by ogg file descriptor