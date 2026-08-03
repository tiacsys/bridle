{
  pkgs,
  lib,
  zephyr,
  bridle,
  python-deps,
  pyproject-nix,
}:

let

  # Create a python whose `withPackages` knows about some extra stuff we need
  python = pkgs.python3.override {
    self = python;
    packageOverrides = final: prev: {
      # Some packages zephyr likes to install using pypi are provided as toplevel packages in
      # nixpkgs. Adding them to this package set makes sure they can be pulled into the build/dev
      # environment by being referenced in a requirements.txt

      inherit (pkgs) gcovr ruff vermin;
      clang-format = pkgs.clang-tools;
      imgtool = pkgs.mcuboot-imgtool;
      gitlint-core = pkgs.gitlint;

      inherit (python-deps) nrf-regtool sphinx-lint;

      # TODO: Remove this workaround once NixOS/nixpkgs#573479 reaches nixos-unstable.
      # buildPythonPackage now defaults to __structuredAttrs = true, under which
      # nixpkgs' sphinxHook only runs the first entry of sphinxBuilders. reuse's
      # "man" builder is therefore skipped and the build fails with "failed to
      # produce output path for output 'man'". reuse is needed for `west spdx`.
      reuse = prev.reuse.overridePythonAttrs (_: {
        __structuredAttrs = false;
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

in
lib.warnIf (invalidConstraints != { })
  "pythonEnv: Found invalid Python constraints for: ${builtins.toJSON (lib.attrNames invalidConstraints)}"
  (
    python.buildEnv.override {
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
    }
  )
