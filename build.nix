{
  lib,
  stdenv,
  zephyr-nix,
  pythonEnv,
  cmake,
  ninja,
  west2nixHook,
  bridleHook,
  gitMinimal,
  bridle,
  app-path,
  board,
  target,
}:

stdenv.mkDerivation {
  name = "helloshell";

  meta.mainProgram = if (lib.strings.hasInfix board "native_sim") then "zephyr.exe" else null;

  nativeBuildInputs = [
    (zephyr-nix.sdk.override {
      targets = [
        target
      ];
    })
    west2nixHook
    bridleHook
    pythonEnv
    zephyr-nix.hosttools-nix
    gitMinimal
    cmake
    ninja
  ];

  # Note: This should be set by the hook but it's tricky to get the ordering correct
  dontUseCmakeConfigure = true;

  CMAKE_PREFIX_PATH = "/build/bridle/share/bridle-package:/build/zephyr/share/zephyr-package";

  src = bridle;

  westBuildFlags = [
    app-path
    "-b"
    board
  ];

  installPhase = ''
    mkdir -p $out/bin
    [ -f build/zephyr/zephyr.exe ] && cp build/zephyr/zephyr.exe $out/bin || true
    [ -f build/zephyr/zephyr.elf ] && cp build/zephyr/zephyr.elf $out/bin || true
    [ -f build/zephyr/zephyr.bin ] && cp build/zephyr/zephyr.bin $out/bin || true
    [ -f build/zephyr/zephyr.hex ] && cp build/zephyr/zephyr.hex $out/bin || true
  '';
}
