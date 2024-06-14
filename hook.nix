{
  lib,
  makeSetupHook,
  gitMinimal,
  bridle,
}:

makeSetupHook {
  name = "nix-bridle-hook.sh";
  propagatedBuildInputs = [ gitMinimal ];
  substitutions = {
    git = lib.getExe gitMinimal;
    inherit bridle;
  };
} ./nix-bridle-hook.sh
