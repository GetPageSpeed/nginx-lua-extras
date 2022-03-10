# nginx-lua-extras

For RHEL 8, two package versions are built for every library.
The 5.1 (OpenResty version), and the default 5.3 Lua version.

The lua5.1-libname in RHEL 8 is according to [conventions](https://docs.fedoraproject.org/en-US/packaging-guidelines/Naming/#_lua_modules).

## Building

Run `make` and this automatically runs:

*   `generate-definitions.py` to hunt down Lua resty modules on GitHub and generate `.yml` definitions
    for them over to `resty/*.yml`
*   `generate.sh` which generates spec files from the module definitions, and push updated specs to this repo.

Finally, CircleCi picks up changes on the repo and runs `rpmbuilder` and deployment of RPM files. 

## Automation

The `make` is run daily on the build server.