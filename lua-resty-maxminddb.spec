# OpenResty is compatible with 5.1 only!
%global luaver 5.1
%{!?luaver: %global luaver %(lua -e "print(string.sub(_VERSION, 5))" || echo 0)}
%global lualibdir %{_libdir}/lua/%{luaver}
%global luapkgdir %{_datadir}/lua/%{luaver}

%global gittag v%{version}
%global gittag_nov %{version}

Name:           lua-resty-maxminddb
Version:        1.3.0
Release:        1%{?dist}
Summary:        A Lua library for reading MaxMind's Geolocation database
Group:          Development/Libraries
License:        BSD
URL:            https://github.com/anjia0532/lua-resty-maxminddb
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

