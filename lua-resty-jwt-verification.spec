%{!?luaver: %global luaver %(lua -e "print(string.sub(_VERSION, 5))" || echo 0)}
%global luapkgdir %{_datadir}/lua/%{luaver}
%global lualibdir %{_libdir}/lua/%{luaver}
# OpenResty is compatible with 5.1 only! We must build 5.1 version always, even on <= EL8
%global luacompatver 5.1
%global luacompatpkgdir %{_datadir}/lua/%{luacompatver}
%global luacompatlibdir %{_datadir}/lua/%{luacompatver}

%global luapkgname resty-jwt-verification

%global gittag v%{version}
%global gittag_nov %{version}

Name:           lua-%{luapkgname}
Version:        0.6.0
Release:        4%{?dist}
Summary:        JWT verification library for nginx-module-lua with JWKS integration
Group:          Development/Libraries
License:        BSD
URL:            https://github.com/anvouk/lua-resty-jwt-verification
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


Requires:       lua-resty-openssl >= 1.6.2
Requires:       lua-resty-http >= 0.17.1
BuildArch: noarch

%description
%{summary}.

%if 0%{?fedora} || 0%{?rhel} > 7
%package -n lua%{luacompatver}-%{luapkgname}
Summary:        JWT verification library for nginx-module-lua with JWKS integration for Lua %{luacompatver}

Requires:       lua%{luacompatver}-resty-openssl >= 1.6.2
Requires:       lua%{luacompatver}-resty-http >= 0.17.1
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
%license LICENSE
%doc README.md


%if 0%{?fedora} || 0%{?rhel} > 7
%files -n lua%{luacompatver}-%{luapkgname}
%{luacompatpkgdir}/*
# Virtually add license macro for EL6:
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md
%endif



%changelog
# not maintained
