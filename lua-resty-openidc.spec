# OpenResty is compatible with 5.1 only!
%global luaver 5.1
%{!?luaver: %global luaver %(lua -e "print(string.sub(_VERSION, 5))" || echo 0)}
%global lualibdir %{_libdir}/lua/%{luaver}
%global luapkgdir %{_datadir}/lua/%{luaver}

%global gittag v%{version}
%global gittag_nov %{version}

Name:           lua-resty-openidc
Version:        1.7.4
Release:        2%{?dist}
Summary:        OpenID Connect Relying Party and OAuth 2.0 Resource Server implementation in Lua for NGINX / nginx-module-lua
Group:          Development/Libraries
License:        BSD
URL:            https://github.com/zmartzone/lua-resty-openidc
Source0:        %{url}/archive/%{gittag}/%{name}-%{gittag}.tar.gz

%if 0%{?fedora} || 0%{?rhel} >= 7
Requires:       lua(abi) = %{luaver}
%else
Requires:       lua >= %{luaver}
%endif


Requires:       lua-resty-http >= 0.13
Requires:       lua-resty-session >= 2.8
Requires:       lua-resty-jwt >= 0.2.0
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
# Virtually add license macro for EL6:
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%doc README.md


%changelog
# not maintained

