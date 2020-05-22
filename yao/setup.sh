#!/bin/bash
julia --color=yes -e "using Pkg;Pkg.activate(@__DIR__);Pkg.instantiate(verbose=true)"
