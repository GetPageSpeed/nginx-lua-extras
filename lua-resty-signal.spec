# OpenResty is compatible with 5.1 only!
%global luaver 5.1
%{!?luaver: %global luaver %(lua -e "print(string.sub(_VERSION, 5))" || echo 0)}
%global lualibdir %{_libdir}/lua/%{luaver}
%global luapkgdir %{_datadir}/lua/%{luaver}

%global gittag v0.02
%global gittag_nov v0.02

Name:           lua-resty-signal
Version:        0.2
Release:        1%{?dist}
Summary:        Lua library for killing or sending signals to UNIX processes
Group:          Development/Libraries
License:        BSD
URL:            https://github.com/openresty/lua-resty-signal
Source0:        %{url}/archive/%{gittag}.tar.gz

%if 0%{?fedora} || 0%{?rhel} >= 7
Requires:       lua(abi) = %{luaver}
%else
Requires:       lua >= %{luaver}
%endif

BuildArch:      noarch

%description
%{summary}.


%prep
%autosetup -n %{name}-%{gittag_nov}


%build
# nothing to do


%install
mkdir -p $RPM_BUILD_ROOT%{luapkgdir}
cp -pr lib/* $RPM_BUILD_ROOT%{luapkgdir}


%check


%files
%{luapkgdir}/*
%doc README.md


%changelog
# not maintained

