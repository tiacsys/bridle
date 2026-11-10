{
  pkgs,
  lib,
  zephyr,
  bridle,
  python-deps,
  pyproject-nix,
}:

let

  # Some packages zephyr likes to install using pypi are only provided as applications (or
  # non-Python tools) in nixpkgs. python.buildEnv drops anything that isn't a Python module, so
  # these are mapped into the package set to satisfy the requirements.txt lookup, and added
  # alongside the Python environment below to actually end up on PATH.
  cliTools = {
    inherit (pkgs) sphinx-lint vermin;
    clang-format = pkgs.clang-tools;
    gitlint-core = pkgs.gitlint;
    inherit (python-deps) nrf-regtool;
  };

  # Create a python whose `withPackages` knows about some extra stuff we need
  python = pkgs.python3.override {
    self = python;
    packageOverrides =
      final: prev:
      cliTools
      // {
        # gcovr is a toplevel package in nixpkgs, but built as a Python module, so it can go
        # into the Python environment directly.
        inherit (pkgs) gcovr;

        # Zephyr's compliance requirements want tree-sitter-cmake, which nixpkgs only provides
        # nested inside the tree-sitter-grammars package set.
        inherit (prev.tree-sitter-grammars) tree-sitter-cmake;

        # TODO: Remove once nixpkgs' pyrefly builds again. shacl2code (needed by
        # spdx-python-model for `west spdx`) only uses pyrefly in its test suite, and the
        # pyrefly build currently fails because zstd-sys can't find pkg-config. Skipping
        # shacl2code's tests drops pyrefly from the closure entirely.
        shacl2code = prev.shacl2code.overridePythonAttrs (_: {
          doCheck = false;
        });

        # spsdk and spsdk-pyocd depend on each other. nixpkgs breaks the cycle by
        # not listing spsdk as a dependency of spsdk-pyocd, but the wheel metadata
        # still declares it, so pythonRuntimeDepsCheck fails with "spsdk not
        # installed". spsdk itself pulls in spsdk-pyocd, so both still end up in the
        # environment.
        spsdk-pyocd = prev.spsdk-pyocd.overridePythonAttrs (old: {
          pythonRemoveDeps = (old.pythonRemoveDeps or [ ]) ++ [ "spsdk" ];
        });
      };
  };

  # Parse requirements.txt files into pyproject-nix projects
  zephyr-project = pyproject-nix.lib.project.loadRequirementsTxt {
    requirements = zephyr + "/scripts/requirements.txt";
  };

  bridle-project = pyproject-nix.lib.project.loadRequirementsTxt {
    requirements = bridle + "/zephyr/requirements.txt";
  };

  # Can't validate the combined packages sets, but we can at least check for
  # conflicts within each subset
  invalidConstraints =
    zephyr-project.validators.validateVersionConstraints { inherit python; }
    // bridle-project.validators.validateVersionConstraints { inherit python; };

  pythonEnv = python.buildEnv.override {
    extraLibs =
      (bridle-project.renderers.withPackages {
        inherit python;
        # Nest one project's withPackages within the other to get a combined package
        # set. If we want more than two, we should name these lambdas to reduce
        # indentation.
        extraPackages = (
          zephyr-project.renderers.withPackages {
            inherit python;
            extraPackages = ps: [ ps.west ];
          }
        );
      })
        python.pkgs;
    ignoreCollisions = true;
  };

in
lib.warnIf (invalidConstraints != { })
  "pythonEnv: Found invalid Python constraints for: ${builtins.toJSON (lib.attrNames invalidConstraints)}"
  (
    pkgs.buildEnv {
      name = "bridle-python-env";
      paths = [ pythonEnv ] ++ lib.attrValues cliTools;
    }
  )
