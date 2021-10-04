{ pkgs ? import <nixpkgs> {}
, mkDerivation ? pkgs.stdenv.mkDerivation
, python ? pkgs.python39
}:
mkDerivation rec {
    name = "stregsystem-cli";

    buildInputs = [
        (python.withPackages (pypkgs: [ pypkgs.requests ]))
    ];

    dontUnpack = true;
    dontBuild = true;
    installPhase = ''
        mkdir -p $out/bin
        cp ${./main.py} $out/bin/sts
        chmod +x $out/bin/sts
    '';
}
