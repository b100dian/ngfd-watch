Name:       ngfd-watch
Version:    0.0.4
Release:    1
Summary:    Watchdog for ngfd
BuildArch:  noarch
License:    GPL-3.0-or-later
URL:        https://github.com/b100dian/ngfd-watch
Source0:    %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires: pkgconfig(systemd)

%description
Determines if ngfd service is in a deadlock and kills it if is.


Custom:
  Repo: https://github.com/b100dian/ngfd-watch
Categories:
  - System

%files
%{_bindir}/%{name}.sh
%{_userunitdir}/%{name}.service
%{_userunitdir}/ngfd.service.wants/ngfd-watch.service

%prep
%setup -q

%build

%install
%{__install} -D -m 755 %{name}.sh %{buildroot}%{_bindir}/%{name}.sh
%{__install} -D -m 644 %{name}.service %{buildroot}%{_userunitdir}/%{name}.service
mkdir %{buildroot}%{_userunitdir}/ngfd.service.wants/
ln -s ../ngfd-watch.service %{buildroot}%{_userunitdir}/ngfd.service.wants/ngfd-watch.service

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%changelog
* Tue Jan 10 2023 Vlad G. <vlad@grecescu.net> - 0.0.4-1
- Display name in notification. Configure via /etc/ngfd-watch.
* Mon Jan 09 2023 Vlad G. <vlad@grecescu.net> - 0.0.3-1
- More sampling + kills by consecutive samples count
* Sun Jan 08 2023 Vlad G. <vlad@grecescu.net> - 0.0.2-1
- Initial detection by ogg file descriptor
