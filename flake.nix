{
  description = "A flake for working with Bridle";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";

    zephyr = {
      type = "github";
      owner = "tiacsys";
      repo = "zephyr";
      ref = "tiacsys/main";
      flake = false;
    };

    zephyr-nix = {
      url = "github:adisbladis/zephyr-nix";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.zephyr.follows = "zephyr";
    };

    west2nix = {
      url = "github:adisbladis/west2nix";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.zephyr-nix.follows = "zephyr-nix";
    };

    pyproject-nix.url = "github:nix-community/pyproject.nix";

    python-deps = {
      type = "github";
      owner = "Irockasingranite";
      repo = "bridle-python-deps";
      ref = "main";
      inputs.nixpkgs.follows = "nixpkgs";
    };

  };

  outputs = { self, nixpkgs, flake-utils, ... }@inputs:
    (flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        inherit (nixpkgs) lib;

        west2nix = callPackage inputs.west2nix.lib.mkWest2nix { };

        callPackage = pkgs.newScope (pkgs // {
          bridle = self;
          zephyr = inputs.zephyr;
          zephyr-nix = inputs.zephyr-nix.packages.${system};
          pyproject-nix = inputs.pyproject-nix;
          pythonEnv = callPackage ./python.nix {
            python-deps = inputs.python-deps.packages.${system};
          };
          west2nixHook = west2nix.mkWest2nixHook {
            manifest = ./west2nix.toml;
          };
        });

      in {
        formatter = pkgs.nixfmt;

        packages.west2nix = inputs.west2nix.packages.${system}.default;

        devShells.default = callPackage ./shell.nix { };

        packages.doc = callPackage ./doc.nix { };
      }));
}
