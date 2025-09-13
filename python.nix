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

      inherit (pkgs) gcovr gitlint ruff;
      clang-format = pkgs.clang-tools;
      imgtool = pkgs.mcuboot-imgtool;

      inherit (python-deps) nrf-regtool sphinx-lint;
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
