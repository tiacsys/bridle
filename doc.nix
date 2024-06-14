{
  lib,
  stdenv,
  west2nixHook,
  pythonEnv,
  cmake,
  ninja,
  doxygen,
  mscgen,
  graphviz,
  git,
  zephyr,
  bridle,
  bridleHook,
}:

stdenv.mkDerivation {

  name = "bridle-doc";
  src = bridle;

  nativeBuildInputs = [
    west2nixHook
    bridleHook
    pythonEnv
    cmake
    ninja
    doxygen
    mscgen
    graphviz
    git
  ];

  dontUseCmakeConfigure = true;

  CMAKE_PREFIX_PATH = "/build/bridle/share/bridle-package:/build/zephyr/share/zephyr-package";

  buildPhase = ''
    cd /build
    chmod +w -R ./*
    west build --cmake-only -b none -d build bridle/doc
    west build -t zephyr-doxygen -b none -d build
    west build -t bridle-doxygen -b none -d build
    west build -t build-all -b none -d build
  '';

  installPhase = ''
    mkdir $out
    cp -r build/html $out/
  '';
}
