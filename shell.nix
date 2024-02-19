{ lib
, callPackage
, pythonEnv
, mkShell
, zephyr
, zephyr-nix
, bridle
, cmake
, ninja
, git
}:

mkShell {
  packages = [
    zephyr-nix.sdkFull
    zephyr-nix.hosttools-nix
    pythonEnv
    cmake
    ninja
    git
  ];

  LC_ALL = "C.UTF-8"; # Needed by sphinx

  shellHook = ''
    export CMAKE_PREFIX_PATH=$(realpath ${bridle}/share/bridle-package/cmake):$CMAKE_PREFIX_PATH;
    export CMAKE_PREFIX_PATH=$(realpath ${zephyr}/share/zephyr-package/cmake):$CMAKE_PREFIX_PATH;
  '';
}
