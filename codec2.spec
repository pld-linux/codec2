#
# Conditional build:
%bcond_with	tests	# unit tests
%bcond_without	lpcnet	# LPCNet support
#
Summary:	Speech codec for 2400 bit/s and below
Summary(pl.UTF-8):	Kodek mowy do przesyłania danych 2400 bitów/s i poniżej
Name:		codec2
Version:	0.9.2
Release:	1
License:	LGPL v2.1
Group:		Libraries
#Source0Download: https://github.com/drowe67/codec2/releases
Source0:	https://github.com/drowe67/codec2/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e2f5e0a7a15f172ecb9875332d9a83e0
URL:		http://rowetel.com/codec2.html
BuildRequires:	cmake >= 3.0
%{?with_lpcnet:BuildRequires:	lpcnetfreedv-devel}
%if %{with tests}
BuildRequires:	libsamplerate-devel
BuildRequires:	speex-devel
BuildRequires:	speexdsp-devel
%endif
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Codec 2 is an open source (LGPL licensed) speech codec for 2400 bit/s
and below. This is the runtime library package.

%description -l pl.UTF-8
Codec 2 to mający otwarte źródła (na licencji LGPL) kodek mowy dla
szybkości przesyłania danych 2400 bit/s i niższych. Ten pakiet zawiera
bibliotekę uruchomieniową.

%package devel
Summary:	Header files for Codec 2 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Codec 2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Codec 2 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Codec 2.

%package tools
Summary:	Tools for encoding and decoding in Codec 2 format
Summary(pl.UTF-8):	Narzędzia do kodowania i dekodowania w formacie Codec 2
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description tools
Tools for encoding and decoding in Codec 2 format.

%description tools -l pl.UTF-8
Narzędzia do kodowania i dekodowania w formacie Codec 2.

%prep
%setup -q

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	%{?with_lpcnet:-DLPCNET=ON} \
	%{!?with_tests:-DUNITTEST=OFF}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README*
%attr(755,root,root) %{_libdir}/libcodec2.so.0.9

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcodec2.so
%{_includedir}/codec2
%{_libdir}/cmake/codec2
%{_pkgconfigdir}/codec2.pc

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/c2dec
%attr(755,root,root) %{_bindir}/c2enc
%attr(755,root,root) %{_bindir}/drs232
%attr(755,root,root) %{_bindir}/drs232_ldpc
%attr(755,root,root) %{_bindir}/fdmdv_demod
%attr(755,root,root) %{_bindir}/fdmdv_get_test_bits
%attr(755,root,root) %{_bindir}/fdmdv_mod
%attr(755,root,root) %{_bindir}/fdmdv_put_test_bits
%attr(755,root,root) %{_bindir}/fm_demod
%attr(755,root,root) %{_bindir}/fsk_mod
%attr(755,root,root) %{_bindir}/insert_errors
