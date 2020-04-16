# OpenResty is compatible with 5.1 only!
%global luaver 5.1
%{!?luaver: %global luaver %(lua -e "print(string.sub(_VERSION, 5))" || echo 0)}
%global lualibdir %{_libdir}/lua/%{luaver}
%global luapkgdir %{_datadir}/lua/%{luaver}

%global gittag v0.01-6
%global gittag_nov 0.01-6

Name:           lua-resty-newrelic
Version:        0.1.post6
Release:        1%{?dist}
Summary:        This Lua library is a luajit ffi-based wrapper around newrelic agent SDK for nginx-module-lua nginx module
Group:          Development/Libraries
License:        BSD
URL:            https://github.com/saks/lua-resty-newrelic
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
# Virtually add license macro for EL6:
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md


%changelog
# not maintained

