# OpenResty is compatible with 5.1 only!
%global luaver 5.1
%{!?luaver: %global luaver %(lua -e "print(string.sub(_VERSION, 5))" || echo 0)}
%global lualibdir %{_libdir}/lua/%{luaver}
%global luapkgdir %{_datadir}/lua/%{luaver}

%global gittag v%{version}
%global gittag_nov %{version}

Name:           lua-resty-jump-consistent-hash
Version:        0.1.4
Release:        2%{?dist}
Summary:        Consistent hash for nginx-module-lua
Group:          Development/Libraries
License:        BSD
URL:            https://github.com/ruoshan/lua-resty-jump-consistent-hash
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

