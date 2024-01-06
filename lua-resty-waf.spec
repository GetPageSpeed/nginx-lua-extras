%{!?luaver: %global luaver %(lua -e "print(string.sub(_VERSION, 5))" || echo 0)}
%global luapkgdir %{_datadir}/lua/%{luaver}
%global lualibdir %{_libdir}/lua/%{luaver}
# OpenResty is compatible with 5.1 only! We must build 5.1 version always, even on <= EL8
%global luacompatver 5.1
%global luacompatpkgdir %{_datadir}/lua/%{luacompatver}
%global luacompatlibdir %{_datadir}/lua/%{luacompatver}

%global luapkgname resty-waf

%global gittag v%{version}
%global gittag_nov %{version}

Name:           lua-%{luapkgname}
Version:        0.11.1
Release:        4%{?dist}
Summary:        High-performance WAF built on nginx-module-lua stack
Group:          Development/Libraries
License:        BSD
URL:            https://github.com/p0pr0ck5/lua-resty-waf
Source0:        %{url}/archive/%{gittag}/%{name}-%{gittag}.tar.gz

%if 0%{?fedora} || 0%{?rhel} >= 7
Requires:       lua(abi) = %{luaver}
%else
Requires:       lua >= %{luaver}
%endif

%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires:  compat-lua >= %{luacompatver}, compat-lua-devel >= %{luacompatver}
Requires:       lua(abi) = %{luacompatver}
%endif


Requires:       lua-resty-iputils
Requires:       lua-resty-cookie
Requires:       lua-resty-logger-socket
BuildArch: noarch

%description
%{summary}.

%if 0%{?fedora} || 0%{?rhel} > 7
%package -n lua%{luacompatver}-%{luapkgname}
Summary:        High-performance WAF built on nginx-module-lua stack for Lua %{luacompatver}

Requires:       lua%{luacompatver}-resty-iputils
Requires:       lua%{luacompatver}-resty-cookie
Requires:       lua%{luacompatver}-resty-logger-socket
%description -n lua%{luacompatver}-%{luapkgname}
%{summary}.
%endif


%prep
%autosetup -n %{name}-%{gittag_nov}


%build
# nothing to do


%install
mkdir -p $RPM_BUILD_ROOT%{luapkgdir}
cp -pr lib/* $RPM_BUILD_ROOT%{luapkgdir}

%if 0%{?fedora} || 0%{?rhel} > 7
mkdir -p $RPM_BUILD_ROOT%{luacompatpkgdir}
cp -pr lib/* $RPM_BUILD_ROOT%{luacompatpkgdir}
%endif


%check
# nothing to do

%files
%{luapkgdir}/*
# Virtually add license macro for EL6:
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README.md


%if 0%{?fedora} || 0%{?rhel} > 7
%files -n lua%{luacompatver}-%{luapkgname}
%{luacompatpkgdir}/*
# Virtually add license macro for EL6:
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README.md
%endif



%changelog
# not maintained
