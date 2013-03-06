%global gem_name awestruct
#%global mandir %{_mandir}/man1

Summary: A static site generation tool
Name: rubygem-%{gem_name}
Version: 0.4.8
Release: 1%{?dist}
Group: Development/Tools
License: MIT
URL: http://awestruct.org
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?fedora} <= 18
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
Requires: rubygem(mustache)
Requires: rubygem(rdiscount)
Requires: rubygem(RedCloth)
Requires: rubygem(coffee-script)
Requires: rubygem(thin)
Requires: rubygem(rb-inotify)
BuildRequires: rubygems-devel
BuildRequires: ruby(rubygems)
#BuildRequires: rubygem(rspec)
#BuildRequires: rubygem(rake)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
A build tool for generating static HTML websites from templates that are fed
through an extension pipeline.

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
#%patch0 -p1
#%patch1 -p1

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
#%exclude %{gem_instdir}/Gemfile
#%exclude %{gem_instdir}/Rakefile
#%exclude %{gem_instdir}/test
#%exclude %{gem_instdir}/man
#%{gem_instdir}/LICENSE
#%{gem_instdir}/README.*
%{_bindir}/*
%{gem_instdir}/bin
%{gem_libdir}
#%{mandir}/*
%{gem_spec}

%files doc
%doc %{gem_docdir}

%changelog
* Fri Mar 01 2013 Dan Allen <dan.j.allen@gmail.com> - 0.1.1-1
- Initial package
