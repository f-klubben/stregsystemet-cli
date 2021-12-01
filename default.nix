{ pkgs ? import <nixpkgs> {}
, mkDerivation ? pkgs.stdenv.mkDerivation
}:
mkDerivation rec {
    name = "stregsystem-cli";

	python = pkgs.python39.withPackages (pypkgs: [
    	pypkgs.requests
	]);

    nativeBuildInputs = [
        python
    ];

    dontUnpack = true;
    dontBuild = true;
    installPhase = ''
        mkdir -p $out/bin
        cp ${./main.py} $out/bin/.sts-wrapped
        chmod +x $out/bin/.sts-wrapped
        echo -e "#!/bin/sh\n${python}/bin/python $out/bin/.sts-wrapped\n" > $out/bin/sts
        chmod +x $out/bin/sts
    '';
}
