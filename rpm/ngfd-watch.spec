Name:   ngfd-watch
Version:  0.0.1
Release:  1%{?dist}
Summary:  Watchdog for ngfd
BuildArch:  noarch
License:  GPLv3+
URL:    https://github.com/b100dian/ngfd-watch

BuildRequires: systemd
#BuildRequires: systemd-rpm-macros

%description
Tries to determine if ngfd service is in a deadlock and kills it if is.

%files
%{_unitdir}/user/%{name}.service
%{_bindir}/%{name}.sh

%install
install -D -m 644 %{name}.sh %{buildroot}%{_bindir}/%{name}.sh
install -D -m 644 %{name}.service %{buildroot}%{_unitdir}/user/%{name}.service

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%changelog
* Tue Jan 10 2023 Vlad G. <vlad@grecescu.net> - 0.0.1-1
- Initial detection by ogg file descriptor