{ pkgs ? (import <nixpkgs> {}).pkgs }:
with pkgs;
mkShell {
  buildInputs = [
    python312Packages.html5lib
    python312Packages.beautifulsoup4
    python312Packages.requests
  ];
}
