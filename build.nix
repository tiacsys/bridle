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
  shields ? [ ],
}:

stdenv.mkDerivation {
  name = builtins.baseNameOf app-path;

  meta = lib.optionalAttrs (lib.strings.hasInfix "native_sim" board) {
    mainProgram = "zephyr.exe";
  };

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
  ]
  ++ lib.concatMap (shield: [
    "--shield"
    shield
  ]) shields;

  installPhase = ''
    mkdir -p $out/bin
    [ -f build/zephyr/zephyr.exe ] && cp build/zephyr/zephyr.exe $out/bin || true
    [ -f build/zephyr/zephyr.elf ] && cp build/zephyr/zephyr.elf $out/bin || true
    [ -f build/zephyr/zephyr.bin ] && cp build/zephyr/zephyr.bin $out/bin || true
    [ -f build/zephyr/zephyr.hex ] && cp build/zephyr/zephyr.hex $out/bin || true
    [ -f build/zephyr/zephyr.uf2 ] && cp build/zephyr/zephyr.uf2 $out/bin || true
  '';
}
