%global gem_name awestruct
#%global mandir %{_mandir}/man1

Summary: A static site generation tool
Name: rubygem-%{gem_name}
Version: 0.5.0
Release: 1%{?dist}
Group: Development/Tools
License: MIT
URL: http://awestruct.org
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# Patch0: Disable the minify extension since it depends on compressor libraries
# not available on Fedora (rubygem-htmlcompressor)
Patch0: awestruct-disable-minify-extension.patch
# Patch1: Disable the s3 deployer since it depends on a library not yet
# available in Fedora (rubygem-s3cmd)
Patch1: awestruct-disable-s3-deployer.patch
# Patch2: Disable the bootstrap sass integration since its not yet available in
# Fedora (rubygem-bootstrap-sass)
Patch2: awestruct-remove-bootstrap-sass-import.patch
# Patch3: Set the EXECJS_RUNTIME environment variable suitable for Fedora
Patch3: awestruct-set-execjs-runtime.patch
%if 0%{?fedora} < 19
Requires: ruby(abi) = 1.9.1
BuildRequires: ruby(abi) = 1.9.1
%else
Requires: ruby(release)
BuildRequires: ruby(release)
%endif
Requires: ruby(rubygems)
Requires: rubygem(hpricot)
Requires: rubygem(tilt)
Requires: rubygem(compass)
Requires: rubygem(compass-960-plugin)
#Requires: rubygem(bootstrap-sass)
Requires: rubygem(json)
Requires: rubygem(rest-client)
Requires: rubygem(git)
#Requires: rubygem(htmlcompressor)
Requires: rubygem(uglifier)
#Requires: rubygem(ruby-s3cmd)
Requires: rubygem(listen)
Requires: rubygem(rack)
Requires: rubygem(eventmachine)
Requires: rubygem(coffee-script)
Requires: rubygem(rb-inotify)
BuildRequires: rubygems-devel
BuildRequires: ruby(rubygems)
#BuildRequires: rubygem(rspec)
#BuildRequires: rubygem(rake)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Awestruct is a build tool for creating non-trivial static websites using tools
like Compass, Haml, Markdown and AsciiDoc as well as common CSS frameworks like
Twitter Bootstrap and Blueprint.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack -V %{SOURCE0}
%setup -q -D -T -n %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
# loosen dependency requirements since they're determined by packaging system
sed -i "s/\(_dependency(.*\), .*/\1)/" %{gem_name}.gemspec
sed -i "s/.*\(bootstrap-sass\|ruby-s3cmd\|htmlcompressor\)/#&/" %{gem_name}.gemspec

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
gem build %{gem_name}.gemspec
%gem_install

%check
# can't run tests from here, they aren't distributed
#LANG=en_US.utf8 rspec spec/*_spec.rb

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

#mkdir -p %{buildroot}%{mandir}
#cp -pa .%{gem_instdir}/man/*.1 \
#        %{buildroot}%{mandir}/

%files
%dir %{gem_instdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/%{gem_name}.gemspec
#%exclude %{gem_instdir}/test
#%exclude %{gem_instdir}/man
%{_bindir}/*
%{gem_instdir}/bin
%{gem_libdir}
#%{mandir}/*
%{gem_spec}

%files doc
%doc %{gem_docdir}

%changelog
* Wed Mar 06 2013 Dan Allen <dan.j.allen@gmail.com> - 0.5.0-1
- Initial package
