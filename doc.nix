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
}:

stdenv.mkDerivation {

  name = "bridle-doc";
  src = bridle;
  unpackPhase = ''
    cp -r ${bridle} bridle
    chmod +w -R bridle
    cd bridle
    git init
    git config user.email "foo@bar.com"
    git config user.name "Foo"
    git checkout -b fake-branch
    git add -A
    git commit -m "Fake Commnit"
    cd ..
  '';

  nativeBuildInputs = [
    west2nixHook
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
