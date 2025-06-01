{ pkgs ? (import <nixpkgs> {}).pkgs }:
with pkgs;
mkShell {
  buildInputs = [
    python312Packages.tomlkit
    python312Packages.requests
  ];
}
