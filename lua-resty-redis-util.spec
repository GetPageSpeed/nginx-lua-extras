# OpenResty is compatible with 5.1 only!
%global luaver 5.1
%{!?luaver: %global luaver %(lua -e "print(string.sub(_VERSION, 5))" || echo 0)}
%global lualibdir %{_libdir}/lua/%{luaver}
%global luapkgdir %{_datadir}/lua/%{luaver}

%global gittag v%{version}
%global gittag_nov %{version}

Name:           lua-resty-redis-util
Version:        0.0.5
Release:        2%{?dist}
Summary:        Nginx-module-lua-resty-redis 封装工具类
Group:          Development/Libraries
License:        BSD
URL:            https://github.com/anjia0532/lua-resty-redis-util
Source0:        %{url}/archive/%{gittag}/%{name}-%{gittag}.tar.gz

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

